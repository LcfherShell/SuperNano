import urwid

import pyperclip

import os, sys, shutil, logging, time, threading, argparse

from datetime import datetime


try:
    from libs.helperegex import findpositions, rreplace

    from libs.titlecommand import get_console_title, set_console_title

    from libs.cmd_filter import shorten_path, validate_folder

    from libs.errrorHandler import complex_handle_errors

    from libs.system_manajemen import set_low_priority, SafeProcessExecutor

    from libs.timeout import timeout_v2, timeout_v1

    from libs.filemanager import (
        StreamFile,
        ModuleInspector,
        read_file_in_chunks,
        validate_file,
        isvalidate_folder,
        isvalidate_filename,
        create_file_or_folder,
        resolve_relative_path_v2,
        resolve_relative_path,
        all_system_paths,
    )

except:
    try:
        from .helperegex import findpositions, rreplace

        from .titlecommand import get_console_title, set_console_title

        from .cmd_filter import shorten_path, validate_folder

        from .errrorHandler import complex_handle_errors

        from .system_manajemen import set_low_priority, SafeProcessExecutor

        from .timeout import timeout_v2, timeout_v1

        from .filemanager import (
            StreamFile,
            ModuleInspector,
            read_file_in_chunks,
            validate_file,
            isvalidate_folder,
            isvalidate_filename,
            create_file_or_folder,
            resolve_relative_path_v2,
            resolve_relative_path,
            all_system_paths,
        )

    except:
        from helperegex import findpositions, rreplace

        from titlecommand import get_console_title, set_console_title

        from cmd_filter import shorten_path, validate_folder

        from errrorHandler import complex_handle_errors

        from system_manajemen import set_low_priority, SafeProcessExecutor

        from timeout import timeout_v2, timeout_v1

        from filemanager import (
            StreamFile,
            ModuleInspector,
            read_file_in_chunks,
            validate_file,
            isvalidate_folder,
            isvalidate_filename,
            create_file_or_folder,
            resolve_relative_path_v2,
            resolve_relative_path,
            all_system_paths,
        )


set_low_priority(os.getpid())

#########mendapatkan process terbaik tanpa membebani ram dan cpu

thisfolder, _x = all_system_paths

__version__ = "2.2.1"


fileloogiing = os.path.join(thisfolder, "cache", "file_browser.log").replace("\\", "/")


if not os.path.isfile(fileloogiing):
    open(fileloogiing, "a+")

elif os.path.getsize(fileloogiing) > 0:
    with open(fileloogiing, "wb+") as f:
        f.truncate(0)


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=fileloogiing,
    filemode="w",
    encoding=sys.getfilesystemencoding(),
    format="%(asctime)s, %(msecs)d %(name)s %(levelname)s [ %(filename)s-%(module)s-%(lineno)d ]  : %(message)s",
    datefmt="%H:%M:%S",
    level=logging.ERROR,
)

logging.getLogger("urwid").disabled = True

logger = logging.getLogger("urwid")

for handler in logger.handlers[:]:
    logger.removeHandler(handler)


def setTitle(title: str):
    """

    Fungsi setTitle bertugas untuk mengatur judul konsol (console title) berdasarkan parameter title yang diberikan.\n

    Jika inputan title memiliki panjang lebih dari 30 karakter maka potong karakternya

    """

    process = title

    Getitles = get_console_title()

    if os.path.isdir(process) or os.path.isfile(process):
        length = int(process.__len__() / 2)

        if length < 28:
            x = process.__len__()

            nexts = int(50 - x) - (x / 2)

            if nexts < 28:
                length = int((28 - nexts) + nexts)

            else:
                length = nexts

        elif length > 50:
            length = 28

        process = shorten_path(process, length)

    if Getitles.startswith("Win-SuperNano"):
        output = str("Win-SuperNano {titles}".format(titles=process))

    else:
        output = title

    set_console_title(output)


@complex_handle_errors(loggering=logging, nomessagesNormal=False)
def parse_args():
    """

    Fungsi parse_args bertugas untuk mendapatkan\menangkap argument konsol (console title) yang diberikan oleh user.\n

    """

    parser = argparse.ArgumentParser(
        description="An extension on nano for editing directories in CLI."
    )

    parser.add_argument(
        "path",
        default=os.path.split(thisfolder)[0],
        nargs="?",
        type=str,
        help="Target file or directory to edit.",
    )

    args = parser.parse_args()

    path = resolve_relative_path(args.path, "") or "."

    if os.path.exists(path):
        if validate_folder(path=path):
            pass

        else:
            logging.error(f"ERROR - {path} path cannot access")

            exit()

    else:
        logging.error(f"ERROR - {path} path does not exist")

        exit()

    return resolve_relative_path_v2(path).replace("\\", "/")


class PlainButton(urwid.Button):

    """

    Class PlainButton bertugas untuk mengkoustomisasi button dan menghilangkan karakter < dan >.\n

    """

    button_left = urwid.Text("")

    button_right = urwid.Text("")


