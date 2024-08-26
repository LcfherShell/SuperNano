import py_cui
import os, sys, time, argparse, logging
from typing import List, Tuple, Any
from datetime import datetime
from string import ascii_letters, punctuation
try:
    from libs.titlecommand import get_console_title, set_console_title
    from libs.cmd_filter import shorten_path, validate_folder
    from libs.errrorHandler import complex_handle_errors
    from libs.system_manajemen import set_low_priority, SafeProcessExecutor
    from libs.filemanager import StreamFile, all_system_paths, resolve_relative_path_v2
    from libs.timeout import timeout_v2
    
except:
    try:
        from .titlecommand import get_console_title, set_console_title
        from .cmd_filter import shorten_path, validate_folder
        from .errrorHandler import complex_handle_errors
        from .system_manajemen import set_low_priority, SafeProcessExecutor
        from .filemanager import StreamFile, all_system_paths, resolve_relative_path_v2
        from .timeout import timeout_v2
    except:
        from titlecommand import get_console_title, set_console_title
        from cmd_filter import shorten_path, validate_folder
        from errrorHandler import complex_handle_errors
        from system_manajemen import set_low_priority, SafeProcessExecutor
        from filemanager import StreamFile, all_system_paths, resolve_relative_path_v2
        from timeout import timeout_v2
        

set_low_priority(os.getpid())
#########mendapatkan process terbaik tanpa membebani ram dan cpu

__version__ = "1.0.0"
thisfolder, _x = all_system_paths

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setTitle(title: str):
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

