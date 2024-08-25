import json, subprocess, os, sys, threading, time, psutil, platform, random

from typing import Iterable, Container, Protocol, List, Tuple

from dataclasses import dataclass

from functools import wraps, lru_cache
try:
    from .helperegex import split, findpositions, re as regex
    from .randoms import random, randomDigits

except:
    try:
        from helperegex import split, findpositions, re as regex
        from randoms import random, randomDigits
    except:
        from libs.helperegex import split, findpositions, re as regex
        from libs.randoms import random, randomDigits


try:
    rangeX = range
except:
    rangeX = xrange
    range = xrange



@dataclass(order=True)
class ResultContainer:
    results = (
        []
    )  # Mutable - anything inside this list will be accesable anywher in your program


def save_result(cls):
    def decorator(func):
        def wrapper(args, *kwargs):
            # get result from the function

            func_result = func(args, *kwargs)

            # Pass the result into mutable list in our ResultContainer class

            cls.results.append(func_result)

            # Return result from the function

            return func_result

        return wrapper

    return decorator


@save_result(ResultContainer)
def func(a, b):
    return a * b

@lru_cache(maxsize=128)
def remwithre(text, there=regex.compile(regex.escape("=") + ".*")):
    return there.sub("", text)

@lru_cache(maxsize=128)
def compiltesV2(cmd: str)  -> List[str]:
    def find_indices_of_substring(substring, string):
        return [m.start() for m in regex.finditer(regex.escape(substring), string)]

    if "#" in cmd:
        command_part, comment_part = cmd.split("#", 1)
        comment_part = "#" + comment_part
    else:
        command_part = cmd
        comment_part = ""

    # Handle quotes
    single_quote_count = find_indices_of_substring("'", command_part).__len__()
    double_quote_count = find_indices_of_substring('"', command_part).__len__()

    if single_quote_count % 2 == 0 and single_quote_count > 0:
        record = findpositions(r"'(.*?)'", command_part)
        keysplit = "'"
    elif double_quote_count % 2 == 0 and double_quote_count > 0:
        record = findpositions(r"\"(.*?)\"", command_part)
        keysplit = '"'
    else:
        return

    recordlist = [substr for substr in record]

    for idx, substr in enumerate(recordlist):
        recordlist[idx] = list(substr)
        placeholder = f"__PLACEHOLDER_{idx}__"
        command_part = command_part.replace(recordlist[idx][0][0], placeholder)

    # Preserve & inside quotes and comments
    segments: List[Tuple[str]] = []
    in_single_quote = in_double_quote = False

    i:int = 0
    while i < len(command_part):
        char = command_part[i]
        if char == "'":
            in_single_quote = not in_single_quote
        elif char == '"':
            in_double_quote = not in_double_quote

        if char == "&" and not (in_single_quote or in_double_quote):
            if i + 1 < len(command_part) and command_part[i + 1] == "&":
                segments.append("&&")
                i += 1
            else:
                segments.append("&")
        else:
            start = i
            while i < len(command_part) and (
                char != "&"
                or (in_single_quote or in_double_quote)
                or (i + 1 < len(command_part) and command_part[i + 1] != "&")
            ):
                i += 1
                if i < len(command_part):
                    char = command_part[i]
            segments.append(command_part[start:i])
            continue
        i += 1

    # Reconstruct commands based on segments
    commands: List[Tuple[str]] = []
    outputs:List[Tuple[str]] = []
    command:str = ""
    for segment in segments:
        if segment == "&&":
            commands.append(command.strip())
            command = ""
        else:
            command += segment

    if command:
        commands.append(command.strip())

    for command in commands:
        # Restore quoted substrings from placeholders
        for i, substr in enumerate(recordlist):
            placeholder = f"__PLACEHOLDER_{i}__"
            command = command.replace(placeholder, recordlist[i][0][0])
        outputs.append(command)
    return outputs

