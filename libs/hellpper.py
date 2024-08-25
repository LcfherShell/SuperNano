import sys, os, platform
import ctypes
from ctypes import wintypes as w

def version(osname=None):
    if osname:
        try:
            assert osname in ['windows', 'linux', 'darwin']
        except:
            if ['windows', 'linux', 'darwin'].index(osname):
                pass
            else:
                return
        versions = sys.getwindowsversion().major or platform.version().split('.')[0]
    else:
        versions = "0.2"
    return versions


def os_platform():
    platforms = platform.system() or os.name or sys.platform
    if platforms.startswith(("windows", "Windows", "nt", "win")):
        platformname = "windows"
    elif platforms.startswith(("darwin", "Darwin", "Air", "air", "posix")):
        if os.name =="posix" and platform.system() == "Darwin":
            platformname = "darwin"
        else:
            platformname = "darwin"
    elif platforms.startswith(("posix","fedora", "Fedora", "unix", "Unix", "Linux", "linux", "ubuntu", 'Ubuntu', "debian"
        , "Debian", "arch", "Arch", "redhat", "Redhat")):
        platformname = "linux"
    else:
        platformname = "unknow"
    return platformname

def sizewindow():
    from ctypes import windll, byref
    from ctypes.wintypes import SMALL_RECT

    STDOUT = -11

    hdl = windll.kernel32.GetStdHandle(STDOUT)
    rect = SMALL_RECT(0, 50, 150, 80) # (left, top, right, bottom)
    windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))

#os.system("mode con cols=93 lines=45")
def fontsize():
    import ctypes

    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 10  # in your case X=10
    font.dwFontSize.Y = 18  # and Y=18



    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle,False, ctypes.byref(font))


def getTerminalSize(platformname):
   #import platform
    current_os = platform.system()
    tuple_xy = None
    try:
        if platformname == 'windows':
            tuple_xy = _getTerminalSize_windows()
            if tuple_xy is None:
                tuple_xy = _getTerminalSize_tput()
                # needed for window's python in cygwin's xterm!
        if platformname == 'linux' or platformname == 'darwin' or  current_os.startswith('CYGWIN'):
            tuple_xy = _getTerminalSize_linux()
        if tuple_xy is None:
            tuple_xy = (80, 25)      # default value
    except:
        import shutil
        columns, lines = shutil.get_terminal_size((80, 20))
        return columns, lines
    return tuple_xy

def _getTerminalSize_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
       import subprocess
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


all = ["fontsize"]

from ptpython.python_input import PythonInput


def main():
    prompt = PythonInput()

    text = prompt.app.run()
    print("You said: " + text)

import pathlib
import collections
collections.Callable = collections.abc.Callable
try:
    import readline
except ImportError:
    import pyreadline as readline

def complete_path(text, state):
    incomplete_path = pathlib.Path(text)
    if incomplete_path.is_dir():
        completions = [p.as_posix() for p in incomplete_path.iterdir()]
    elif incomplete_path.exists():
        completions = [incomplete_path]
    else:
        exists_parts = pathlib.Path('.')
        for part in incomplete_path.parts:
            test_next_part = exists_parts / part
            if test_next_part.exists():
                exists_parts = test_next_part

        completions = []
        for p in exists_parts.iterdir():
            p_str = p.as_posix()
            if p_str.startswith(text):
                completions.append(p_str)
    return completions[state]


# we want to treat '/' as part of a word, so override the delimiters
#readline.set_completer_delims(' \t\n;')
#readline.parse_and_bind("tab: complete")
#readline.set_completer(complete_path)
#while True:
#    print(input('tab complete a filename: '))
#if __name__ == '__main__':
    #sizex,sizey=getTerminalSize(os_platform())
    #print('width =',sizex,'height =',sizey)
    #answer = prompt('Give me some input: ')
    #print('You said: %s' % answer)


# From the documentation at
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
MB_OKCANCEL = 1
IDCANCEL = 2
IDOK = 1

user32 = ctypes.WinDLL('user32')
MessageBox = user32.MessageBoxW
MessageBox.argtypes = w.HWND,w.LPCWSTR,w.LPCWSTR,w.UINT
MessageBox.restype = ctypes.c_int

ret = MessageBox(None, 'message', 'title', MB_OKCANCEL)
if ret == IDOK:
    print('OK')
elif ret == IDCANCEL:
    print('CANCEL')
else:
    print('ret =', ret)

import curses, textwrap
from editor.editor import Editor


def xxsx():
    stdscr = curses.initscr()
    xxx = Editor(stdscr,  box=False)
    while True:
        xxx.stdscr.move(xxx.cur_pos_y, xxx.cur_pos_x)
        loop = xxx.get_key()
        if loop is False:
            break
        xxx.display()
    print("\n".join(["".join(i) for i in xxx.text]))

screen = curses.initscr()
screen.immedok(True)
try:
    screen.border(0)
    screen.addstr("Hello! Dropping you in to a command prompt...\n")
    box1 = curses.newwin(20, 40, 6, 50)
    box2 = curses.newwin(18,38,7,51)
    box1.immedok(True)
    box2.immedok(True)
    text = "I want all of this text to stay inside its box. Why does it keep going outside its borders?"
    text = "The quick brown fox jumped over the lazy dog."
    text = "A long time ago, in a galaxy far, far away, there lived a young man named Luke Skywalker."
    box1.box()
    box2.addstr(1, 0, textwrap.fill(text, 38))

    #box1.addstr("Hello World of Curses!")

    screen.getch()

finally:
    curses.endwin()