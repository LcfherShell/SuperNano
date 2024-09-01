<img src="https://repository-images.githubusercontent.com/847198464/b36c0223-b3fa-4846-8f82-21e1b48d7021" alt="Banner" style="max-width: 100%; height: auto;" />

Here is the documentation for the `SuperNano` script, a console-based editor written in Python with the `py_cui` module. It provides an interface for managing files and directories and provides basic text editing features. 

---

# SuperNano Documentation

## Description
`SuperNano` is a console-based text editor that allows users to open, edit, save and delete files directly from a text-based interface. It also provides file editing, directory navigation and file search features.

### Key Features:
- **Directory Navigation**: Displays the contents of directories and allows navigation between directories.
- **Text Editing**: Allows editing of text files with undo feature.
- File Saving**: Saves changes to the opened file.
- File Deletion**: Deletes the selected file.
- File Search**: Searches for files or directories by name.

## Code Structure
This script is divided into several important parts:
1. **Imports**: This section imports the modules required to run the application. In addition to the standard Python modules, this script also imports some specialized modules that serve for system management, file management, error handling, and timing.

2. **Configure Logging**: Set up logging to record events or errors that occur during application running.

3. **SetTitle function**: This function is used to set the title of the console window according to the path of the current file or directory.

4. **SuperNano class**: This class is the core of the application that manages various features such as opening files, saving files, deleting files, directory navigation, and others.

5. **Function `parse_args`**: This function is used to parse command line arguments that specify the target file or directory to edit.

6. **The `main` function**: The main function that initializes the `PyCUI` object, sets the application title, and starts the user interface.

7. **Safe Execution**: Uses `SafeProcessExecutor` to safely run the application using threads.

## Implementation Details

### Class `SuperNano`
This class handles all the functionality of the application and is initialized with the parameters `root` (`PyCUI` object) and `path` (file or directory path). Some important methods in this class are:

- **`__init__`**: Initializes the interface and determines if `path` is a file or directory.
- **`open_new_directory`**: Opens and displays the contents of the new directory.
- **`open_file_dir`**: Opens a file or navigates to the selected directory.
- **`save_opened_file`**: Saves the currently opened file.
- **`delete_selected_file`**: Deletes the selected file.
- **`search_files`**: Searches for files in the directory based on the search input.

### `setTitle` function
This function sets the title of the console window to the name of the current file or directory, and adjusts its length to not exceed a certain character limit.

### `parse_args` function
This function is used to process the arguments given through the command line. The arguments will determine which file or directory will be opened by `SuperNano`.

### Safe Execution
The use of `SafeProcessExecutor` ensures that the application runs safely and efficiently, especially when executing functions that may take time.

## How to run script
Run this script through the command line by giving an argument in the form of the path of the file or directory you want to edit. Example:
```
python supernano.py /path/to/directory_or_file
```
or visit [main](https://github.com/LcfherShell/SuperNano/tree/main)

## License
This application was created by Ramsyan Tungga Kiansantang and is licensed under the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.html). For contributions or bug reporting, please visit the provided Github repository.

## Version
- **Version**: V1.0.0
- **Release Date**: July 18, 2024

---

## Conclusion
`SuperNano` is a console-based text editor designed to make it easy to manage files and directories directly from the command line. It offers lightweight tools for users working in a text-based environment.

If you have any questions or need further assistance with the implementation, feel free to contact the developer or check out any additional documentation that may be available. [Email Support](mailto:alfiandecker2@gmail.com,ramstungga2@gmail.com)
