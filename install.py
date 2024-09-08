import os, sys, time, re
import subprocess, base64
import requests as api_requests
import zipfile
import importlib.util

username, modulename, filedir = (
    "LcfherShell",
    "SuperNano",
    os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"),
)
urlgitversion = f"https://api.github.com/repos/{username}/{modulename}/branches"
urlfilezipper = (
    f"https://github.com/{username}/{modulename}/archive/refs/heads/lastverion.zip"
)


def search_like_regex(data_list, pattern):
    """Mencari elemen dalam daftar yang cocok dengan pola regex."""
    regex = re.compile(pattern, re.IGNORECASE)
    return [item for item in data_list if regex.search(item)]


def install_packages(packages: list):
    """Menginstal beberapa paket Python menggunakan pip."""
    len_pkg: int = packages.__len__()
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
            print(f"Packages {pkg} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during package installation: {pkg}")
            len_pkg -= 1
            if pkg == "logging":
                len_pkg += 1
        except Exception as e:
            print(f"General error during package installation: {pkg}")
            len_pkg -= 1
            if pkg == "logging":
                len_pkg += 1
        except:
            if pkg == "logging":
                len_pkg += 1
    if len_pkg < packages.__len__():
        return False
    return True


def module_version():
    """Mendapatkan semua versi modul dari GitHub."""
    maxreplay = 12
    while maxreplay > 0:
        try:
            response = api_requests.get(urlgitversion)
            response.raise_for_status()
            results = response.json()
            return [x["name"] for x in results if x["name"] != "main"]
        except:
            time.sleep(2)
            maxreplay -= 1
    return []


def download_file(url: str, local_filename: str):
    """Mengunduh file dari URL dengan retry jika terjadi kegagalan."""
    attempt, max_retries, wait_time = 0, 3, 1
    while attempt < max_retries:
        try:
            with api_requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(local_filename, "wb") as file:
                    for chunk in response.iter_content(chunk_size=None):
                        file.write(chunk)
            if os.path.isfile(local_filename):
                print(f"File downloaded successfully: {local_filename}")
                return local_filename
        except api_requests.RequestException as e:
            attempt += 1
            print(f"Download failed: {e}. Attempt {attempt} of {max_retries}.")
            time.sleep(wait_time)
    print(f"All download attempts failed for: {url}")
    return None


