import re, os, string, psutil, random
from functools import lru_cache
from typing import List, Tuple, TypeVar, Generic, Any
try:
    from itertools import izip as zip

    range = xrange
except:
    pass

def analyze_line(line):
    """
    Analyzes a line of text to determine if it contains assignment or comparison.

    Parameters:
    - line (str): The line of text to analyze.

    Returns:
    - str: Description of the line content.
    """
    # Regex pattern to find single '=' (assignment) and multiple '=' (comparison)
    assignment_pattern = re.compile(r'^\s*[$]?\w+\s*=\s*.*$') #re.compile(r'^\s*\w+\s*=\s*.*$')
    comparison_pattern = re.compile(r'==|>=|<=|!=|>|\<')

    # Check for assignment
    if assignment_pattern.match(line):
        # Further check if it contains comparison operators
        if comparison_pattern.search(line):
            return 0
        else:
            return 1
    else:
        return 0


def rremovelist(data: list):
    unicude = {}.fromkeys(data)
    return list(unicude)[::-1]


def remove_duplicates_from_right(lst: list):
    seen = set()
    result: List[Tuple[str, int, Any]] = []

    # Iterasi dari akhir ke awal
    for item in reversed(lst):
        if item not in seen:
            seen.add(item)
            result.append(item)

    # Membalikkan hasil untuk mempertahankan urutan awal
    result.reverse()

    # Buat list akhir dengan mempertahankan posisi index
    final_result: List[Tuple[str, int, Any]] = []
    seen.clear()

    for item in lst:
        if item in result and item not in seen:
            final_result.append(item)
            seen.add(item)

    return final_result

def lremove_duplicates_from_left(lst: list, limit: int = 1, total: int = 0):
    removal_count = 0
    result: List[Tuple[str, int, Any]] = []
    if total == 0:
        total = round(lst.__len__() / 2)
        if total % 2 == 0:
            total = int(total / 2)
        elif total % 3:
            total = round(total / 2)
        else:
            pass
    if lst.__len__() > limit + total:
        for item in lst:
            if removal_count < limit:
                removal_count += 1
            else:
                result.append(item)
    else:
        result = lst
    return result

#clean 
def clean_string(strings, regex, newstring):
    s = re.sub(regex, newstring, strings)
    # Hapus spasi putih di awal dan akhir string
    s = s.strip()
    return s

# Fungsi ini menghapus karakter terakhir didalam input string

def remove_laststring(data, spec, new=""):
    maxreplace = data.count(spec) - 1
    return new.join(data.rsplit(spec, maxreplace))


# Fungsi ini mereplace karakter terakhir didalam input string dan menggantikannya dengan karakter baru

def rreplace(s:str, old:str, new:str, count:int):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]


# Fungsi ini mereplace karakter berdasarkan posisi didalam input string dan menggantikannya dengan karakter baru

def replaceusinglenght(data: str, lenght: int):
    return data[-data.__len__() : data.__len__() - lenght]


# Fungsi ini mereplace satu kata atau karakter berdasarkan posisi didalam input string dan menggantikannya dengan karakter baru

def replace_char_at_position(s, position, new_char):
    if position < 0 or position >= len(s):
        return s

    # Create a new string with the character replaced
    new_string = s[:position] + new_char + s[position + 1 :]

    return new_string


# Fungsi ini mereplace semua kata atau karakter berdasarkan posisi didalam input string dan menggantikannya dengan karakter baru menggunakan regex

def replacebypost(data: str, new_character: str, regex=r"\((.*)\)"):
    for position in re.finditer(regex, data):
        if position:
            if (isinstance(position, list) and position.__len__() == 2) or (
                isinstance(position, tuple) and position.__len__() == 2
            ):
                data = (
                    data[: position[0]] + new_character + data[position[1] :].strip()
                )  # data[position[1]+1:]
    return data


# Fungsi ini untuk memanipulasi string dengan mengganti karakter khusus tertentu dengan karakter lain, kecuali karakter yang berada dalam tanda kutip.