@lru_cache(maxsize=128)
def compiltesV3(cmd: str) -> List[str]:
    def find_indices_of_substring(substring, string):
        return [m.start() for m in regex.finditer(regex.escape(substring), string)]

    def find_positions(pattern, string):
        return [(m.start(), m.group(0)) for m in regex.finditer(pattern, string)]

    # Split the command and comments
    if "#" in cmd:
        command_part, comment_part = cmd.split("#", 1)
        comment_part = "#" + comment_part
    else:
        command_part = cmd
        comment_part = ""

    # Handle quotes
    single_quote_count = len(find_indices_of_substring("'", command_part))
    double_quote_count = len(find_indices_of_substring('"', command_part))

    if single_quote_count % 2 == 0 and single_quote_count > 0:
        quoted_strings = find_positions(r"'(.*?)'", command_part)
        quote_char = "'"
    elif double_quote_count % 2 == 0 and double_quote_count > 0:
        quoted_strings = find_positions(r'"(.*?)"', command_part)
        quote_char = '"'
    else:
        return []

    # Replace quoted substrings with placeholders
    for i, (pos, substr) in enumerate(quoted_strings):
        placeholder = f"__PLACEHOLDER_{i}__"
        command_part = (
            command_part[:pos] + placeholder + command_part[pos + len(substr) :]
        )

    # Preserve & inside quotes and comments
    segments: List[Tuple[str]] = []
    i:int = 0
    while i < len(command_part):
        char = command_part[i]
        if char == quote_char:
            # Skip quoted parts
            i += 1
            while i < len(command_part) and command_part[i] != quote_char:
                i += 1
            i += 1
        elif char == "&":
            if i + 1 < len(command_part) and command_part[i + 1] == "&":
                segments.append("&&")
                i += 1
            else:
                segments.append("&")
        else:
            start = i
            while i < len(command_part) and (
                command_part[i] != "&"
                or (i + 1 < len(command_part) and command_part[i + 1] != "&")
            ):
                i += 1
            segments.append(command_part[start:i])
            continue
        i += 1

    # Reconstruct commands based on segments
    commands: List[Tuple[str]] = []
    command:str = ""
    for segment in segments:
        if segment == "&&":
            commands.append(command.strip())
            command = ""
        else:
            command += segment

    if command:
        commands.append(command.strip())

    # Restore quoted substrings from placeholders
    outputs: List[Tuple[str]] = []
    for command in commands:
        for i, (pos, substr) in enumerate(quoted_strings):
            placeholder = f"__PLACEHOLDER_{i}__"
            command = command.replace(placeholder, substr)
        outputs.append(command)

    return outputs

@lru_cache(maxsize=128)
def compiltes(string: str) -> List[str]:
    if string == "":
        return []
    
    _output: List[str] = []

    xout = findpositions(r"'(.*?)?'|\"(.*?)?\"", string)
    lenght = len(xout)
    cv = 0
    checkpoint: Tuple[str] = ()
    checkpoint2: List[Tuple[str]] = []
    place = "<%%"
    newstring = string
    keyplace = ""

    maxpend: List[int] = []
    digit: str = "1"
    xct = regex.finditer(r"<%%(.*?)?>", string)
    for xc in xct:
        if xc:
            if xc.group(0).count(" ") == 0:
                maxdigit = xc.group(1)
                maxpend.append(int(maxdigit))

    if maxpend:
        _s_s = len(str(max(maxpend))) + 1
        digit = str(_s_s)

    score_record: List[str] = []
    for y in xout:
        for x in y:
            if "&&" in x[0]:
                keyplace = "&&"
            elif "&" in x[0]:
                keyplace = "&"

            if lenght != 0:
                score = randomDigits(int(digit))
                while score in score_record:
                    score = randomDigits(int(digit))
                score_record.append(score)

                newword = "".join([place, str(score), ">"])
                newpad = regex.sub(r"&&|&", newword, x[0])
                if x[0].count("&") == 0:
                    cv += 1
                else:
                    if lenght == len(xout) - cv:
                        pass
                    else:
                        minus = len(newword) + len(keyplace)
                        checkpoint2.append((
                            x[1][0] + minus - len(keyplace),
                            x[1][-1] + minus + 1,
                        ))

                string = string.replace(x[0], newpad, 1)
                checkpoint = checkpoint + ((x[0], newword, score, keyplace),)
                lenght -= 1

    # Handle splitting based on characters following '&'
    temp_output = []
    i = 0
    while i < len(string):
        if string[i] == "&":
            if i + 1 < len(string) and (string[i + 1] == " " or string[i + 1] == "&"):
                # Split and handle based on next character
                if i > 0:
                    temp_output.append(string[:i].strip())
                string = string[i + 1:].lstrip()
                i = 0
            else:
                i += 1
        else:
            i += 1
    
    if string:
        temp_output.append(string.strip())
    # Process checkpoints to replace placeholders
    for x in temp_output:
        for y in checkpoint:
            if y[1] in x:
                oldstring = regex.search(r"'(.*?)?'", x) or regex.search(r'"(.*?)?"', x)
                if oldstring:
                    x = x.replace(oldstring.group(0), y[0], 1)
                else:
                    x = x.replace(y[1], y[3])
        _output.append(x.strip())

    return _output


