<a href="https://github.com/LcfherShell/SuperNano"><img src="https://repository-images.githubusercontent.com/847198464/b36c0223-b3fa-4846-8f82-21e1b48d7021" alt="SuperNano" style="max-width: 100%; height: auto;" /></a>

Here is the documentation for the `SuperNano` script, a powerful console-based text editor specialized for Windows 8, 10, 11 platforms.

---

# SuperNano Documentation

## Description
`SuperNano` is a console-based text editor developed using Python and the `urwid[curses]` library. It is designed to give users the ability to edit text, manage files, and inspect Python modules directly from a console-based interface. SuperNano supports several features such as undo-redo, clipboard (copy-paste), file search, and Python, C, NodeJS, and PHP module inspection.

## Key Features
- **Text Editing**: Text editor with multiline support, undo-redo, copy-paste, and file saving.
- **File Management**: Allows directory navigation, opening and saving files, and creating and deleting files.
- Module Inspection**: Features for inspecting Python, C, NodeJS, and PHP modules, displaying information about global variables, classes, and functions within the module.



## Classes and Methods

### `SuperNano`
`SuperNano` is the main class that manages the entire application, including initialization, menu creation, and UI management.

#### Attributes:
- **current_path**: Stores the current directory path.
- **current_file_name**: Stores the name of the current file.
- **undo_stack**, **redo_stack**: Stack used to store text state to support undo-redo feature.
- **overlay**: Widgets used to display popups.
- **modulePython**: An object of `ModuleInspector` used for Python, C, NodeJS, and PHP module inspection.
- **loop**: The `urwid.MainLoop` object that handles application loop events.
- **loading_alarm**, **system_alarm**: Alarms for timing layout changes and monitoring the system.

#### Methods:
- **`__init__(self, start_path=“.”)`**: Initialize the class, set up the start path, widgets, and start the event loop.
- **`load_main_menu(self)`**: Set up and display the main menu after the loading period.
- **`switch_to_secondary_layout(self)`**: Changes the application layout to the main menu.
- **`setup_main_menu(self)`**: Set up widgets for the main menu, including the file list, text editor, and functional buttons.
- **`create_modules_menus(self, listmodulename)`**: Creates a button for each module in `sys.path`.
- **`inspect_module(self, button, module_name)`**: Displays module inspection results in the footer.
- **`setup_popup(self, options, title, descrip=“”)`**: Sets up the content and layout for the popup menu.
- **`show_popup(self, title, descrip, menus)`**: Displays the popup menu with the given title, description, and options.
- **`close_popup(self, button)`**: Closes the popup and returns to the main layout.
- **`get_file_list(self)`**: Retrieve a list of files and directories in the current path.
- **`handle_input(self, key)`**: Handles keyboard input for various actions such as exit, save, delete, undo, redo, copy-paste, and UI refresh.
- **`get_current_edit(self)`**: Returns the currently focused edit widget (text editor or search edit).
- **`set_focus_on_click(self, widget, new_edit_text, index)`**: Sets the focus on the edit widget based on click and index.
- **`copy_text_to_clipboard(self)`**: Copies the text from the current edit widget to the clipboard.
- **`paste_text_from_clipboard(self)`**: Paste text from the clipboard into the current edit widget.

### `ModuleInspector`
This class is responsible for loading and inspecting Python, C, NodeJS, and PHP modules. Retrievable information includes global variables, classes, and functions in the module.

#### Attributes:
- **modules**: Stores a list of module names found in `sys.path`.

#### Method:
- **`get_moduleV2(self, paths)`**: Returns a list of modules found in the given paths.
- **`inspect_module(self, module_name)`**: Inspects the module with the given name and returns the details of the module.

## Usage
1. **Run Application**: Run the `SuperNano` script with Python 3.6 and above in your terminal.
2. **Navigate Files**: Use the up and down arrows to select files in the directory. Press Enter to open the file.
3. **Edit Text**: Once the file is open, the text can be edited directly in the editor. Use `Ctrl+S` to save changes.
4. **Undo-Redo**: Use `Ctrl+Z` to undo and `Ctrl+Y` to redo.
5. **Copy-Paste**: Use `Ctrl+C` to copy and `Ctrl+V` to paste.
6. **Inspect Module**: Select a module from the list available in the UI to display information about the module.
7. **Exit Application**: Press `Ctrl+Q` or `ESC` to exit the application.


## Requirements
- Python V3.8^
- Nodejs
- Clang [not required]
- PHP Composer [not required]
- Module pip (Python) : requirements.txt
- Module NPM (Node) : acorn, php-parser
  

## How to run script
Run this script through the command line by giving an argument in the form of the path of the file or directory you want to edit. Example:
```
python supernano.py /path/to/directory_or_file
```
or visit [main](https://github.com/LcfherShell/SuperNano/tree/main)

## License
This application was created by Ramsyan Tungga Kiansantang and is licensed under the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.html). For contributions or bug reporting, please visit the provided Github repository.

## Version
- **Version**: V2.2.1
- **Release Date**: August 30, 2024

---

## Conclusion
`SuperNano` is a console-based text editor designed to make it easy to manage files and directories directly from the command line. It offers powerful tools for users working in a text-based environment.

If you have any questions or need further assistance with the implementation, feel free to contact the developer or check out any additional documentation that may be available. [Email Support](mailto:alfiandecker2@gmail.com,ramstungga2@gmail.com)