def cleanstring(data: str, spec: str, place: str, maximun=None, xplace=""):
    """
    data: String input yang akan diproses.
    spec: Karakter khusus yang akan diganti.
    place: Karakter pengganti untuk spec.
    maximun: Batas maksimum jumlah penggantian.
    xplace: Karakter pengganti sementara untuk spec di luar tanda kutip."""

    sessionplace: List[Tuple[str]] = ["", ""]  # yang satu kalimat asli dan satunya kalimat pengganti
    if "$(-%places%-)" in data:
        numb, stop = 0, True
        while stop != False:
            places = "$(-%places%-{number})".format(number=str(numb))
            if stop != False and places not in data:
                data = data.replace("$(-%places%-)", places)
                sessionplace[0] = "$(-%places%-)"
                sessionplace[1] = places
                stop = False
                break
            numb += 1
        numb = 0

    try:
        select_x = re.findall(r"\"(.*?)\"", data.strip()) or re.findall(
            r"'(.*?)'", data.strip()
        )
        if select_x.__len__() != 0:
            # mob = data.replace(spec, "${place}".format(place=place))
            for xe in select_x:
                new = xe.replace(spec, "$(-%places%-)")
                data = data.replace(xe, new)

            # replacebypost(regex=r"$\((.*)\)")
            if isinstance(maximun, int):
                maxcount = data.count("$(-%places%-)")
                if maximun > 0 and maximun <= maxcount:
                    data = data.replace(spec, "").replace(
                        "$(-%places%-)", place, maximun
                    )
            else:
                data = data.replace(spec, xplace).replace("$(-%places%-)", place)
        else:
            if maximun == None:
                maximun = int(data.count(spec))
            data = data.replace(spec, xplace, maximun)
    except:
        pass

    if sessionplace[1].__len__() > 1:
        data = data.replace(sessionplace[1], sessionplace[0])
    return data


def fullmacth(macth, data):
    return re.fullmatch(macth, data)


def searching(patternRegex, data: str):
    # Define the regex pattern to match the function name
    pattern = re.compile(patternRegex)

    # Search for the pattern in the function definition
    match = pattern.search(data)

    # If a match is found, return the function name
    if match:
        return match.group(1)
    else:
        return None
        
def split_from_right_with_regex(text, pattern, maxsplit:int=-1):
    # Menggunakan re.split() untuk membagi string
    try:
        parts = re.split(pattern, text)
        # Jika maxsplit diatur, batasi jumlah split dari kanan
        if maxsplit > 0:
            # Membalikkan hasil split untuk memproses dari kanan ke kiri
            parts.reverse()
            # Batasi split dan balikkan kembali
            limited_parts = parts[:maxsplit+1]
            limited_parts.reverse()
            return limited_parts
        else:
            return parts
    except:
        return text.rsplit(pattern, maxsplit=maxsplit)
        
####menemkan karakter diluar  tanda kutipp
def count_character_outside_quotes(input_string, character):
    """
    Count occurrences of a specified character outside of quotes.

    Parameters:
    - input_string (str): The input string to process.
    - character (str): The character to count.

    Returns:
    - int: The number of occurrences of the character outside quotes.
    """
    inside_quotes = False
    count = 0
    quote_char = ''
    
    for i, char in enumerate(input_string):
        if char in ('"', "'"):
            if not inside_quotes:
                # Entering a quoted section
                inside_quotes = True
                quote_char = char
            elif char == quote_char:
                # Exiting a quoted section
                inside_quotes = False
        elif char == character and not inside_quotes:
            count += 1
    
    return count


##### menghitung spasi sebelum karakter
def count_leading_spaces(line):
    """
    Count the number of leading spaces in a given string.

    Parameters:
    - line (str): The string to check.

    Returns:
    - int: The number of leading spaces.
    """
    match = re.match(r'^\s*', line)
    if match:
        return len(match.group(0))
    return 0

# Menemukan posisi text didalam variable string dengan mencocokan pola menggunakan regex dan menyimpannya kedalam tuple

def findpositions(regex, string: str):
    """
    regex: Pola regex yang digunakan untuk menemukan teks
    string: String input yang akan diproses.
    """
    postion_list: List[Tuple[str, int, Any]] = []
    try:
        compiles = re.compile(regex, re.IGNORECASE)
        for match in compiles.finditer(string):
            if match:
                # postion_list.append( (match.group(), match.span()))
                postion_list.append(zip([match.group()], [match.span()]))
    except:
        for match in re.finditer(regex, string):
            if match:
                # postion_list.append( (match.group(), match.span()))
                postion_list.append(zip([match.group()], [match.span()]))
    return tuple(postion_list)