@lru_cache(maxsize=128)
def functionclean(functions, powershell=True):
    # fff = regex.search(r'function(.*)\(', functions, regex.MULTILINE)

    fff = regex.search(r"function(.*)\{", functions, regex.DOTALL or regex.MULTILINE)

    if fff:
        remove_scp = regex.sub(r"\s+", "", fff.group(1), regex.UNICODE)

        _functioname = regex.match(r"(.\S+)?\(", remove_scp).group(1)

        if _functioname.count("(") != 0 and _functioname.endswith("}") == False:
            _functioname = regex.match("(.*?)\(", _functioname).group(1)

            remove_scp = regex.match("(.*?){", remove_scp).group(1)

        # print(fff.group(1), "\nFunName:",_functioname, "\nRem:", remove_scp, "\n")

        _argsx = regex.match(r"{names}\((.*)\)".format(names=_functioname), remove_scp)

        _argsx = _argsx.group(1)

        if powershell == True:
            # print(_argsx)

            # print(regex.findall(r"(\[.\S+\])", "([string]$helllo=$fo, [int]$dddd)".format(args=_argsx)))

            stringsl = regex.sub(r"(,)", r"\1 ", "({args})".format(args=_argsx))

            for scleans in regex.findall(r"(\[.\S+\])", stringsl):
                _argsx = _argsx.replace(scleans, "", 1)

            _argsx = _argsx.replace("$", "")

        _spaces = ""

        if _argsx.count('"') != 0 and _argsx.count('"') % 2 == 0:
            _spaces = '"'

        elif _argsx.count("'") != 0 and _argsx.count("'") % 2 == 0:
            _spaces = "'"

        else:
            reps = regex.sub(r"(=)", r"\1'", _argsx)

            if reps:
                xappend: List[Tuple[str]] = []

                for xsplit in reps.split(","):
                    if xsplit.count("'") != 0:
                        xappend.append(str(xsplit[: xsplit.__len__()] + "'"))

                    else:
                        xappend.append(str(xsplit + "=None"))

                _argsx = ",".join(xappend)

        if _spaces:
            clos = regex.findall(r"{args}(.*){args}".format(args=_spaces), _argsx)

            xxs: List[Tuple[str]] = []

            if clos.__len__() != 0:
                for xin in clos:
                    _argsx = _argsx.replace(xin, "", 1)

                splitz = _argsx.split(",")

                for xin in splitz:
                    if xin.find("=") != -1:
                        xxs.append(xin)

                    elif xin.find("=") == -1:
                        xxs.append(xin + "=''")

                splitz = None

                _argsx = ", ".join(xxs)

                xxs = None

        functionmake = """def {functioname}({arguments}):pass""".format(
            functioname=_functioname, arguments=_argsx
        )

        exec(
            functionmake
            + "\nf_code = {functioname}.__code__".format(functioname=_functioname)
        )

        get_arguments = eval(
            """f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]"""
        )

        """if _argsx.count("=") !=0:

                xcs = []

                for a in _argsx.split(",", _argsx.count("=")):

                    if a.find("=") != -1:

                        xcs.append(remwithre( _argsx))"""

        return dict((x, y) for x, y in [(_functioname, list(get_arguments))])

        # except:

        # return _functioname, []