class FileButton(PlainButton):
    def __init__(self, label, functions, file_path):
        super().__init__(label)

        self.file_path = file_path

        self.functions = functions

        urwid.connect_signal(
            self, "click", self.on_single_click, user_args=self.file_path
        )

    def on_single_click(self, button, user_data=None):
        time.sleep(0.02)

        if (
            not self.get_label()
            .lower()
            .endswith(
                (
                    ".bin",
                    ".exe",
                    ".dat",
                    ".dll",
                    ".flt",
                    ".xbin",
                    ".x",
                    ".bmp",
                    ".rpm",
                    ".xz",
                    ".iso",
                    ".zst",
                    ".appimage",
                    ".apk",
                    ".msi",
                    ".apx",
                    ".app",
                    ".apps",
                    ".cmd",
                    ".run",
                    ".deb",
                    ".dmg",
                    ".ipa",
                )
            )
        ):
            self.functions(button, user_data)  # Buka file jika single-click

        else:
            self.functions(button, None)


class NumberedEdit(urwid.WidgetWrap):
    def __init__(self, edit_text="", multiline=True):
        self.edit = urwid.Edit(edit_text, multiline=multiline)

        self.line_numbers = urwid.Text("")

        self.update_line_numbers()

        columns = urwid.Columns([("fixed", 4, self.line_numbers), self.edit])

        super().__init__(urwid.AttrMap(columns, None, focus_map="reversed"))

        # Connect the 'change' signal from the internal Edit widget

        urwid.connect_signal(self.edit, "change", self._on_change)

    def update_line_numbers(self):
        text = self.edit.get_edit_text()

        lines = text.splitlines()

        line_numbers = "\n".join([f"{i+1:>3}" for i in range(len(lines))])

        self.line_numbers.set_text(line_numbers)

    def keypress(self, size, key):
        key = super().keypress(size, key)

        self.update_line_numbers()

        return key

    def mouse_event(self, size, event, button, col, row, focus):
        handled = super().mouse_event(size, event, button, col, row, focus)

        if handled:
            self.update_line_numbers()

        return handled

    def _on_change(self, edit, new_text):
        self.update_line_numbers()

        urwid.emit_signal(self, "change", self, new_text)

    def set_edit_text(self, text):
        """Set the text of the edit widget and update line numbers."""

        self.edit.set_edit_text(text)

        self.update_line_numbers()

    def get_edit_text(self):
        """Get the text from the edit widget."""

        return self.edit.get_edit_text()


class SaveableEdit(urwid.Edit):
    signals = ["save"]

    def keypress(self, size, key):
        if key == "enter":
            # Emit the 'save' signal with the current text
            urwid.emit_signal(self, "save", self.get_edit_text())
            return True
        return super().keypress(size, key)


urwid.register_signal(NumberedEdit, ["change"])


