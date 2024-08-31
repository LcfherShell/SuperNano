import os, sys, time, shutil, psutil, inspect, importlib, pkg_resources, pkgutil, json, logging, threading

try:
    from .helperegex import (
        searchmissing,
        searching,
        fullmacth,
        rremovelist,
        clean_string,
        rreplace,
        cleanstring,
    )
    from .cmd_filter import filter_json, safe_load_json
    from .system_manajemen import set_low_priority, SafeProcessExecutor
    from .timeout import timeout_v1, timeout_v2
    from .https import Fetch
except:
    try:
        from helperegex import (
            searchmissing,
            searching,
            fullmacth,
            rremovelist,
            clean_string,
            rreplace,
            cleanstring,
        )
        from cmd_filter import filter_json, safe_load_json
        from system_manajemen import set_low_priority, SafeProcessExecutor
        from timeout import timeout_v1, timeout_v2
        from https import Fetch
    except:
        from libs.helperegex import (
            searchmissing,
            searching,
            fullmacth,
            rremovelist,
            clean_string,
            rreplace,
            cleanstring,
        )
        from libs.cmd_filter import filter_json, safe_load_json
        from libs.system_manajemen import set_low_priority, SafeProcessExecutor
        from libs.timeout import timeout_v1, timeout_v2
        from libs.https import Fetch

if __name__ == "__main__":
    set_low_priority(os.getpid())


script_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
all_system_paths = ["/".join(script_dir.split("/")[:-1]), script_dir]


class StreamFile:
    def __init__(self, file_path: str, buffer_size: int = 8192, print_delay: float = 2):
        """
        Inisialisasi StreamFile untuk membaca file baris demi baris dengan delay dan menulis dengan buffer.

        :param file_path: Path ke file yang akan dibaca atau ditulis.
        :param buffer_size: Ukuran buffer sebelum data ditulis ke file.
        :param print_delay: Waktu jeda (dalam detik) antara print setiap baris.
        """
        self.file_path = file_path
        self.buffer_size = buffer_size or 0
        self.print_delay = print_delay
        self.buffer = bytearray()

    def readlines(self):
        """
        Membaca file dengan buffer size dan menghasilkan setiap baris satu per satu dengan delay.

        :yield: Baris dari file.
        """

        with open(self.file_path, "r+") as f:
            buffer = self.buffer
            while True:
                chunk = f.read(self.buffer_size)
                if not chunk:
                    break

                buffer.extend(
                    chunk.encode("utf-8")
                )  # Encode chunk to bytes if necessary

                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    yield line.decode("utf-8")
                    time.sleep(self.print_delay)

            if buffer:
                yield buffer.decode("utf-8")
            self.buffer_size = 0

    def write(self, data):
        """
        Menulis data ke buffer dan secara otomatis menulis ke file ketika buffer penuh.

        :param data: Data yang akan ditulis ke buffer.
        """
        self.buffer.extend(data)
        while len(self.buffer) >= self.buffer_size:
            with open(self.file_path, "ab+") as f:
                f.write(self.buffer[: self.buffer_size])
            self.buffer = self.buffer[self.buffer_size :]

    def writelines(self, lines):
        """
        Menulis baris-baris data ke file dengan delay antara setiap baris.

        :param lines: List atau generator yang menghasilkan baris-baris data untuk ditulis.
        """
        for line in lines:
            self.write(line.encode("utf-8"))
            time.sleep(self.print_delay + timeout_v1())
        self.close()  # Memastikan buffer ditulis dan ditutup setelah penulisan selesai

    def eraseFile(self):
        with open(self.file_path, "rb+") as f:
            f.truncate(0)

    def close(self):
        """
        Menulis sisa data di buffer ke file dan membersihkan buffer.
        """
        if self.buffer and self.buffer_size:
            with open(self.file_path, "ab+") as f:
                f.write(self.buffer)
            self.buffer.clear()
        else:
            pass