# findpostion("'(.*?)?'", "'sssss' hshs 'cbcbcbc'")


def split(regex, string: str, inject: str = "", post: list = [], mode: bool = False):
    result: List[Tuple[str, int, Any]] = []
    if isinstance(regex, list) or isinstance(regex, tuple):
        indices = list(regex)
        if mode == False:
            if indices.count(None) >= 1:
                if indices[-1:][0] == None:
                    pass
                else:
                    indices.append(None)
            else:
                indices.append(None)
            result = [string[i:j] for i, j in zip(indices, indices[1:])]
        else:
            if indices[0] == 0:
                pass
            else:
                indices.remove(0)
                indices.insert(0, 0)
            if indices[-1:][0] == string.__len__():
                pass
            else:
                indices.append(string.__len__())
            indices = sorted(set(indices))
            result = [string[x:y] for x, y in zip(indices, indices[1:])]

    elif isinstance(regex, str):
        try:
            if string.count(regex) > 1:
                position = findpositions(regex=regex, string=string)
                if position.__len__() != 0:
                    all_lines: List[Tuple[str, int, Any]] = []
                    for x in position:
                        for c in x:
                            all_lines.append(c[1][0])
                    if all_lines.__len__() != 0:
                        x = split(all_lines, string, mode=True)
                        if regex.count(" ") != 0:
                            for y in range(x.__len__()):
                                x[y] = x[y].replace(regex, "")
                        else:
                            for y in range(x.__len__()):
                                x[y] = x[y].replace(regex, "")

                        x = list(filter(lambda v: v != "", x))
                        result = x
                else:
                    assert 12 == 11
            else:
                try:
                    position = findpositions(regex=regex, string=string)
                    if position.__len__() != 0:
                        all_lines, textsearch = [[], []]
                        for x in position:
                            for c in x:
                                all_lines.append(c[1][0])
                                textsearch.append(c[0])
                        if all_lines.__len__() != 0:
                            x = split(all_lines, string, mode=True)
                            for y in range(x.__len__()):
                                for regex in textsearch:
                                    x[y] = x[y].replace(regex, "")

                            result = x
                    else:
                        assert 12 == 11
                except:
                    m = re.search(regex, string)
                    result = [string[: m.start()], string[m.end() :]]
        except:
            result = string.split(str(regex))
    elif isinstance(regex, int):
        result = string[:regex], string[regex:]
    else:
        return

    result = list(filter(lambda x: x != "", result))
    if post.__len__() != 0:
        if inject:
            lenght = result.__len__()
            for p in post:
                if p > lenght:
                    result.insert(lenght, inject)
                else:
                    result.insert(p, inject)

    return result


# Fungsi ini cukup efisien dalam menemukan semua posisi di mana substring dimulai dalam string lengkap, dengan menggunakan pendekatan langsung dan fallback regex jika diperlukan.

def find_indices_of_substring(full_string, sub_string):
    return [
        index
        for index in range(len(full_string))
        if full_string.startswith(sub_string, index)
    ] or [m.start() for m in re.finditer(re.escape(sub_string), full_string)]


def searchmissing(s, t):
    """
    s: Kalimat input yang ingin dibandingkan.
    t: Kalimat input yang ingin dibandingkan.
    \ncontoh:
    s = "I like eating apples and bananas"
    t = "I apples bananas"
    missing_words = searchmissing(s, t)
    print(missing_words)  # Output: ['like', 'eating', 'and']
    """
    res: List[Tuple[str, int, Any]] = []  # Daftar untuk menyimpan kata-kata yang hilang
    t_words = t.split()  # Memecah string `t` menjadi daftar kata
    s_words = s.split()  # Memecah string `s` menjadi daftar kata
    size = s_words.__len__()  # Mendapatkan jumlah kata dalam `s`
    i = 0  # Indeks untuk melacak kata dalam `t`
    j = 0  # Indeks untuk melacak kata dalam `s`
    for j in range(size):
        if s_words[j] == t_words[i]:
            i += 1  # Jika kata dalam `s` sama dengan kata dalam `t`, pindah ke kata berikutnya di `t`
            if i >= t_words.__len__():
                break  # Jika semua kata dalam `t` ditemukan, hentikan loop
        else:
            res.append(
                s_words[j]
            )  # Jika kata dalam `s` tidak ada di `t`, tambahkan ke hasil
    # Tambahkan kata-kata yang tersisa dalam `s` setelah indeks `j`
    for k in range(j + 1, size):
        res.append(s_words[k])
    return res  # Kembalikan daftar kata yang hilang


