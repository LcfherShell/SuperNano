import os, sys, time, shutil, psutil, inspect, importlib, pkg_resources, pkgutil, json, logging, threading, re

try:
    from .helperegex import (
        searchmissing,
        searching,
        fullmacth,
        rremovelist,
        clean_string,
        rreplace,
        cleanstring,
        split_from_right_with_regex,
    )
    from .cmd_filter import filter_json, safe_load_json
    from .system_manajemen import set_low_priority, SafeProcessExecutor
    from .commandcheck import subprocess
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
            split_from_right_with_regex,
        )
        from cmd_filter import filter_json, safe_load_json
        from system_manajemen import set_low_priority, SafeProcessExecutor
        from commandcheck import subprocess
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
            split_from_right_with_regex,
        )
        from libs.cmd_filter import filter_json, safe_load_json
        from libs.system_manajemen import set_low_priority, SafeProcessExecutor
        from libs.commandcheck import subprocess
        from libs.timeout import timeout_v1, timeout_v2
        from libs.https import Fetch

if __name__ == "__main__":
    set_low_priority(os.getpid())



def removeduplicatejson(my_list:list):
    # Menggunakan dictionary untuk melacak elemen unik
    seen = {}
    for d in my_list:
        key = (d["name"])  # Kunci unik berdasarkan 'name' dan 'age'
        if key not in seen:
            seen[key] = d

    # Mengambil nilai dari dictionary
    unique_list = list(seen.values())
    return list(unique_list)

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
        
        self.languages = {"languages": "PYTHON"}
        self.modules = self.getsys_module()
        self.curents = self.modules
        self.curentpath = sys.path.copy()
        self.modulepathnow = []

    def get_two_level_subfolders(self, root_directory):
        def is_valid_directory(directory_name):
            # Memeriksa apakah nama direktori mengandung spasi atau karakter khusus
            if re.search(r'[ \s@#$%^&*()+=\[\]{};:\'",<>?/\\|`~]', directory_name):
                return False
            return True

        result = []
        for root, dirs, files in os.walk(root_directory):
            # Mendapatkan subfolder pada level pertama
            if root == root_directory:
                result.extend(
                    [
                        resolve_relative_path(root, d).replace("\\", "/")
                        for d in dirs
                        if d.count(" ") == 0 and is_valid_directory(d)
                    ]
                )
            else:
                # Mendapatkan subfolder pada level kedua
                # Hentikan iterasi lebih dalam dengan mengosongkan 'dirs'
                dirs[:] = []
                result.extend(
                    [
                        resolve_relative_path(root, d).replace("\\", "/")
                        for d in dirs
                        if d.count(" ") == 0 and is_valid_directory(d)
                    ]
                )
        if root_directory.replace("\\", "/") not in result:
            result.append(root_directory.replace("\\", "/"))
        return result

    def subprocess(self, filescript: str, file_path: str):
        try:
            result = subprocess.run(
                ["node", resolve_relative_path(all_system_paths[1], filescript), file_path], capture_output=True, text=True
            )

            if result.returncode == 0:
                # Parsing output JSON
                return json.loads(result.stdout)
            else:
                return {}
        except:
            return {}

    ########################NodeJS module
    def get_global_nodejs_modules(self):
        # Menemukan path global `node_modules`
        node_modules_path = os.path.join(
            os.getenv("APPDATA") or "/usr/local", "npm", "node_modules"
        )

        # Mengambil semua modul di direktori
        try:
            self.languages["languages"] = "NODEJS" 
            return [
                module
                for module in os.listdir(node_modules_path)
                if not module.startswith(".")
            ] or None
        except FileNotFoundError:
            return []

    def inspect_nodejs_module(self, module_name):
        try:
            # Path ke node_modules global
            node_modules_path = os.path.join(
                os.getenv("APPDATA") or "/usr/local", "npm", "node_modules"
            )
            module_path = resolve_relative_path(node_modules_path, module_name)

            # Path ke package.json
            package_json_path = os.path.join(module_path, "package.json")
            if not os.path.isfile(package_json_path):
                return None
            # Membaca file package.json
            try:
                with open(package_json_path, "r") as f:
                    package_info = json.load(f)
            except:
                return None
            # Mendapatkan file entry point utama dari package.json
            entry_point = package_info.get("main", "index.js")
            # Path lengkap ke entry point
            index_file_path = resolve_relative_path(module_path, entry_point)

            # Pastikan file tersebut ada
            if not os.path.isfile(index_file_path):
                return None

            result = self.subprocess("ParserNodeModule.js", index_file_path)
            if "module" in result.keys():
                result.update({"module": module_name})
            return result

        except FileNotFoundError:
            return {}

    ###############################################################

    # -------------------------------------------------------------

    ########################Python module
    def getsys_module(self):
        self.languages["languages"] = "PYTHON" 
        return (
            sorted(
                [
                    module.name
                    for module in pkgutil.iter_modules([x for x in sys.path if x])
                    if not module.name.strip().startswith("~")
                    and not module.name.strip().startswith("__pycache__")
                ]
            )
            or None
        )

    def get_python_module(self, paths: list = []):
        def getmodules(path: list, result: list):
            result.extend(
                sorted(
                    [
                        module.name
                        for module in pkgutil.iter_modules(path)
                        if not module.name.strip().startswith("~")
                        and not module.name.strip().startswith("__pycache__")
                    ]
                )
            )

        threads, result = [[], self.curents]
        if paths.__len__() < 1:
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
        return result or None

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

    def get_function_detail(self, module):
        details = []
        try:
            for name, obj in inspect.getmembers(importlib.import_module(module)):
                if inspect.isfunction(obj):
                    func_details = {"name": name, "params": str(inspect.signature(obj))}
                    details.append(func_details)
        except:
            pass
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

    def inspect_python_module(self, module_name: str):
        if self.modulepathnow.__len__() >= 1:
            sys.path.extend(self.modulepathnow)
        self.modulepathnow = []
        try:
            classes = self.list_classes(module_name)
            result = {
                "module": module_name,
                "variables": self.get_global_variables(module_name),
                "classes": [],
                "functions": self.get_function_detail(module_name),
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

    ########################PHP module
    def get_php_module(self, directory: str):
        """Menemukan semua file .php dalam direktori."""
        php_files = []
        directory = directory.replace("\\", "/")
        for folder in self.get_two_level_subfolders(directory):
            for file in os.listdir(folder):
                if os.path.isfile(resolve_relative_path(folder, file)):
                    index_file_path = resolve_relative_path(folder, file).replace(
                        "\\", "/"
                    )
                    if index_file_path.endswith(".php") or index_file_path.endswith(
                        ".phpx"
                    ):
                        modules = [x for x in index_file_path.split(directory) if x]
                        php_files.append(modules[0])
        self.languages["languages"] = "PHP" 
        return php_files or None

    def inspect_php_module(self, file_path: str):
        try:
            result = self.subprocess("ParserPHP.js", file_path)
            if "module" in result.keys():
                head, tail = os.path.split(file_path)
                result.update({"module": tail})
        except:
            result = {}
        return result

    ########################C module
    def get_c_module(self, directory: str):
        """Menemukan semua file .c dan .h dalam direktori."""
        c_files = []
        directory = directory.replace("\\", "/")
        for folder in self.get_two_level_subfolders(directory):
            for file in os.listdir(folder):
                if os.path.isfile(resolve_relative_path(folder, file)):
                    index_file_path = resolve_relative_path(folder, file).replace(
                        "\\", "/"
                    )
                    if (
                        index_file_path.endswith(".c")
                        or index_file_path.endswith(".cpp")
                        or index_file_path.endswith("csx")
                        or index_file_path.endswith(".h")
                    ):
                        modules = [x for x in index_file_path.split(directory) if x]
                        c_files.append(modules[0])
        self.languages["languages"] = "C" 
        return c_files or None

    def inspect_c_module(self, file_path: str):
        # Menyimpan hasil inspeksi
        result = {"classes": [], "functions": [], "variables": []}
        try:
            import clang.cindex

            def get_functions(node):
                """Mengambil informasi tentang fungsi dari node AST."""
                functions = []
                for child in node.get_children():
                    if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                        func_info = {
                            "name": child.spelling,
                            "params": [
                                param.spelling for param in child.get_arguments()
                            ],
                        }
                        functions.append(func_info)
                    elif child.kind == clang.cindex.CursorKind.CXX_METHOD:
                        # Menangani metode dalam kelas (C++)
                        func_info = {
                            "name": child.spelling,
                            "params": [
                                param.spelling for param in child.get_arguments()
                            ],
                        }
                        functions.append(func_info)
                    elif child.kind in [
                        clang.cindex.CursorKind.STRUCT_DECL,
                        clang.cindex.CursorKind.CLASS_DECL,
                    ]:
                        # Menangani struct atau class
                        # Tidak melakukan apa-apa di sini, akan diproses di tempat lain
                        pass
                return functions

            def get_variables(node):
                """Mengambil informasi tentang variabel dari node AST."""
                variables = []
                for child in node.get_children():
                    if child.kind in [
                        clang.cindex.CursorKind.VAR_DECL,
                        clang.cindex.CursorKind.FIELD_DECL,
                    ]:
                        variables.append(child.spelling)
                return variables

            index = clang.cindex.Index.create()
            translation_unit = index.parse(file_path)

            # Menangani fungsi global dan variabel
            result["functions"].extend(get_functions(translation_unit.cursor))
            result["variables"].extend(get_variables(translation_unit.cursor))

            # Menangani struct atau class
            for child in translation_unit.cursor.get_children():
                if child.kind in [
                    clang.cindex.CursorKind.STRUCT_DECL,
                    clang.cindex.CursorKind.CLASS_DECL,
                ]:
                    class_info = {
                        "name": child.spelling,
                        "methods": get_functions(child),
                        "variables": get_variables(child),
                    }
                    result["classes"].append(class_info)
        except:
            with open(file_path, "r+", encoding=sys.getfilesystemencoding()) as f:
                code = f.read()
            # Regex pattern untuk menemukan fungsi dan variabel
            function_pattern = re.compile(
                r"\b[A-Za-z_][A-Za-z_0-9]*\s+\**\s*([A-Za-z_][A-Za-z_0-9]*)\s*\(.*?\)\s*\{",
                re.MULTILINE | re.DOTALL,
            )
            variable_pattern = re.compile(
                r"\b[A-Za-z_][A-Za-z_0-9]*\s+\**\s*([A-Za-z_][A-Za-z_0-9]*)\s*(?=\=|;)",
                re.MULTILINE | re.DOTALL,
            )

            # Regex pattern untuk menemukan struct dan field-nya
            struct_pattern = re.compile(
                r"\bstruct\s+(\w+)\s*\{([^}]*)\};", re.MULTILINE | re.DOTALL
            )
            field_pattern = re.compile(
                r"([a-zA-Z_][a-zA-Z_0-9]*)\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*(?:\[\s*\d*\s*\])?\s*(?:;|,)",
                re.MULTILINE | re.DOTALL,
            )
            try:
                # Menemukan fungsi
                for match in function_pattern.finditer(code):
                    result["functions"].append(
                        {
                            "name": match.group(1),
                            "params": [
                                ""
                            ],  # Parameter tidak diekstrak dalam regex sederhana ini
                        }
                    )
            except:
                function_pattern = re.compile(
                    r"\b[A-Za-z_][A-Za-z_0-9]*\s+\**\s*([A-Za-z_][A-Za-z_0-9]*)\s*\(.*?\)\s*\{",
                    re.MULTILINE | re.DOTALL,
                )
                if function_pattern.finditer(code):
                    for match in function_pattern.finditer(code):
                        result["functions"].append(
                            {
                                "name": match.group(1),
                                "params": [
                                    ""
                                ],  # Parameter tidak diekstrak dalam regex sederhana ini
                            }
                        )
            result["functions"] = removeduplicatejson(result["functions"])
            try:
                # Menemukan variabel
                result["variables"] = [
                    match.group(1) for match in variable_pattern.finditer(code)
                ]
            except:
                variable_pattern = re.compile(
                    r"\b[A-Za-z_][A-Za-z_0-9]*\s+\**\s*([A-Za-z_][A-Za-z_0-9]*)\s*(?=\=|;)",
                    re.MULTILINE | re.DOTALL,
                )

                if variable_pattern.finditer(code):
                    result["variables"] = [
                        match.group(1) for match in variable_pattern.finditer(code)
                    ]
            if result["variables"]:
                result["variables"] = list(set(result["variables"]))
            # Menemukan struct dan field-nya (menganggap struct sebagai class)
            try:
                for match in struct_pattern.finditer(code):
                    struct_name = match.group(1)
                    struct_body = match.group(2)
                    fields = [
                        field_match.group(2)
                        for field_match in field_pattern.finditer(struct_body)
                    ]

                    result["classes"].append(
                        {
                            "name": struct_name,
                            "methods": [
                                ""
                            ],  # Metode tidak diekstrak dalam regex sederhana ini
                            "variables": fields,
                        }
                    )
            except:
                struct_pattern = re.compile(
                    r"\btypedef\s+struct\s+(\w+)\s*\{([^}]*)\}\s*;", re.MULTILINE | re.DOTALL
                )
                field_pattern = re.compile(
                    r"([a-zA-Z_][a-zA-Z_0-9]*)\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*(?:\[\s*\d*\s*\])?\s*(?:;|,)",
                    re.MULTILINE | re.DOTALL,
                )
                if struct_pattern.finditer(code):
                    for match in struct_pattern.finditer(code):
                        struct_name = match.group(1)
                        struct_body = match.group(2)
                        try:
                            fields = [
                                field_match.group(2)
                                for field_match in field_pattern.finditer(struct_body)
                            ]
                        except:
                            fields = []
                        result["classes"].append(
                            {
                                "name": struct_name,
                                "methods": [
                                    ""  # Metode tidak diekstrak dalam regex sederhana ini
                                ],
                                "variables": fields,
                            }
                        )
            result["classes"] = removeduplicatejson(result["classes"])
        if "module" not in result.keys():
            head, tail = os.path.split(file_path)
            result.update({"module": tail})

        return result

    #############path sekarang dari file
    def get_moduleV2(self, pathfiles: str):
        results = None
        paths = os.path.dirname(os.path.abspath(pathfiles))
        _, ext = os.path.splitext(pathfiles)
        self.modulepathnow = [paths]
        try:
            if ext.lower() in (".py", ".pyz", "pyx"):
                results = self.getsys_module()
            elif ext.lower() in (".js", ".ts"):
                results = self.get_global_nodejs_modules()
            elif ext.lower() in (".php", ".phpx"):
                results = self.get_php_module(paths)
            elif ext.lower() in (".c", ".cpp", "csx", ".h"):
                results = self.get_c_module(paths)
            else:
                results = []
        except:
            pass
        _, ext, paths = [None, None, None]
        return results

    def inspect_module(self, module_name: str):
        if self.modulepathnow.__len__() >= 1:
            sys.path.extend(self.modulepathnow)
        _, ext = os.path.splitext(module_name)
        if ext.__len__()==0:
            node_modules_path = os.path.join(
                os.getenv("APPDATA") or "/usr/local", "npm", "node_modules"
            )
            module_path = resolve_relative_path(node_modules_path, module_name)
            if os.path.isdir(module_path):
                inspectModule = self.inspect_nodejs_module(module_name)
            else:
                inspectModule = self.inspect_python_module(module_name)
        else:
            if module_name.startswith("\\"):
                module_name = module_name.replace("\\", "",1)
            elif module_name.startswith("/"):
                module_name = module_name.replace("/", "",1)
            if ext.lower() in (".php", ".phpx"):
                inspectModule = self.inspect_php_module(
                    resolve_relative_path(os.path.join(*self.modulepathnow), module_name)
                )
            elif ext.lower() in (".c", ".cpp", "csx", ".h"):
                inspectModule = self.inspect_c_module(
                    resolve_relative_path(os.path.join(*self.modulepathnow), module_name)
                )
        return inspectModule


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