@lru_cache(maxsize=128)
def classclean(classname, powershell=True):
    classreg = regex.search(r"class(.*?)\{", classname, regex.DOTALL or regex.MULTILINE)

    if classreg:
        _argsx = ""

        remove_scp = regex.sub(r"\s+", "", classreg.group(1), regex.UNICODE)

        try:
            _classsname = regex.match(r"(.\S+)?\(", remove_scp).group(1)

        except:
            _classsname = regex.match(r"(.\S+)?", remove_scp).group(1)

        if powershell == True:
            argsx_ = classreg.group(1)

            _argsx = regex.match(
                r"{names}+\((.*)\)".format(names=_classsname), remove_scp
            )

            if _argsx:
                stringsl = regex.sub(
                    r"(,)", r"\1 ", "({args})".format(args=_argsx.group(1))
                )

                _argsx = _argsx.group(1)

            else:
                pass

            for scleans in regex.findall(r"(\[.\S+\])", stringsl):
                _argsx = _argsx.replace(scleans, "", 1)

            _argsx = _argsx.replace("$", "")

        # print( regex.search(r"{(.*)}" , classname, regex.DOTALL).group(1))

        # print( r"{xxgro}(.*){endsx}".format(xxgro= classreg.group(0), endsx = "\}") )

        if _argsx.__len__() == 0:
            argsx_ = regex.search(r"{(.*)}", classname, regex.DOTALL)

            if argsx_:
                if powershell == True:
                    splits = argsx_.group(1).split("\n")

                    sout = ""

                    for sout in splits:
                        init_function = regex.match(
                            r"(.*){names}+\((.*)\)?".format(names=_classsname),
                            sout.strip(),
                        )

                        # print("after:", init_function)

                        if sout.strip().startswith("[") and init_function:
                            if init_function.group(1):
                                sout = sout.replace(init_function.group(1), "", 1)

                                if sout.endswith("{"):
                                    sout = sout[:-1].strip()

                            break

                        elif sout.strip().startswith(_classsname) and init_function:
                            # if init_function.group(1):

                            if init_function.group(0):
                                sout = init_function.group(0).strip()[:-1]

                            elif sout and sout.endswith("{"):
                                sout = sout.strip()[:-1]

                            break

                    if sout:
                        s_argsx = regex.match(
                            r"{names}+\((.*)\)".format(names=_classsname), sout
                        )

                        cleansub = regex.sub(
                            r"(,)", r"\1 ", "({args})".format(args=s_argsx.group(1))
                        )

                        for scleans in regex.findall(r"(\[.\S+\])", cleansub):
                            sout = sout.replace(scleans, "")

                        sout = regex.search(r"\((.*?)?\)", sout.replace("$", ""))

                        if sout:
                            _argsx = sout.group(1).strip()

                if _argsx.count("="):
                    xx = "function xx({args})".format(args=_argsx)
                    cleans = functionclean(xx + "{ pass}", True)
                    _argsx = ",".join(cleans["xx"])

        functionmake = """def {_classsname}({arguments}):pass""".format(
            _classsname=_classsname, arguments=_argsx
        )

        exec(
            functionmake
            + "\nf_code = {_classsname}.__code__".format(_classsname=_classsname)
        )

        get_arguments = eval(
            """f_code.co_varnames[:f_code.co_argcount + f_code.co_kwonlyargcount]"""
        )

        return dict((x, y) for x, y in [(_classsname, list(get_arguments))])


# functions = """function max_x2([string]$helllo='$fo', [int]$dddd){ pass }"""

# print(functionclean(functions=functions, powershell=True))

def map_function_arguments(class_str):
    # Regex untuk menemukan fungsi beserta argumennya
    func_pattern = regex.compile(r'[\[.*?\]]?(\w+)\((.*?)\)')
    matches = func_pattern.findall(class_str)
    
    func_args_map = {}
    for match in matches:
        func_name, args_str = match
        # Memisahkan argumen
        args = [arg.strip() for arg in args_str.split(',')]
        func_args_map[func_name] = args

    return func_args_map
#print(map_function_arguments(classname))

def validate_folder(path: str) -> bool:
    """
    Validates whether the given path is within the directory of the script.

    Parameters:
    - path (str): The folder path to validate.

    Returns:
    - bool: True if the path is valid and within the script directory, False otherwise.
    """
    # Absolute path of the script's directory
    script_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/")
    # Convert to lowercase and normalize paths
    script_dir = script_dir.lower()
    path = path.lower().replace("\\", "/")

    n = str(script_dir).split("/")
    Syscript = str("/".join(n[: n.__len__() - 1])).strip()
    # Check if path starts with the script directory path
    if path.startswith(Syscript) or path.startswith(script_dir):
        return False
    return True