class SuperNano:

    """

    Kelas SuperNano yang sedang Anda kembangkan adalah text editor berbasis console yang menggunakan Python 3.6 ke atas dengan dukungan urwid[curses].

    Pembuat: Ramsyan Tungga Kiansantang (ID)  |  Github: LcfherShell

    Tanggal dibuat: 21 Agustus 2024

    Jika ada bug silahkan kunjungi git yang telah tertera diatas

    """

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def __init__(self, start_path="."):
        "Mengatur path awal, judul aplikasi, widget, dan layout utama. Juga mengatur alarm untuk memuat menu utama dan memulai loop aplikasi."

        self.current_path = start_path

        self.current_pathx = self.current_path

        self.current_file_name = None  # Track current file name

        self.undo_stack, self.redo_stack = [[], []]  # Stack for undo  # Stack for redo

        self.overlay_POPUP = None  # Overlay untuk popup

        self.module_package_Python = ModuleInspector()  # memuat module python

        self.module_package_PythonC = self.module_package_Python.curents

        # Set title

        setTitle("Win-SuperNano v{version}".format(version=__version__))

        # Create widgets

        """

        1.loading menu 

        2. main menu: search, list file or folder, and inspect module python

        """

        ######Create widgets modulepython menu

        def create_button(module_name):
            button = PlainButton(module_name)

            urwid.connect_signal(button, "click", self.inspect_module, module_name)

            return urwid.AttrMap(button, None, focus_map="reversed")

        self.listmodules_from_package_Python = urwid.SimpleFocusListWalker(
            [
                create_button(module)
                for module in self.module_package_Python.get_python_module(sys.path)
            ]
        )

        # Footer text and ListBox for scrolling

        self.Text_Deinspect_modules_from_package_Python = urwid.Text(
            "Select a module to inspect."
        )

        MenuText_Inspect_modules_from_package_Python = urwid.ListBox(
            urwid.SimpleFocusListWalker(
                [self.Text_Deinspect_modules_from_package_Python]
            )
        )

        Box_Deinspect_modules_from_package_Python = urwid.BoxAdapter(
            MenuText_Inspect_modules_from_package_Python, 14
        )  # Set max height for the footer

        # Use a Frame to wrap the main content and footer

        self.Inspect_modules_from_package_Python = urwid.Frame(
            body=urwid.LineBox(
                urwid.ListBox(self.listmodules_from_package_Python),
                title="Python Modules",
            ),
            footer=Box_Deinspect_modules_from_package_Python,
        )

        ###Create widgets loading menu

        self.title_loading_widget = urwid.Text(
            "Win-SuperNano v{version} CopyRight: LcfherShell@{year}\n".format(
                version=__version__, year=datetime.now().year
            ),
            align="center",
        )

        self.loading_widget = urwid.Text("Loading, please wait...", align="center")

        self.main_layout = urwid.Filler(
            urwid.Pile([self.title_loading_widget, self.loading_widget]),
            valign="middle",
        )

        # Create main menu

        self.main_menu_columns = urwid.Columns([])

        self.main_menu_pile = urwid.Pile([self.main_menu_columns])

        self.status_msg_footer_text = urwid.Text(
            "Press ctrl + q to exit, Arrow keys to navigate"
        )

        self.main_footer_text = urwid.Text(
            "Ctrl+S : Save file    Ctrl+D : Delete File    Ctrl+Z : Undo Edit    Ctrl+Y : Redo Edit    Ctrl+E : Redirect input   Ctrl+R : Refresh UI    ESC: Quit "
        )

        # Event loop

        self.loop = urwid.MainLoop(self.main_layout, unhandled_input=self.handle_input)

        self.loading_alarm = self.loop.set_alarm_in(
            round(timeout_v1() * timeout_v2(), 1) + 1,
            lambda loop, user_data: self.load_main_menu(),
        )

        self.system_alarm = None

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def load_main_menu(self):
        "Menyiapkan dan menampilkan menu utama setelah periode loading, dan menghapus alarm loading."

        # self.loading_widget.set_text("Press key R")

        set_low_priority(os.getpid())

        self.loop.remove_alarm(self.loading_alarm)  # Hentikan alarm

        self.loading_alarm = None

        self.switch_to_secondary_layout()

    def switch_to_secondary_layout(self):
        "Mengubah layout aplikasi ke menu utama yang telah disiapkan."

        self.setup_main_menu()

        if self.loading_alarm != None:
            self.loop.remove_alarm(
                self.loading_alarm
            )  # Hentikan alarm loading jika masih ada

            self.loading_alarm = None

        self.loop.widget = self.main_layout

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def setup_main_menu(self):
        "Menyiapkan dan mengatur widget untuk menu utama, termasuk daftar file, editor teks, dan tombol-tombol fungsional. Mengatur layout untuk tampilan aplikasi."

        # Define widgets

        self.file_list = urwid.SimpleFocusListWalker(self.get_file_list())

        self.file_list_box = urwid.ListBox(self.file_list)

        self.text_editor = NumberedEdit(multiline=True)

        self.current_focus = 0  # 0 for textbox1, 1 for textbox2

        # Wrap text_editor with BoxAdapter for scrollable content

        self.text_editor_scrollable = urwid.LineBox(
            urwid.Filler(self.text_editor, valign="top"), title="TextBox"
        )

        # Define menu widgets

        self.quit_button = PlainButton("Quit", align="center")

        urwid.connect_signal(self.quit_button, "click", self.quit_app)

        self.search_edit = urwid.Edit(
            "Search, Rename or Create: ", multiline=False, align="left"
        )

        search_limited = urwid.BoxAdapter(
            urwid.Filler(self.search_edit, valign="top"), height=1
        )

        self.search_button = PlainButton("Execute", align="center")

        urwid.connect_signal(self.search_button, "click", self.in_search_)

        padded_button = urwid.Padding(
            self.search_button, align="center", width=("relative", 50)
        )  # Tombol berada di tengah dengan lebar 50% dari total layar

        padded_button = urwid.AttrMap(
            padded_button, None, focus_map="reversed"
        )  # Mengatur warna saat tombol difokuskan

        urwid.connect_signal(
            self.text_editor.base_widget, "change", self.set_focus_on_click, 0
        )

        urwid.connect_signal(
            self.search_edit.base_widget, "change", self.set_focus_on_click, 1
        )

        # Menu layout

        self.main_menu_columns = urwid.Columns(
            [
                (
                    "weight",
                    3,
                    urwid.AttrMap(search_limited, None, focus_map="reversed"),
                ),
                (
                    "weight",
                    1,
                    urwid.AttrMap(padded_button, None, focus_map="reversed"),
                ),
                (
                    "weight",
                    2,
                    urwid.AttrMap(self.quit_button, None, focus_map="reversed"),
                ),
                # (
                #    "weight",
                #    4,
                #    urwid.AttrMap(urwid.Pile(menu_items), None, focus_map="reversed"),
                # ),
            ]
        )

        self.main_menu_pile = urwid.Pile([self.main_menu_columns])

        # Layout

        self.main_layout = urwid.Frame(
            header=self.main_menu_pile,
            body=urwid.Columns(
                [
                    (
                        "weight",
                        1,
                        urwid.LineBox(self.file_list_box, title="Directory Files"),
                    ),
                    (
                        "weight",
                        1,
                        urwid.AttrMap(
                            self.Inspect_modules_from_package_Python,
                            None,
                            focus_map="reversed",
                        ),
                    ),
                    (
                        "weight",
                        3,
                        self.text_editor_scrollable,
                    ),
                ]
            ),
            footer=urwid.Pile([self.status_msg_footer_text, self.main_footer_text]),
        )

        self.loop.set_alarm_in(timeout_v2(), self.update_uiV2)

        self.system_alarm = self.loop.set_alarm_in(
            timeout_v2() + 1,
            lambda loop, user_data: self.system_usage(),
        )
        try:
            urwid.TrustedLoop(self.loop).set_widget(self.main_layout)
        except:
            self.loop.widget = self.main_layout

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def create_modules_menus(self, listmodulename: list):
        def create_button(module_name):
            button = PlainButton(module_name)

            urwid.connect_signal(button, "click", self.inspect_module, module_name)

            return urwid.AttrMap(button, None, focus_map="reversed")

        return [create_button(module) for module in listmodulename]

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def inspect_module(self, button, module_name):
        result = self.module_package_Python.inspect_module(module_name)

        if result:
            if "module" in result.keys():
                keys = result.keys()

                if "classes" in keys or "functions" in keys or "variables" in keys:
                    result_text = f"Module: {result['module']}\n\nGlobal Variables:\n"

                    result_text += ", ".join(result["variables"])

                    if result["classes"]:
                        result_text += "\n\nClass:\n"

                        for cls in result["classes"]:
                            if cls["name"]:
                                result_text += f"Class: {cls['name']}\n"

                                result_text += "  Variables:\n"

                                result_text += (
                                    "  " + "\n > ".join(cls["variables"]) + "\n\n"
                                )

                                if cls["functions"]:
                                    result_text += "  Function:\n"

                                    for func in cls["functions"]:
                                        result_text += (
                                            f" > {func['name']}{func['params']}\n\n"
                                        )

                    for funcs in result["functions"]:
                        if funcs["name"]:
                            result_text += f"\nFunction: {funcs['name']}\n"

                            result_text += f" > {funcs['name']}{funcs['params']}\n\n"

                    self.Text_Deinspect_modules_from_package_Python.set_text(
                        result_text
                    )

        else:
            self.Text_Deinspect_modules_from_package_Python.set_text(
                "Error inspecting module."
            )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def setup_popup(self, options, title, descrip: str = ""):
        "Menyiapkan konten dan layout untuk menu popup dengan judul, deskripsi, dan opsi yang diberikan."

        # Konten popup

        menu_items = []

        if descrip:
            menu_items = [urwid.Text(descrip, align="center"), urwid.Divider("-")]

        # Tambahkan opsi ke dalam menu popup

        for option in options:
            menu_items.append(option)

        # Tambahkan tombol untuk menutup popup

        menu_items.append(PlainButton("Close", on_press=self.close_popup))

        # Buat listbox dari opsi yang sudah ada

        popup_content = urwid.ListBox(urwid.SimpleFocusListWalker(menu_items))

        # Tambahkan border dengan judul

        self.popup = urwid.LineBox(popup_content, title=title)

    def on_option_selected(self, button):
        "Menangani pilihan opsi dari popup dengan menutup popup dan mengembalikan label opsi yang dipilih."

        urwid.emit_signal(button, "click")

        getbutton = button.get_label()

        self.close_popup(None)

        return getbutton

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def show_popup(self, title: str, descrip: str, menus: list):
        "Menampilkan popup menu dengan judul, deskripsi, dan daftar opsi yang diberikan."

        # Siapkan popup dengan judul, descrip, dan opsi

        self.setup_popup(title=title, descrip=descrip, options=menus)

        # Tentukan ukuran dan posisi popup

        popup_width = 35

        popup_height = 25

        self.overlay_POPUP = urwid.Overlay(
            self.popup,
            self.main_layout,
            "center",
            ("relative", popup_width),
            "middle",
            ("relative", popup_height),
        )

        self.loop.widget = self.overlay_POPUP

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def close_popup(self, button):
        "Menutup popup menu dan mengembalikan tampilan ke layout utama."

        self.overlay_POPUP = None

        self.loop.widget = self.main_layout

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def get_file_list(self):
        "Mengambil daftar file dan direktori di path saat ini, termasuk opsi untuk naik satu level di direktori jika bukan di direktori root."

        files = []

        if self.current_path != ".":  # Cek apakah bukan di direktori root
            button = PlainButton("...")

            urwid.connect_signal(button, "click", self.go_up_directory)

            files.append(urwid.AttrMap(button, None, focus_map="reversed"))

        for f in os.listdir(f"{self.current_path}"):
            if os.path.isdir(resolve_relative_path(self.current_path, f)):
                f = f + "/"

            button = PlainButton(f)

            urwid.connect_signal(button, "click", self.open_file, f)

            files.append(urwid.AttrMap(button, None, focus_map="reversed"))

        return files

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def renameORcreatedPOP(self):
        select = urwid.Edit("Search or Create", "")
        replaces = SaveableEdit("Replace         ", "")

        def on_save(button, *args):
            slect = select.get_edit_text().strip()
            if slect.__len__() <= 0:
                return
            getselect = [f for f in os.listdir(f"{self.current_path}") if slect in f]
            if getselect and replaces.get_edit_text():
                _y = replaces.get_edit_text().strip()
                if isvalidate_folder(_y):
                    try:
                        selecfolder = resolve_relative_path(
                            self.current_path, getselect[0]
                        )
                        selecrepcae = resolve_relative_path(self.current_path, _y)
                        if os.path.isdir(selecfolder) or os.path.isfile(selecfolder):
                            os.rename(selecfolder, selecrepcae)
                        ms = str(f"Success renaming item")
                    except:
                        ms = str(f"Failed renaming item: {getselect[0]}")
                else:
                    ms = str("Item to rename not found")
            else:
                x, _y = os.path.split(slect)
                if os.path.isdir(x):
                    ms = str("Item to rename not found")
                else:
                    if isvalidate_folder(_y) or _y.find(".") == -1:
                        ms = create_file_or_folder(
                            resolve_relative_path(self.current_path, slect)
                        )
                    elif isvalidate_filename(_y) or _y.find(".") > 0:
                        ms = create_file_or_folder(
                            resolve_relative_path(self.current_path, slect)
                        )
                    else:
                        ms = str("Item to rename not found")

            self.switch_to_secondary_layout()
            self.status_msg_footer_text.set_text(ms)

        urwid.connect_signal(replaces, "save", on_save)
        return [select, replaces]

    def handle_input(self, key):
        "Menangani input keyboard dari pengguna untuk berbagai tindakan seperti keluar, menyimpan, menghapus, undo, redo, copy, paste, dan refresh UI."

        if key in ("ctrl q", "ctrl Q", "esc"):
            self.show_popup(
                menus=[PlainButton("OK", on_press=lambda _x: self.quit_app())],
                title="Confirm Quit",
                descrip="Are you sure you Quit",
            )

        elif key in ("ctrl n", "ctrl N"):
            self.show_popup(
                menus=[*self.renameORcreatedPOP()],
                title="Rename or Create",
                descrip="AChoose to rename an existing item or create a new one in the current directory. Press ENter to done",
            )

        elif key in ("ctrl s", "ctrl S"):
            # self.save_file()

            self.show_popup(
                menus=[
                    PlainButton(
                        "OK",
                        on_press=lambda _x: self.close_popup(None)
                        if self.save_file()
                        else None,
                    )
                ],
                title="Save File",
                descrip="Are you sure you want to save the file changes",
            )

        elif key in ("ctrl d", "ctrl D"):
            self.show_popup(
                menus=[
                    PlainButton(
                        "OK",
                        on_press=lambda _x: self.close_popup(None)
                        if self.delete_file()
                        else None,
                    )
                ],
                title="Delete File",
                descrip="Are you sure you want to delete the file",
            )

        elif key in ("ctrl z", "ctrl Z"):
            self.undo_edit()

        elif key in ("ctrl y", "ctrl Y"):
            self.redo_edit()

        elif key in ("ctrl c", "ctrl C"):
            self.copy_text_to_clipboard()

        elif key in ("ctrl v", "ctrl V"):
            self.paste_text_from_clipboard()

        elif key in ("ctrl r", "ctrl R"):
            self.switch_to_secondary_layout()

        elif key in ("f1", "ctrl e", "ctrl E"):
            self.current_focus = 1 if self.current_focus == 0 else 0

            self.status_msg_footer_text.set_text(f"focus {self.current_focus}")

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def get_current_edit(self):
        "Mengembalikan widget edit yang sedang difokuskan (text editor atau search edit)."

        if self.current_focus == 0:
            return self.text_editor.edit.base_widget

        elif self.current_focus == 1:
            return self.search_edit.base_widget

        return None

    def set_focus_on_click(self, widget, new_edit_text, index):
        "Mengatur fokus pada widget edit berdasarkan klik dan indeks."

        self.current_focus = index

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def copy_text_to_clipboard(self):
        "Menyalin teks dari widget edit yang sedang aktif ke clipboard."

        current_edit = self.get_current_edit()

        if current_edit:
            if hasattr(current_edit, "edit_pos") and hasattr(
                current_edit, "get_edit_text"
            ):
                self.status_msg_footer_text.set_text("Text copied to clipboard.")

                cursor_position = current_edit.edit_pos

                pyperclip.copy(
                    current_edit.get_edit_text()[cursor_position:]
                    or current_edit.get_edit_text()
                )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def paste_text_from_clipboard(self):
        "Menempelkan teks dari clipboard ke widget edit yang sedang aktif."

        pasted_text = pyperclip.paste()  # Mengambil teks dari clipboard

        current_edit = self.get_current_edit()

        if current_edit:
            if hasattr(current_edit, "edit_pos") and hasattr(
                current_edit, "get_edit_text"
            ):
                current_text = (
                    current_edit.get_edit_text()
                )  # Mendapatkan teks saat ini di widget Edit

                cursor_position = (
                    current_edit.edit_pos
                )  # Mendapatkan posisi kursor saat ini

                # Membagi teks berdasarkan posisi kursor

                text_before_cursor = current_text[:cursor_position]

                text_after_cursor = current_text[cursor_position:]

                # Gabungkan teks sebelum kursor, teks yang ditempelkan, dan teks setelah kursor

                new_text = text_before_cursor + pasted_text + text_after_cursor

                # Set teks baru dan sesuaikan posisi kursor

                current_edit.set_edit_text(new_text)

                current_edit.set_edit_pos(cursor_position + len(pasted_text))

                self.status_msg_footer_text.set_text("Text paste from clipboard.")

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def go_up_directory(self, button):
        "Naik satu level ke direktori atas dan memperbarui daftar file."

        self.current_path = os.path.dirname(self.current_path)

        self.file_list[:] = self.get_file_list()

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def open_file(self, button, file_name):
        "Membuka file yang dipilih, membaca isinya, dan menampilkannya di text editor. Jika itu adalah direktori, berpindah ke direktori tersebut."

        if file_name:
            file_path = resolve_relative_path(self.current_path, file_name)

            _c, ext = os.path.splitext(file_path)

            if os.path.isdir(file_path):
                if validate_folder(file_path):
                    try:
                        sys.path.remove(self.current_path)

                    except:
                        pass

                    self.current_path = file_path

                    self.file_list[:] = self.get_file_list()

                else:
                    self.status_msg_footer_text.set_text("Folder access denied!")

            else:
                if validate_folder(os.path.dirname(file_path)) and validate_file(
                    file_path, os.path.getsize(file_path) or 20, 6
                ):
                    try:
                        with open(
                            file_path, "r+", encoding=sys.getfilesystemencoding()
                        ) as f:
                            content = f.read()

                    except UnicodeDecodeError:
                        with open(file_path, "r+", encoding="latin-1") as f:
                            content = f.read()

                    content = content.replace("\t", " " * 4)

                    self.undo_stack.append(content)

                    self.text_editor.set_edit_text(content)

                    if self.current_file_name != file_path:
                        modulefile = self.module_package_Python.get_moduleV2(file_path)

                        if modulefile:
                            if modulefile != self.module_package_Python.curents:
                                self.listmodules_from_package_Python[
                                    :
                                ] = self.create_modules_menus(modulefile)

                                self.module_package_Python.curents = modulefile

                        else:
                            self.listmodules_from_package_Python[
                                :
                            ] = self.create_modules_menus(self.module_package_PythonC)

                    self.current_file_name = file_name  # Track the current file name

                    # if str(ext).lower() in ( ".pyx", ".pyz", ".py"):

                    #    self.listmodules_from_package_Python[:] = self.modules_menus(self.current_path)

                    if self.module_package_Python.languages:
                        self.Inspect_modules_from_package_Python.body.set_title(
                            self.module_package_Python.languages["languages"]
                            + " Modules"
                        )

                    self.main_layout.body.contents[2][0].set_title(file_name)

                else:
                    self.status_msg_footer_text.set_text("File access denied!")

            if str(ext).lower().startswith((".pyx", ".pyz", ".py")) != True:
                self.Text_Deinspect_modules_from_package_Python.set_text(
                    "Select a module to inspect."
                )

        else:
            self.status_msg_footer_text.set_text("File binary access denied!")

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def save_file(self):
        "Menyimpan perubahan yang dilakukan pada file saat ini dan mengembalikan status keberhasilan."

        if self.current_file_name:
            file_path = os.path.join(self.current_path, self.current_file_name)

            if os.path.isfile(file_path):
                try:
                    with open(
                        file_path, "w+", encoding=sys.getfilesystemencoding()
                    ) as f:
                        f.write(self.text_editor.get_edit_text())

                except:
                    with open(file_path, "w+", encoding="latin-1") as f:
                        f.write(self.text_editor.get_edit_text())

                self.status_msg_footer_text.set_text("File saved successfully!")

        return True

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def delete_file(self):
        "Menghapus file yang dipilih dan memperbarui daftar file serta text editor dan mengembalikan status keberhasilan."

        if self.current_file_name:
            file_path = os.path.join(self.current_path, self.current_file_name)

            if os.path.isfile(file_path):
                os.remove(file_path)

                self.text_editor.set_edit_text("")

                self.file_list[:] = self.get_file_list()

                self.status_msg_footer_text.set_text("File deleted successfully!")

                self.current_file_name = None  # Clear the current file name

            else:
                self.status_msg_footer_text.set_text("File does not exist!")

        return True

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def save_undo_state(self):
        "Menyimpan status saat ini dari text editor ke stack undo dan mengosongkan stack redo."

        # Save the current content of the text editor for undo

        current_text = self.text_editor.get_edit_text()

        self.undo_stack.append(current_text)

        self.redo_stack.clear()  # Clear redo stack on new change

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def undo_edit(self):
        "Melakukan undo terhadap perubahan terakhir pada text editor dengan mengembalikan status dari stack undo."

        if self.undo_stack:
            # Save the current state to redo stack

            self.redo_stack.append(self.text_editor.get_edit_text())

            # Restore the last state

            last_state = self.undo_stack.pop()

            self.text_editor.set_edit_text(last_state)

            self.status_msg_footer_text.set_text("Undo performed.")

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def redo_edit(self):
        "Melakukan redo terhadap perubahan terakhir yang diundo dengan mengembalikan status dari stack redo."

        if self.redo_stack:
            # Save the current state to undo stack

            self.undo_stack.append(self.text_editor.get_edit_text())

            # Restore the last redone state

            last_state = self.redo_stack.pop()

            self.text_editor.set_edit_text(last_state)

            self.status_msg_footer_text.set_text("Redo performed.")

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def highlight_text(self, search_text):
        text = self.text_editor.get_edit_text()

        result = []

        # Pisahkan teks menjadi sebelum, pencarian, dan sesudahnya

        for x in findpositions(f"{search_text}", text):
            if x:
                _x = list(x)

                result.append(str(_x[0][1][1]))

        if result.__len__() > 8:
            return "Total: {total}  Pos: {posts}".format(
                total=result.__len__(), posts=", ".join(result[:8]) + "..."
            )

        return "Total: {total}  Pos: {posts}".format(
            total=result.__len__(), posts=", ".join(result)
        )

    @complex_handle_errors(loggering=logging)
    def in_search_(self, button):
        "Mencari file atau folder berdasarkan input pencarian, membuka file jika ditemukan, atau memperbarui daftar file jika folder ditemukan."

        search_query = self.search_edit.get_edit_text().replace("\\", "/").strip()

        if search_query:
            if ":" in search_query and not search_query.startswith("@[select]"):
                if os.path.isfile(search_query):
                    dirname, file_name = os.path.dirname(
                        search_query
                    ), os.path.basename(search_query)

                    try:
                        with open(search_query, "r+", encoding="utf-8") as f:
                            content = f.read()

                    except UnicodeDecodeError:
                        with open(search_query, "r+", encoding="latin-1") as f:
                            content = f.read()

                    content = content.replace("\t", " " * 4)

                    self.undo_stack.append(content)

                    self.text_editor.set_edit_text(content)

                    self.current_file_name = file_name  # Track the current file name

                    self.main_layout.body.contents[1][0].set_title(file_name)

                elif os.path.isdir(search_query):
                    dirname = search_query

                else:
                    x, _y = os.path.split(search_query)

                    if self.current_path.replace("\\", "/") == x.replace(
                        "\\", "/"
                    ) and os.path.isdir(x):
                        if _y.endswith(("/", "\\")) or _y.find(".") == -1:
                            _y = rreplace(_y, "/", "", 1)
                            _y = rreplace(_y, "\\", "", 1)
                            if isvalidate_folder(_y):
                                search_query = str(create_file_or_folder(search_query))
                            else:
                                search_query = "{search_query} is Failed"
                        else:
                            if isvalidate_filename(_y):
                                search_query = str(create_file_or_folder(search_query))
                            else:
                                search_query = "{search_query} is Failed"

                        self.update_ui()

                        self.file_list[:] = self.get_file_list()

                    dirname = None

                if dirname:
                    self.current_path = dirname

                    self.file_list[:] = self.get_file_list()

                self.status_msg_footer_text.set_text(
                    f"Search results for '{search_query}'"
                )

            else:
                search_resultsFile = [
                    f for f in os.listdir(self.current_path) if search_query in f
                ]

                search_resultsModule = [
                    module
                    for module in self.module_package_Python.curents
                    if search_query in module
                ]

                search_resultsHighlight_Text = self.highlight_text(search_query)

                if search_resultsFile and search_resultsModule:
                    self.listmodules_from_package_Python[:] = self.create_modules_menus(
                        search_resultsModule
                    )

                    self.file_list[:] = self.create_file_list(search_resultsFile)

                    self.status_msg_footer_text.set_text(
                        f"Search results for '{search_query}'"
                    )

                elif search_resultsFile:
                    self.file_list[:] = self.create_file_list(search_resultsFile)

                    self.status_msg_footer_text.set_text(
                        f"Search results for '{search_query}'"
                    )

                else:
                    if search_resultsModule:
                        self.listmodules_from_package_Python[
                            :
                        ] = self.create_modules_menus(search_resultsModule)

                        self.file_list[:] = self.get_file_list()

                        self.status_msg_footer_text.set_text(
                            f"Search results for '{search_query}'"
                        )

                    elif search_resultsHighlight_Text and not search_query.startswith(
                        "@[files]"
                    ):
                        self.status_msg_footer_text.set_text(
                            f"Search results for '{search_query}' {search_resultsHighlight_Text}"
                        )

                    else:
                        if (
                            search_query.startswith("@[select]")
                            and search_query.find("[@rename]") > -1
                        ):
                            x = search_query.replace("@[select]", "", 1).split(
                                "[@rename]", 1
                            )

                            if x.__len__() == 2:
                                getREName = [
                                    f
                                    for f in os.listdir(self.current_path)
                                    if x[0] in f
                                ]

                                if getREName.__len__() > 0:
                                    oldfilesorfolder, newplace = [
                                        os.path.join(self.current_path, getREName[0]),
                                        os.path.join(self.current_path, x[1]),
                                    ]
                                    _y, _xs = os.path.split(newplace)
                                    if _xs:
                                        if (
                                            _xs.endswith("/", "\\")
                                            or _xs.find(".") == -1
                                        ):
                                            _y = rreplace(_xs, "/", "", 1)
                                            _y = rreplace(_xs, "\\", "", 1)
                                            if not isvalidate_folder(_xs):
                                                return
                                        else:
                                            if not isvalidate_filename(_xs):
                                                return
                                        try:
                                            os.rename(oldfilesorfolder, newplace)

                                            self.status_msg_footer_text.set_text(
                                                f"Rename {getREName[0]} success"
                                            )

                                            self.update_ui()

                                            self.file_list[:] = self.get_file_list()

                                        except:
                                            pass

                        else:
                            self.status_msg_footer_text.set_text(
                                f"Search results for {search_query}"
                            )

        else:
            self.file_list[:] = self.get_file_list()

            self.listmodules_from_package_Python[:] = self.create_modules_menus(
                self.module_package_Python.curents
            )

            self.status_msg_footer_text.set_text("")

    @complex_handle_errors(loggering=logging)
    def create_file_list(self, files):
        "Membuat daftar widget untuk file yang ditemukan sesuai hasil pencarian."

        widgets = []

        for f in files:
            if os.path.isdir(os.path.join(self.current_path, f)):
                f = f + "/"

            button = FileButton(f, self.open_file, f)

            # urwid.connect_signal(button, "click", self.open_file, f)

            widgets.append(urwid.AttrMap(button, None, focus_map="reversed"))

        return widgets

    def system_usage(self):
        "Memantau penggunaan CPU dan menampilkan peringatan jika konsumsi CPU tinggi."

        timemming = timeout_v1()

        if timemming > 0.87:
            self.status_msg_footer_text.set_text("High CPU utilization alert")

    def update_ui(self):
        "Memperbarui tampilan UI aplikasi."

        self.loop.draw_screen()

    def update_uiV2(self, *args, **kwargs):
        "Memperbarui tampilan UI aplikasi."

        self.loop.set_alarm_in(timeout_v2(), self.update_uiV2)

        self.loop.draw_screen()

    def quit_app(self, button=None):
        "Menghentikan aplikasi dan menghapus alarm sistem jika ada."

        if self.system_alarm != None:
            self.loop.remove_alarm(self.system_alarm)  # Hentikan alarm

        self.system_alarm = None

        raise urwid.ExitMainLoop()

    def run(self):
        "Memulai loop utama urwid untuk menjalankan aplikasi."

        self.loop.run()


@complex_handle_errors(loggering=logging)
def main(path: str):
    app = SuperNano(start_path=path)

    app.run()


if __name__ == "__main__":
    set_low_priority(os.getpid())

    #########mendapatkan process terbaik tanpa membebani ram dan cpu

    safe_executor = SafeProcessExecutor(
        max_workers=1
    )  #########mendapatkan process terbaik tanpa membebani cpu

    safe_executor.submit(main, path=parse_args())

    time.sleep(timeout_v2())

    safe_executor.shutdown(
        wait=True
    )  ###mmenunggu process benar-benar berhenti tanpa memaksanya

    rd = StreamFile(
        file_path=fileloogiing,
        buffer_size=os.path.getsize(fileloogiing) + 2,
        print_delay=timeout_v2(),
    )  #########mendapatkan process terbaik membaca file logging tanpa membebani cpu

    for r in rd.readlines():
        print(r)

    rd.eraseFile()  # membersihkan loggging

    rd.close()
