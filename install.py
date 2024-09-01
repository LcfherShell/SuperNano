import os, sys, time, re
import subprocess
import requests as api_requests
import zipfile


username, modulename, filedir = "LcfherShell", "SuperNano", os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
urlgitversion = f"https://api.github.com/repos/{username}/{modulename}/branches"
urlfilezipper = f"https://github.com/{username}/{modulename}/archive/refs/heads/lastverion.zip"

def search_like_regex(data_list, pattern):
    """ Mencari elemen dalam daftar yang cocok dengan pola regex. """
    regex = re.compile(pattern, re.IGNORECASE)
    return [item for item in data_list if regex.search(item)]

def install_packages(packages:list):
    """ Menginstal beberapa paket Python menggunakan pip. """
    len_pkg:int = packages.__len__()
    for pkg in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
            print(f"Packages {pkg} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during package installation: {pkg}")
            len_pkg-=1
        except Exception as e:
            print(f"General error during package installation: {pkg}")
            len_pkg-=1
    if len_pkg<packages.__len__():
        return False
    return True

def module_version():
    """ Mendapatkan semua versi modul dari GitHub. """
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

def download_file(url:str, local_filename:str):
    """ Mengunduh file dari URL dengan retry jika terjadi kegagalan. """
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

        print(f"Contents of folder '{folder_name}' successfully extracted to: {extract_to}")


def install_script():
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
            if session<=0:
                return
            session-=1
        print("No valid version selected.")
    
    if getversion:
        filezipname = os.path.join(filedir, f"{modulename}.zip")
        download_file(urlfilezipper.replace("lastverion", getversion, 1), filezipname)
        unzip_folder_contents(filezipname, filedir, f"{modulename}{getversion.replace('V', '-', 1)}")
        
        requirements = os.path.join(filedir, "requirements.txt")
        if os.path.isfile(requirements):
            with open(requirements, "r") as fd:
                packages = fd.read().splitlines()
            install_packages(packages)

if __name__ == "__main__":
    install_script()