class SuperNano:
    def __init__(self, root: py_cui.PyCUI, path):
        self.root = root
        self.path = path
        # Confirmation message
        self.confirmation_popup = None
        self.prev_dir_stack: List[str] = []

        # Set Title Window Console
        setTitle("Win-SuperNano")

        # Determine if path is a file or directory
        if os.path.isfile(self.path):
            self.dir = os.path.dirname(self.path)
            self.file_to_open = os.path.basename(self.path)
        else:
            self.dir = self.path
            self.file_to_open = None

        # Initialize undo stack
        self.undo_stack: List[Tuple[str, int, Any]] = []

        # Key bindings
        self.root.add_key_command(py_cui.keys.KEY_CTRL_S, self.save_opened_file)
        self.root.add_key_command(py_cui.keys.KEY_CTRL_D, self.delete_selected_file)
        self.root.add_key_command(py_cui.keys.KEY_CTRL_Z, self.undo_last_edit)

        # File selection menu
        self.file_menu = self.root.add_scroll_menu(
            "Directory Files", 0, 0, row_span=5, column_span=2
        )
        self.file_menu.add_key_command(py_cui.keys.KEY_ENTER, self.open_file_dir)
        self.file_menu.add_key_command(
            py_cui.keys.KEY_DELETE, self.delete_selected_file
        )
        self.file_menu.add_text_color_rule(
            "<DIR>",
            py_cui.GREEN_ON_BLACK,
            "startswith",
            match_type="region",
            region=[5, 1000],
        )
        self.file_menu.set_color(py_cui.WHITE_ON_BLACK)

        # Search box
        self.search_box = self.root.add_text_box("Search", 5, 0, column_span=2)
        self.search_box.add_key_command(py_cui.keys.KEY_ENTER, self.search_files)
        self.search_box.set_color(py_cui.WHITE_ON_BLACK)
        self.search_box.set_focus_text('Press Enter')
        #self.search_box. ('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")[]')

        # Delete button
        self.delete_button = self.root.add_button(
            "Delete Selected File",
            6,
            0,
            column_span=2,
            command=self.delete_selected_file,
        )
        self.delete_button.set_color(py_cui.WHITE_ON_BLACK)
        self.delete_button.set_focus_text('Press Enter')

        # Directory text box
        self.current_dir_box = self.root.add_text_box(
            "Current Directory", 7, 0, column_span=2
        )
        self.current_dir_box.set_text(self.dir)
        self.current_dir_box.set_color(py_cui.WHITE_ON_BLACK)
        self.current_dir_box.add_key_command(
            py_cui.keys.KEY_ENTER, self.open_new_directory
        )

        # Text box for adding new files
        self.new_file_textbox = self.root.add_text_block(
            "Add New File", 8, 0, column_span=2
        )
        self.new_file_textbox.add_key_command(py_cui.keys.KEY_ENTER, self.add_new_file)
        self.new_file_textbox.set_color(py_cui.WHITE_ON_BLACK)
        self.new_file_textbox.set_focus_text('Press Enter')

        # Main text block for editing text
        self.edit_text_block = self.root.add_text_block(
            "Open file", 0, 2, row_span=8, column_span=6
        )
        self.edit_text_block.set_focus_text('Save - Ctrl + S')
        self.edit_text_block.set_color(py_cui.WHITE_ON_BLACK)

        # Footer Text
        self.footer = self.root.add_label(
            "Ctrl+S : Save file     Ctrl+D : Delete File     Ctr+Z : Undo Edit",
            8,
            2,
            column_span=6,
        )
        self.footer.set_color(py_cui.WHITE_ON_BLACK)

        # Open initial directory
        self.open_new_directory()

        # If initial path was a file, open it
        if self.file_to_open:
            self.open_file_dir(self.file_to_open)

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def save_current_state(self):
        """
        Save the current state of the text block for undo functionality.
        """
        current_text = self.edit_text_block.get()
        if not self.undo_stack or self.undo_stack[-1] != current_text:
            self.undo_stack.append(current_text)

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def undo_last_edit(self):
        """
        Undo the last edit by reverting to the previous state.
        """
        if self.undo_stack:
            self.undo_stack.pop()  # Remove current state
            if self.undo_stack:
                last_state = self.undo_stack[-1]  # Get the previous state
                self.edit_text_block.set_text(last_state)
    
    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def open_new_directory(self):
        """
        Open and list the contents of a new directory.
        """
        target = self.current_dir_box.get()
        if not target:
            target = "."
        elif not os.path.exists(target):
            self.root.show_error_popup(
                "Does not exist", f"ERROR - {target} path does not exist"
            )
            return
        elif not os.path.isdir(target):
            self.root.show_error_popup(
                "Not a Dir", f"ERROR - {target} is not a directory"
            )
            return

        # Update previous directory stack and set the new directory
        if self.dir != target:
            self.prev_dir_stack.append(self.dir)
            self.dir = target

        target = os.path.abspath(target)
        self.current_dir_box.set_text(target)

        files = (
            ["<DIR> .."] if self.prev_dir_stack else []
        )  # Add ".." only if we have a previous directory
        dir_contents = os.listdir(self.dir)
        for elem in dir_contents:
            if os.path.isfile(os.path.join(self.dir, elem)):
                if validate_folder(path=os.path.join(self.dir, elem)):
                    files.append(elem)
            else:
                if validate_folder(path=os.path.join(self.dir, elem)):
                    files.append("<DIR> " + elem)

        self.file_menu.clear()
        self.file_menu.add_item_list(files)
    
    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def add_new_file(self):
        """
        Add a new file to the file menu.
        """
        new_file_name = self.new_file_textbox.get().strip()
        if not new_file_name:
            self.root.show_error_popup(
                "Invalid File Name", "Please enter a valid file name."
            )
            return

        self.file_menu.add_item(new_file_name)
        self.file_menu.selected_item = len(self.file_menu.get_item_list()) - 1
        self.new_file_textbox.set_selected(False)
        self.root.set_selected_widget(self.edit_text_block.get_id())
        self.edit_text_block.set_title(new_file_name)
        self.edit_text_block.clear()
        self.new_file_textbox.clear()
        self.undo_stack.clear()  # Clear undo stack when a new file is added

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def open_file_dir(self, filename=None):
        """
        Open a file or directory.
        """
        filename = filename or self.file_menu.get()
        if filename.startswith("<DIR>"):
            if filename == "<DIR> ..":
                # Navigate back to the previous directory
                if self.prev_dir_stack:
                    self.dir = self.prev_dir_stack.pop()
                    self.current_dir_box.set_text(self.dir)
                    self.open_new_directory()
            else:
                # Open the selected directory
                new_dir = os.path.join(self.dir, filename[6:])
                self.current_dir_box.set_text(new_dir)
                self.open_new_directory()
        else:
            if validate_folder(path=os.path.join(self.dir, filename)):
                try:
                    with open(os.path.join(self.dir, filename), "r+") as fp:
                        text = fp.read()
                    self.edit_text_block.set_text(text)
                    self.edit_text_block.set_title(filename)
                    self.undo_stack.clear()  # Clear undo stack when a new file is opened
                    self.undo_stack.append(
                        text
                    )  # Add the initial state of the file to the undo stack
                    # Set Title Window Console
                    setTitle(os.path.join(self.dir, filename))
                except Exception as e:
                    logging.error(f"Failed to open file {filename}: {e}")
                    self.root.show_warning_popup(
                        "Not a text file",
                        "The selected file could not be opened - not a text file",
                    )
            else:
                self.root.show_warning_popup(
                    "Not a text file",
                    "The selected file could not be opened - not a text file",
                )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def save_opened_file(self):
        """
        Save the currently opened file.
        """
        if self.edit_text_block.get_title() != "Open file":
            self.save_current_state()  # Save the current state before saving
            try:
                if validate_folder(
                    path=os.path.join(self.dir, self.edit_text_block.get_title())
                ):
                    with open(
                        os.path.join(self.dir, self.edit_text_block.get_title()), "w+"
                    ) as fp:
                        fp.write(self.edit_text_block.get())
                    self.root.show_message_popup(
                        "Saved",
                        f"Your file has been saved as {self.edit_text_block.get_title()}",
                    )
            except Exception as e:
                logging.error(
                    f"Failed to save file {self.edit_text_block.get_title()}: {e}"
                )
                self.root.show_error_popup("Save Error", "Failed to save the file.")
        else:
            self.root.show_error_popup(
                "No File Opened", "Please open a file before saving it."
            )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def delete_selected_file(self):
        """
        Delete the currently selected file.
        """
        if self.edit_text_block.get_title() != "Open file":
            if validate_folder(
                path=os.path.join(self.dir, self.edit_text_block.get_title())
            ):
                self.root.show_yes_no_popup(
                    "Are you sure you want to delete this file?",
                    command=self.confirm_delete,
                )
        else:
            self.root.show_error_popup(
                "No File Opened", "Please open a file before deleting it."
            )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def confirm_delete(self, confirmed: bool):
        """
        Confirm the deletion of the file based on user response.
        """
        if confirmed:
            try:
                os.remove(os.path.join(self.dir, self.edit_text_block.get_title()))
                self.edit_text_block.clear()
                self.edit_text_block.set_title("Open file")
                self.file_menu.remove_selected_item()
                self.root.show_message_popup(
                    "Deleted", "The file has been successfully deleted."
                )
            except OSError as e:
                logging.error(
                    f"Failed to delete file {self.edit_text_block.get_title()}: {e}"
                )
                self.root.show_error_popup(
                    "OS Error", "Operation could not be completed due to an OS error."
                )
        else:
            self.root.show_message_popup(
                "Delete Cancelled", "File deletion was cancelled."
            )

    @complex_handle_errors(loggering=logging, nomessagesNormal=False)
    def search_files(self):
        """
        Search for files in the directory that match the search query.
        """
        query = self.search_box.get().strip().lower()
        if not query:
            self.root.show_error_popup(
                "Invalid Query", "Please enter a valid search query."
            )
            return

        matched_files = []
        for item in self.file_menu.get_item_list():
            if query in item.lower() and validate_folder(
                path=os.path.join(self.dir, item.lower())
            ):
                matched_files.append(item)

        if not matched_files:
            self.root.show_error_popup(
                "No Matches", "No files or directories match your search query."
            )
        else:
            self.file_menu.clear()
            self.file_menu.add_item_list(matched_files)


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
    args = vars(parser.parse_args())
    path = args.get("path", ".").strip().replace("\\", "/")
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


def main():
    path = parse_args()
    # Initialize the PyCUI object, and set the title
    root = py_cui.PyCUI(9, 8)
    root.set_title(
        f"Win-SuperNano v{__version__} CopyRight: LcfherShell@{datetime.now().year}"
    )
    # Create the wrapper instance object.
    SuperNano(root, path)
    # Start the CUI
    root.start()

if __name__ == "__main__":
    safe_executor = SafeProcessExecutor(max_workers=2)
    # Collect argument information
    safe_executor.submit(main)
    time.sleep(timeout_v2())
    safe_executor.shutdown(wait=True)
    
