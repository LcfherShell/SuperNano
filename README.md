<img src="https://repository-images.githubusercontent.com/847198464/b36c0223-b3fa-4846-8f82-21e1b48d7021" alt="Banner" style="max-width: 100%; height: auto;" />

Here is the documentation for the `SuperNano` script, a powerful console-based text editor specialized for Windows 8, 10, 11 platforms.

---

# SuperNano Documentation

## Description
`SuperNano` is a console-based text editor developed using Python and the `urwid[curses]` library. It is designed to give users the ability to edit text, manage files, and inspect Python modules directly from a console-based interface. SuperNano supports several features such as undo-redo, clipboard (copy-paste), file search, and Python module inspection.

## Key Features
- **Text Editing**: Text editor with multiline support, undo-redo, copy-paste, and file saving.
- **File Management**: Allows directory navigation, opening and saving files, and creating and deleting files.

## Classes and Methods

### 1. `SuperNano`
`SuperNano` is the main class that manages the entire application, including initialization, menu creation, and UI management.

#### Attributes:
- **current_path**: Stores the current directory path.
- **current_file_name**: Stores the name of the current file.
- **undo_stack**, **redo_stack**: Stack used to store text state to support undo-redo feature.
- **overlay**: Widget used to display a popup.
- **loop**: The `urwid.MainLoop` object that handles application loop events.
- **loading_alarm**, **system_alarm**: Alarms for timing layout changes and monitoring the system.

#### Methods:
- **`__init__(self, start_path=“.”)`**: Initialize the class, set up the start path, widgets, and start the event loop.
- **`load_main_menu(self)`**: Set up and display the main menu after the loading period.
- **`switch_to_secondary_layout(self)`**: Changes the application layout to the main menu.
- **`setup_main_menu(self)`**: Set up widgets for the main menu, including the file list, text editor, and functional buttons.
- **`setup_popup(self, options, title, descrip=“”)`**: Sets up the content and layout for the popup menu.
- **`show_popup(self, title, descrip, menus)`**: Displays the popup menu with the given title, description, and options.
- **`close_popup(self, button)`**: Closes the popup and returns to the main layout.
- **`get_file_list(self)`**: Retrieve a list of files and directories in the current path.
- **`handle_input(self, key)`**: Handles keyboard input for various actions such as exit, save, delete, undo, redo, copy-paste, and UI refresh.
- **`get_current_edit(self)`**: Returns the currently focused edit widget (text editor or search edit).
- **`set_focus_on_click(self, widget, new_edit_text, index)`**: Sets the focus on the edit widget based on click and index.
- **`copy_text_to_clipboard(self)`**: Copies the text from the current edit widget to the clipboard.
- **`paste_text_from_clipboard(self)`**: Paste text from the clipboard into the current edit widget.


## Usage
1. **Running the Application**: Run the `SuperNano` script with Python 3.6 and above in your terminal.
2. **Navigate Files**: Use the up and down arrows to select files in the directory. Press Enter to open the file.
3. **Edit Text**: Once the file is open, the text can be edited directly in the editor. Use `Ctrl+S` to save changes.
4. **Undo-Redo**: Use `Ctrl+Z` to undo and `Ctrl+Y` to redo.
5. **Copy-Paste**: Use `Ctrl+C` to copy and `Ctrl+V` to paste.
6. **Exit Application**: Press `Ctrl+Q` or `ESC` to exit the application.

## How to use
Run this script through the command line by giving an argument in the form of the path of the file or directory you want to edit. Example:
```
python supernano.py /path/to/directory_or_file
```
or visit [main](https://github.com/LcfherShell/SuperNano/tree/main)

## License
This application was created by Ramsyan Tungga Kiansantang and is licensed under the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.html). For contributions or bug reporting, please visit the provided Github repository.

## Version
- **Version**: V1.5.3
- **Release Date**: August 21, 2024

---

## Conclusion
`SuperNano` is a console-based text editor designed to make it easy to manage files and directories directly from the command line. It offers powerful tools for users working in a text-based environment.

If you have any questions or need further assistance with the implementation, feel free to contact the developer or check out any additional documentation that may be available. [Email Support](mailto:alfiandecker2@gmail.com,ramstungga2@gmail.com)