class ModuleInspector:
    def __init__(self):
        self.modules = self.getsys_module()
        self.curents = self.modules
        self.curentpath = sys.path.copy()
        self.modulepathnow = []

    def getsys_module(self):
        return sorted(
            [
                    module.name
                    for module in pkgutil.iter_modules([x for x in sys.path if x])
                    if not module.name.strip().startswith("~")
                    and not module.name.strip().startswith("__pycache__")
            ]
        )
        
    def get_module(self, paths:list=[]):
        def getmodules(path:list, result:list):
            result.extend(sorted(
                [
                    module.name
                    for module in pkgutil.iter_modules(path)
                    if not module.name.strip().startswith("~")
                    and not module.name.strip().startswith("__pycache__")
                ]
            ))

        threads, result = [[], self.curents]
        if paths.__len__()<1:
                paths = [os.getcwd()]
        else:
            pass
        

        for path in paths:
            thread = threading.Thread(target=getmodules, args=([path], result))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.modulepathnow = paths
        return result
        

    def list_classes(self, module):
        try:
            imported_module = importlib.import_module(module)
            classes = [
                obj
                for name, obj in inspect.getmembers(imported_module)
                if inspect.isclass(obj)
            ]
            if not classes:
                pass
            return classes
        except Exception as e:
            return []

    def get_class_details(self, cls):
        details = {"name": cls.__name__, "variables": [], "functions": []}

        for name, obj in inspect.getmembers(cls):
            if inspect.isfunction(obj):
                func_details = {"name": name, "params": str(inspect.signature(obj))}
                details["functions"].append(func_details)
            elif not name.startswith("__") and not inspect.ismodule(obj):
                details["variables"].append(name)

        return details

    def get_global_variables(self, module):
        try:
            imported_module = importlib.import_module(module)
            # global_vars = {name: self.serialize_value(value) for name, value in vars(imported_module).items()
            #               if not (inspect.isclass(value) or inspect.isfunction(value)) and not name.startswith('__')}
            global_vars = [
                name
                for name, value in vars(imported_module).items()
                if not (inspect.isclass(value) or inspect.isfunction(value))
                and not name.startswith("__")
            ]
            return global_vars
        except Exception as e:
            return []

    def serialize_value(self, value):
        """Serialize values for JSON compatibility."""
        if isinstance(value, (int, float, str, bool, list, dict)):
            return value
        elif callable(value):
            return f"Function: {value.__name__}"
        else:
            return str(value)  # Convert other types to string

    def inspect_module(self, module_name):
        if self.modulepathnow.__len__()>=1:
            sys.path.extend(self.modulepathnow)
        self.modulepathnow = []
        try:
            classes = self.list_classes(module_name)
            global_vars = self.get_global_variables(module_name)
            result = {
                "module": module_name,
                "global_variables": global_vars,
                "classes": [],
            }

            for cls in classes:
                class_details = self.get_class_details(cls)
                result["classes"].append(class_details)

            # Convert the result to JSON and print it

            sys.path = self.curentpath
            return result
        except Exception as e:
            sys.path = self.curentpath
            return None


def create_file_or_folder(path: str) -> str:
    """
    Membuat file atau folder di path yang diberikan.

    Args:
        path (str): Path lengkap tempat file atau folder akan dibuat.

    Returns:
        str: Pesan konfirmasi yang menunjukkan apakah file atau folder berhasil dibuat.
    """

    if not path:
        return "Path is empty."

    if os.path.isdir(path):
        return f"The folder '{os.path.basename(path)}' already exists."

    if os.path.isfile(path):
        return f"The file '{os.path.basename(path)}' already exists."

    folder, filename = os.path.split(path)
    if "." in os.path.basename(path) and os.path.exists(folder):
        # Membuat file
        try:
            if folder and not os.path.exists(folder):
                return f"Failed to create the file '{filename}'"
            with open(path, "wb") as f:
                pass  # Membuat file kosong
            return f"The file '{filename}' has been successfully created."
        except Exception as e:
            return f"Failed to create the file '{filename}'"
    elif os.path.exists(folder) and folder:
        # Membuat folder
        try:
            os.makedirs(path)
            return (
                f"The folder '{os.path.basename(path)}' has been successfully created."
            )
        except FileExistsError:
            return f"The folder '{os.path.basename(path)}' already exists."
        except Exception as e:
            return f"Failed to create the folder '{os.path.basename(path)}'."
    else:
        return "Something happened."