def shorten_path(path: str, max_length: int) -> str:
    """
    Shorten a given path to a specified maximum length, inserting '...'
    to represent omitted sections of the path.

    Parameters:
    - path (str): The full path to shorten.
    - max_length (int): The maximum length of the shortened path.

    Returns:
    - str: The shortened path.
    """
    if len(path) <= max_length:
        return path
    
    # Replace backslashes with forward slashes for consistency
    parts = path.replace("\\", "/").split("/")
    
    # Handle Windows drive letter
    if ":" in parts[0]:
        drive = parts.pop(0) + "/"
    else:
        drive = ""
    
    # If the path is too long, we need to shorten it
    result = drive + parts[0] + "/.../" + parts[-1]
    
    # Remove parts from the middle until the length is acceptable
    while len(result) > max_length and len(parts) > 2:
        parts.pop(1)
        result = drive + parts[0] + "/.../" + parts[-1]
    
    # If it's still too long, truncate the last part
    if len(result) > max_length:
        part_length = max_length - len(drive) - 6  # 6 for "/.../"
        if part_length > 0:
            truncated_last_part = parts[-1][:part_length] + "..."
            result = drive + parts[0] + "/.../" + truncated_last_part
        else:
            result = drive + "..."
    
    return result

def maxsize():
    usage = round(psutil.disk_usage(get_system_partitions()[0]).percent, 2)
    try:
        MAX_INT = sys.maxsize
    except:
        MAX_INT = sys.maxint
    return round(MAX_INT / usage)


def get_system_partitions():
    platformname = platform.system().lower()
    if platformname == "windows":
        partitions = (
            os.popen("wmic logicaldisk get name")
            .read()
            .strip()
            .replace("\n", "")
            .split("\n")[1:]
        )
    elif platformname == "linux" or platformname == "unix" or platformname == "darwin":
        partitions = (
            os.popen("df -h | grep \"^/dev/\" | awk '{print $1}'")
            .read()
            .strip()
            .replace("\n", "")
            .split("\n")
        )
    else:
        partitions: List[Tuple[str]] = []
    if partitions:
        for i in rangeX(0, partitions.__len__() - 1):
            try:
                if partitions[i].__len__() > 0:
                    pass
                else:
                    del partitions[i]
            except:
                pass
    return partitions


def safe_load_json(json_string):
    try:
        # Memeriksa ukuran JSON
        if (
            json_string.__len__() > maxsize()
        ):  # Tetapkan batasan ukuran sesuai kebutuhan
            raise ValueError("JSON data too large")

        # Mengurai JSON
        data = json.loads(json_string)

        # Validasi struktur JSON
        if not isinstance(data, dict):  # Contoh validasi sederhana
            raise ValueError("Invalid JSON structure: expected a dictionary")

        return data
    except json.JSONDecodeError as e:
        pass
    except ValueError as e:
        pass
    except Exception as e:
        pass

    return None


def filter_json(data, keys):
    """
    Memfilter data JSON berdasarkan kunci yang diberikan.

    :param data: Data JSON yang akan difilter (dalam bentuk dict atau list).
    :param keys: Daftar kunci yang ingin diambil.
    :return: JSON yang sudah difilter sebagai string.
    """
    if isinstance(data, dict):
        return {k: data.get(k) for k in keys if k in data}
    
    elif isinstance(data, list):
        return [{k: item.get(k) for k in keys if k in item} for item in data]

#https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x64.exe
#https://download.microsoft.com/download/1/6/5/165255E7-1014-4D0A-B094-B6A430A6BFFC/vcredist_x86.exe
#https://download.microsoft.com/download/0/6/4/064F84EA-D1DB-4EAA-9A5C-CC2F0FF6A638/vc_redist.x64.exe
#https://download.microsoft.com/download/0/6/4/064F84EA-D1DB-4EAA-9A5C-CC2F0FF6A638/vc_redist.x86.exe