def split_by_length(s, length):
    # Create a list to store the split parts
    parts: List[Tuple[str, int, Any]] = []

    # Loop through the string, incrementing by the length each time
    for i in range(0, len(s), length):
        parts.append(s[i : i + length])

    return parts

def find_regex_in_list(pattern, lst: list, limit: int = None):
    # Compile the regex pattern
    regex = re.compile(pattern, re.IGNORECASE)

    # List to store the positions
    positions: List[Tuple[str, int, Any]] = []

    # Iterate through the list and search for the pattern
    for i, item in enumerate(lst):
        if limit == 0:
            break
        if regex.search(item):
            positions.append(i)

        if limit != None and limit != 0:
            limit -= 1
    return positions


def find_and_split(text, pattern):
    """
    Menemukan teks setelah pola tertentu dan membagi string satu kali berdasarkan pola tersebut.
    :param text: String input yang akan diproses
    :param pattern: Pola regex yang digunakan untuk menemukan teks
    :return: Tuple yang berisi dua bagian string yang dipisahkan oleh pola
    """
    match = re.search(pattern, text)
    if match:
        # Menemukan posisi akhir dari pola yang cocok
        split_pos = match.end()
        # Memisahkan string satu kali berdasarkan posisi akhir dari pola yang cocok
        part1 = text[:split_pos]
        part2 = text[split_pos:]
        return part1, part2
    else:
        return text, None


# Fungsi mengembalikan daftar posisi karakter yang berada di luar kutipan.

def find_unquoted_brace_positions(text, searchchar):
    positions: List[Tuple[int, Any]] = []
    in_single_quote = False
    in_double_quote = False

    for i, char in enumerate(text):
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == searchchar and not in_single_quote and not in_double_quote:
            positions.append(i)

    return positions

def extract_quoted_text(text):
    # Pola regex untuk menemukan teks di dalam tanda kutip tunggal atau ganda
    pattern = r'(["\'])(.*?)(\1)'
    matches = re.findall(pattern, text)
    
    # Mengambil hanya teks di dalam tanda kutip
    quoted_texts = [match[1] for match in matches]
    return quoted_texts

def reversed(datalist: list | tuple):
    process = datalist[::-1]
    return process

def reindent_function_blocks(input_string):
    """
    Re-indent function blocks in the given string.

    Parameters:
    - input_string (str): The input string containing function blocks.

    Returns:
    - str: The re-indented string.
    """
    def indent_lines(match):
        """
        Indent lines within a function block.
        """
        lines = match.group(0).splitlines()
        indented_lines = [lines[0]]  # Keep the function declaration line
        indented_lines += ["    " + line if line.strip() else "" for line in lines[1:]]
        return "\n".join(indented_lines)

    # Use regex to find function blocks and apply indentation
    pattern = re.compile(r'function|class\s+\w+\s*\{[^{}]*\}', re.DOTALL)
    result = re.sub(pattern, indent_lines, input_string)

    return result

def add_indent_to_lines(text, indent='  '):
    """
    Add a specified indentation to each line of a given text.

    Parameters:
    - text (str): The input text to be indented.
    - indent (str): The string to use as indentation (default is 4 spaces).

    Returns:
    - str: The text with added indentation.
    """
    # Split text into lines
    lines = text.splitlines()
    
    # Add indentation to each line
    indented_lines = [indent + line for line in lines]
    
    # Join lines back into a single string
    indented_text = '\n'.join(indented_lines)
    
    return indented_text