def is_binary_file(file_path):
    """
    Menentukan apakah file adalah file biner atau bukan.

    Args:
        file_path (str): Path ke file yang akan diperiksa.

    Returns:
        bool: True jika file adalah file biner, False jika bukan.
    """
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(1024)  # Membaca bagian pertama file (1KB)
            # Cek apakah file memiliki karakter yang tidak biasa untuk teks
            if b"\0" in chunk:  # Null byte adalah indikator umum dari file biner
                return True
            # Cek apakah file sebagian besar berisi karakter teks (misalnya ASCII)
            text_chars = b"".join([bytes((i,)) for i in range(32, 127)]) + b"\n\r\t\b"
            non_text_chars = chunk.translate(None, text_chars)
            if (
                len(non_text_chars) / len(chunk) > 0.30
            ):  # Jika lebih dari 30% karakter non-teks
                return True
        return False
    except Exception as e:
        return False

def is_binary_file(file_path):
    """
    Menentukan apakah file adalah file biner atau bukan.

    Args:
        file_path (str): Path ke file yang akan diperiksa.

    Returns:
        bool: True jika file adalah file biner, False jika bukan.
    """
    try:
        with open(file_path, "rb+") as file:
            chunk = file.read(1024)  # Membaca bagian pertama file (1KB)
            # Cek apakah file memiliki karakter yang tidak biasa untuk teks
            if b"\0" in chunk:  # Null byte adalah indikator umum dari file biner
                return True
            # Cek apakah file sebagian besar berisi karakter teks (misalnya ASCII)
            text_chars = b"".join([bytes((i,)) for i in range(32, 127)]) + b"\n\r\t\b"
            non_text_chars = chunk.translate(None, text_chars)
            if (
                len(non_text_chars) / len(chunk) > 0.30
            ):  # Jika lebih dari 30% karakter non-teks
                return True
        return False
    except Exception as e:
        return False


def is_binary_file(file_path):
    """
    Menentukan apakah file adalah file biner atau bukan.

    Args:
        file_path (str): Path ke file yang akan diperiksa.

    Returns:
        bool: True jika file adalah file biner, False jika bukan.
    """
    try:
        with open(file_path, "rb+") as file:
            chunk = file.read(1024)  # Membaca bagian pertama file (1KB)
            # Cek apakah file memiliki karakter yang tidak biasa untuk teks
            if b"\0" in chunk:  # Null byte adalah indikator umum dari file biner
                return True
            # Cek apakah file sebagian besar berisi karakter teks (misalnya ASCII)
            text_chars = b"".join([bytes((i,)) for i in range(32, 127)]) + b"\n\r\t\b"
            non_text_chars = chunk.translate(None, text_chars)
            if (
                len(non_text_chars) / len(chunk) > 0.30
            ):  # Jika lebih dari 30% karakter non-teks
                return True
        return False
    except Exception as e:
        return False


def check_class_in_package(package_name, class_name):
    try:
        # Import the package
        package = importlib.import_module(package_name)
        # Cek apakah kelas ada di dalam modul
        if hasattr(package, class_name):
            cls = getattr(package, class_name)
            # Pastikan itu adalah kelas, bukan atribut atau fungsi
            if inspect.isclass(cls):
                return True, "ClassFound"
        return False, "ClassNotFound"
    except ModuleNotFoundError:
        return False, "ModuleNotFoundError"


def resolve_relative_path(current_path: str, relative_path: str) -> str:
    # Menggabungkan current_path dengan relative_path (misalnya "../")
    target_path: str = os.path.normpath(os.path.join(current_path, relative_path))
    return target_path


def resolve_relative_path_v2(path: str) -> str:
    target_folder: str = resolve_relative_path(
        os.getcwd().replace("\\", "/"), path.replace("\\", "/")
    )
    return target_folder


def get_latest_version(package_name):
    with Fetch() as req:
        response = req.get(
            f"https://pypi.org/pypi/{package_name}/json",
            max_retries=3,
            timeout=8,
            follow_redirects=True,
        )
    data = response.json()
    if filter_json(data=data, keys=["info"]):
        return data["info"]["version"]
    return None


def check_update(package_name):
    installed_version = pkg_resources.get_distribution(package_name).version
    latest_version = get_latest_version(package_name)

    if installed_version != latest_version:
        print(
            f"Package {package_name} can be updated from version {installed_version} to {latest_version}."
        )
    else:
        print(f"Package {package_name} is up to date.")