def unzip_folder_contents(zip_path: str, extract_to: str, folder_name: str):
    """
    Mengekstrak isi folder tertentu di dalam ZIP ke luar folder, langsung ke direktori tujuan.

    :param zip_path: Path dari file ZIP.
    :param extract_to: Direktori tujuan untuk mengekstrak file.
    :param folder_name: Nama folder di dalam ZIP yang isinya ingin diekstrak.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # Dapatkan semua file di dalam ZIP
        all_files = zip_ref.namelist()

        # Filter file yang berada di dalam folder tertentu
        folder_files = [f for f in all_files if f.startswith(folder_name + "/")]

        if not folder_files:
            print(f"Folder '{folder_name}' not found in ZIP.")
            return

        # Ekstrak file yang berada di dalam folder tanpa menyertakan folder_name di path tujuan
        for file in folder_files:
            # Hapus nama folder dari path untuk mengekstrak file langsung ke direktori tujuan
            extracted_path = os.path.join(
                extract_to, os.path.relpath(file, folder_name)
            )

            # Jika file adalah folder, buat direktori
            if file.endswith("/"):
                os.makedirs(extracted_path, exist_ok=True)
            else:
                # Jika file, ekstrak file
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                with zip_ref.open(file) as source, open(extracted_path, "wb") as target:
                    target.write(source.read())

        print(
            f"Contents of folder '{folder_name}' successfully extracted to: {extract_to}"
        )


# Encoding string menjadi Base64
def encode_base64(input_string):
    message_bytes = input_string.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("utf-8")
    return base64_message


# Decoding Base64 menjadi string
def decode_base64(base64_string):
    base64_bytes = base64_string.encode("utf-8")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("utf-8")
    return message


# Caesar cipher encryption
def caesar_encrypt(input_string, shift):
    encrypted = []
    for char in input_string:
        # Encrypt only alphabetic characters
        if char.isalpha():
            shift_base = ord("a") if char.islower() else ord("A")
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)
    return "".join(encrypted)


# Caesar cipher decryption
def caesar_decrypt(encrypted_string, shift):
    decrypted = []
    for char in encrypted_string:
        if char.isalpha():
            shift_base = ord("a") if char.islower() else ord("A")
            decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return "".join(decrypted)


def encrypt_and_encode(input_string, shift):
    encrypted_message = caesar_encrypt(input_string, shift)
    return encode_base64(encrypted_message)


# Decode Base64, then decrypt
def decode_and_decrypt(base64_string, shift):
    decrypted_message = decode_base64(base64_string)
    return caesar_decrypt(decrypted_message, shift)


def loadinitmodule():
    file_path = os.path.join(os.path.dirname(__file__), "__init__.py")
    # Memuat spesifikasi modul
    spec = importlib.util.spec_from_file_location("__init__", file_path)
    init_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(init_module)
    return init_module


def rename(paths: str):
    listApps, allmodifed = [[], []]
    for path in tuple(os.listdir(paths)):
        locationApp = os.path.join(paths, path)
        if os.path.isfile(locationApp) and path.endswith((".exe", "exe")):
            listApps.append((locationApp, round(os.path.getctime(locationApp))))
    try:
        for app in listApps:
            allmodifed.append(app[1])
        locationApp = listApps[allmodifed.index(max(allmodifed))][0]
        file_name, ext = list(os.path.splitext(os.path.basename(locationApp)))
        if str(file_name).lower() == "supernano":
            return True
        newfile_name = "{files}{ext}".format(
            files=str(file_name).replace(str(file_name), "supernano"), ext=ext
        )
        dirnames = os.path.dirname(locationApp)
        newfile_name = os.path.realpath(os.path.join(dirnames, newfile_name))
        try:
            os.rename(os.path.realpath(locationApp), newfile_name)
        except:
            return False
        return True
    except:
        return False


def setupyinstaller(data: list):
    xdata: list = []
    if data.__len__() > 0:
        for d in data:
            d = str(d).strip()
            d = d.split("=", 1)[0]
            if d.startswith("windows-curses"):
                d = d.replace("windows-curses", "curses")
            xdata.append(d)
        xdata.extend(["requests", "re", "shutil"])
        return "--hidden-import={hidden_p}".format(
            hidden_p=" --hidden-import=".join(xdata)
        )
    return ""


def install_script():
    filemainapps = os.path.join(filedir, "supernano.py")
    shift = 4  # Shift untuk Caesar cipher
    if os.path.isfile(filemainapps):
        userinput = input("Do you want to install the .exe file?: [y/n]")
        if userinput.lower() == "y":
            dfiles = str(open(filemainapps, "r+").read())
            blobfile = loadinitmodule()

            decoded_dataOLD = str(
                decode_and_decrypt(blobfile.encoded_dataOLD, shift)
            ).strip()
            decoded_dataNOW = str(
                decode_and_decrypt(blobfile.encoded_dataNOW, shift)
            ).strip()
            with open(filemainapps, "w+") as wf:
                wf.write(dfiles.replace(decoded_dataOLD, decoded_dataNOW, 1))

            requirements = os.path.join(filedir, "requirements.txt")
            if os.path.isfile(requirements):
                with open(requirements, "r") as fd:
                    packages = fd.read().splitlines()
                command = f"""pyinstaller --onefile {setupyinstaller(packages)} --add-data "libs;libs"  --add-data "cache;cache" supernano.py"""
                os.system(command)
            try:
                os.remove(filemainapps)
            except:
                os.unlink(filemainapps)
            print(os.path.isfile(requirements))
            statRename = rename(os.path.realpath(os.path.join(filedir, "dist")))
            if statRename == True:
                print("The app has been created..")
        return
    versions, session = sorted(module_version()), 4
    if not versions:
        print("Failed to get module version.")
        return

    print("Available versions:")
    for index, item in enumerate(versions):
        print(f"{index + 1}. {item}")

    getversion = None
    while True:
        try:
            userinput = input("Select version by number or name:")
            if userinput.isdigit() and 0 < int(userinput) <= len(versions):
                getversion = versions[int(userinput) - 1]
                break
            else:
                matches = search_like_regex(versions, userinput)
                if matches:
                    getversion = matches[0]
                    break
        except KeyboardInterrupt:
            if session <= 0:
                return
            session -= 1
        print("No valid version has been selected.")

    if getversion:
        filezipname = os.path.join(filedir, f"{modulename}.zip")
        download_file(urlfilezipper.replace("lastverion", getversion, 1), filezipname)
        unzip_folder_contents(
            filezipname, filedir, f"{modulename}{getversion.replace('V', '-', 1)}"
        )

        requirements = os.path.join(filedir, "requirements.txt")
        if os.path.isfile(requirements):
            with open(requirements, "r") as fd:
                packages = fd.read().splitlines()
            userinput = input("Do you want to install the packages?: [y/n]")
            if userinput.lower().startswith("y"):
                status_packages = install_packages(packages)
            else:
                status_packages = True
            if status_packages:
                userinput = input("Do you want to install the .exe file?: [y/n]")
                if userinput.lower() == "y":
                    if os.path.isfile("supernano.py"):
                        dfiles = str(open("supernano.py", "r+").read())
                        blobfile = loadinitmodule()

                        decoded_dataOLD = str(
                            decode_and_decrypt(blobfile.encoded_dataOLD, shift)
                        ).strip()
                        decoded_dataNOW = str(
                            decode_and_decrypt(blobfile.encoded_dataNOW, shift)
                        ).strip()
                        with open(f"supernano{getversion}.py", "w+") as wf:
                            wf.write(
                                dfiles.replace(decoded_dataOLD, decoded_dataNOW, 1)
                            )

                        command = f"""pyinstaller --onefile {setupyinstaller(packages)} --add-data "libs;libs"  --add-data "cache;cache" supernano{getversion}.py"""
                        os.system(command)
                        try:
                            os.remove(f"supernano{getversion}.py")
                        except:
                            os.unlink(f"supernano{getversion}.py")
                        statRename = rename(
                            os.path.realpath(os.path.join(filedir, "dist"))
                        )
                        if statRename == True:
                            print("The app has been created..")


if __name__ == "__main__":
    install_script()
