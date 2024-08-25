try:
    from .helperegex import fullmacth
except:
    from helperegex import fullmacth

from os import getppid, getenv
import os, subprocess, threading, time, psutil, ctypes
from functools import lru_cache
from ctypes import wintypes
try:
    from GPUtil import getGPUs
except:
    def getGPUs():
        # Contoh fungsi untuk mendapatkan penggunaan GPU
        # Implementasi nyata bergantung pada library dan hardware yang digunakan
        # Untuk sekarang kita kembalikan None, artinya GPU tidak digunakan
        return None

def yime():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent()
    
    # Get GPU usage percentage if available
    gpu_usage = getGPUs()
    
    if gpu_usage is not None:
        usage = gpu_usage
    else:
        usage = cpu_usage

    # Get RAM usage percentage
    ram_usage = psutil.virtual_memory().percent

    # Determine the divisor based on usage level
    if usage > 50:
        cpu_usage_divided = usage / 20  # Higher divisor for higher usage
    else:
        cpu_usage_divided = usage / 10  # Lower divisor for lower usage

    if ram_usage > 50:
        ram_usage_divided = ram_usage / 20  # Higher divisor for higher usage
    else:
        ram_usage_divided = ram_usage / 10  # Lower divisor for lower usage

    # Adjust for very low usage values
    if cpu_usage_divided < 0.1:
        cpu_usage_divided *= 2
    if ram_usage_divided < 0.1:
        ram_usage_divided *= 2

    # Calculate average usage and return
    data = [round(cpu_usage_divided, 1), round(ram_usage_divided, 1)]
    outputdata = round(sum(data) / len(data), 1) / 2
    if outputdata>0.9:
        pass
    else:
        outputdata = 1
    return outputdata

class metablocks(type):
    def __setattr__(self, name, value):
        raise ValueError(name)


class detectcommand(metaclass=metablocks):
    def __init__(self):
        try:
            #from psutil import Process

            #self.shell = Process(getppid()).name().lower()
            x, self.shell = get_console_process_name()
        except:
            process = subprocess.Popen(
                ["tasklist", "/fi", f"PID eq {getppid()}", "/fo", "csv", "/nh"],
                stdout=subprocess.PIPE,
            )
            stdout, _ = process.communicate()
            self.shell = stdout.decode().strip().split(",")[0].strip('"').lower()

    def __dir__(self):
        pass

    def __repr__(self) -> str:
        return self.shell

    @property
    def isPowershell(self):
        isPowershell = False
        if fullmacth(
            r"pswh|pswh.*|pswh.exe|pswh.*.exe|powershell.exe|powershell.*.exe",
            self.shell,
        ):
            isPowershell = True
        return isPowershell

    @property
    def iscmd(self):
        iscmd = False
        if fullmacth(r"cmd|cmd.*|cmd.exe|cmd.*.exe", self.shell):
            iscmd = True
        return iscmd

    @property
    def ispy(self):
        ispy = False
        if fullmacth(
            r"py.*|py.exe|py.*.exe|python.*|python.*.exe|python.exe", self.shell
        ):
            ispy = True
        return ispy

    @property
    def isbash(self):
        checkbash = (
            self.shell.count("bash")
            or self.shell.count("sh")
            or self.shell.count("dash")
            or self.shell.count("ash")
        )
        return checkbash != 0

    def commands(self):
        parent_process = getenv("PROCESSOR_IDENTIFIER", "")

    @lru_cache(maxsize=10)
    def auto(self):
        check = ["isPowershell", "iscmd", "ispy", "isbash"]
        xx_output = {}

        for values in check:
            xcmd = eval("self.{cmd}".format(cmd=values))
            if xcmd == True:
                xx_output["type_command"] = values
                break
        return xx_output


def stream_output(pipe, name):
    for line in iter(pipe.readline, ""):
        print(f"{line.strip()}")
    pipe.close()

@lru_cache(maxsize=10)
def stream_command_output(command: str):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )

    stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, ""))
    stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, ""))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    return process.poll()

@lru_cache(maxsize=10)
def run_powershell_command_as_admin(command):
    # Command to run PowerShell as administrator and execute the given command
    # ps_command = f'powershell -Command "Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -Command {command}\' -WindowStyle Hidden"'

    # Execute the command
    # result = subprocess.call(ps_command, shell=True)
    # Run the command and capture the output
    
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        capture_output=True,
        text=True,
    )

    # Ambil output dari perintah PowerShell
    if result:
        return result.stdout or result.stderr

    return False

@lru_cache(maxsize=10)
def run_powershell_File_as_admin(command: str):
    # Command to run PowerShell as administrator and execute the given command
    # ps_command = f'powershell -Command "Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -Command {command}\' -WindowStyle Hidden"'

    # Execute the command
    # result = subprocess.call(ps_command, shell=True)
    # Run the command and capture the output
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", command],
        capture_output=True,
        text=True,
    )

    # Ambil output dari perintah PowerShell
    if result:
        return result.stderr or result.stdout

    return False

@lru_cache(maxsize=10)
def run_cmd_command_as_admin(command: str):
    # Command to run commandprompt as administrator and execute the given command
    # Execute the command
    # Run the command and capture the output

    command = f"powershell -Command \"Start-Process cmd -ArgumentList \'/c {command}' -Verb runAs -WindowStyle Hidden\""
    time.sleep(2)
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Ambil output dari perintah PowerShell
    if result:
        return True
    return False

@lru_cache(maxsize=10)
def checkcommand(command: str, timeout=None):
    # Mulai proses
    ps = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    # Fungsi untuk menunggu proses selesai
    def target():
        try:
            ps.communicate()
        except Exception as e:
            print(f"Error: {e}")

    ouputs = 0
    # Buat dan mulai thread
    thread = threading.Thread(target=target)
    thread.start()

    # Tunggu sampai selesai atau timeout
    thread.join(timeout)
    if thread.is_alive():
        ps.kill()  # Mengirim sinyal penghentian
        thread.join()  # Tunggu sampai thread selesai
        ouputs = 1
    if ouputs:
        ouputs = 0
    return ouputs

@lru_cache(maxsize=10)
def checkcommandV2(command: str, timeout: int=0) -> str:
    """
    Menjalankan perintah dengan batasan waktu menggunakan thread.
    Jika perintah melebihi waktu yang ditentukan, proses akan dihentikan secara paksa.

    Args:
        command (str): Perintah yang akan dijalankan.
        timeout (int): Waktu maksimum (dalam detik) untuk menjalankan perintah.
    
    Returns:
        str: Output dari perintah jika berhasil, atau pesan error jika proses dihentikan atau gagal.
    """
    if timeout <= 0:
        timeout = round(yime())*2
    def target():
        nonlocal result, process
        try:
            process = subprocess.Popen(
                "powershell -Command {command}".format(command=command),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            result = (process.returncode, stdout, stderr)
        except Exception as e:
            result = e

    result = None
    process = None
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # Proses melebihi waktu yang ditentukan, hentikan secara paksa
        if process is not None:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):  # Membunuh semua child processes
                child.kill()
            parent.kill()
        thread.join()  # Pastikan thread selesai
        return result

    if isinstance(result, tuple):
        returncode, stdout, stderr = result
        if returncode == 0:
            return result
        else:
            return result
    elif isinstance(result, Exception):
        return (1, None, None)
    else:
        return (1, None, None)
    
@lru_cache(maxsize=10)
def checkcommandPrompt(command: str, timeout: int=0) -> str:
    """
    Menjalankan perintah dengan batasan waktu menggunakan thread.
    Jika perintah melebihi waktu yang ditentukan, proses akan dihentikan secara paksa.

    Args:
        command (str): Perintah yang akan dijalankan.
        timeout (int): Waktu maksimum (dalam detik) untuk menjalankan perintah.
    
    Returns:
        str: Output dari perintah jika berhasil, atau pesan error jika proses dihentikan atau gagal.
    """
    if timeout <= 0:
        timeout = round(yime())*2
    def target():
        nonlocal result, process
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            result = (process.returncode, stdout, stderr)
        except Exception as e:
            result = e

    result = None
    process = None
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        # Proses melebihi waktu yang ditentukan, hentikan secara paksa
        if process is not None:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):  # Membunuh semua child processes
                child.kill()
            parent.kill()
        thread.join()  # Pastikan thread selesai
        return result

    if isinstance(result, tuple):
        returncode, stdout, stderr = result
        if returncode == 0:
            return result
        else:
            return result
    elif isinstance(result, Exception):
        return (1, None, None)
    else:
        return (1, None, None)
    
def get_console_process_name():
    """
    Mengembalikan nama proses yang menjalankan konsol saat ini (cmd atau powershell).
    """
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    psapi = ctypes.windll.psapi

    # Mendapatkan handle dari jendela konsol saat ini
    hwnd = kernel32.GetConsoleWindow()
    if not hwnd:
        return None

    # Mendapatkan ID proses dari jendela konsol
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    # Membuka proses untuk membaca informasi
    h_process = kernel32.OpenProcess(0x1000, False, pid.value)
    if not h_process:
        return None

    # Mendapatkan nama file dari proses
    exe_name = ctypes.create_string_buffer(512)
    psapi.GetModuleFileNameExA(h_process, None, exe_name, 512)
    kernel32.CloseHandle(h_process)

    head, tail = os.path.split(exe_name.value.decode('utf-8'))
    return head, tail


def restart_powershell_as_admin():
    """
    Merestart PowerShell dalam mode administrator, memulai proses PowerShell baru, dan menjalankan file Python itu sendiri.
    """
    def is_admin():
        """
        Mengecek apakah skrip dijalankan dengan hak administrator.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    try:
        # Dapatkan path file Python saat ini
        script_path = os.path.abspath(__file__)

        # Perintah untuk menjalankan PowerShell sebagai administrator dan menjalankan file Python ini
        command = f'Start-Process powershell -ArgumentList \'-NoExit -Command "Start-Sleep -Seconds 1; Set-Location -Path \'{os.getcwd()}\'; python \\"{script_path}\\" "\'\' -Verb RunAs'

        # Jalankan perintah menggunakan subprocess
        subprocess.run(["powershell", "-Command", command], shell=True)

        # Keluar dari proses Python saat ini
        os._exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")


detectcommandprompt = detectcommand()
#print(detectcommandprompt.auto())


#####################


def get_current_directory_partition(current_dir:str):
    partitions = psutil.disk_partitions()
    current_dir = current_dir.replace("\\", "/")
    for partition in partitions:
        if current_dir.lower().startswith(partition.mountpoint.lower().replace("\\", "/")):
            return get_detailed_partition_info(partition)
    
    return None

def get_detailed_partition_info(partition):
    usage = psutil.disk_usage(partition.mountpoint)
    return {
        'device': partition.device,
        'mountpoint': partition.mountpoint,
        'fstype': partition.fstype,
        'total': usage.total,
        'used': usage.used,
        'free': usage.free,
        'percent': usage.percent
    }



if __name__ == "__main__":
    command = "$pass = Read-Host '{command}' -AsSecureString; $plainTextPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)); Write-Output $plainTextPass".format(command="prompt")  # Contoh perintah Python yang tidur selama 60 detik
    #timeout = round(yime())  # Waktu maksimum yang diizinkan (dalam detik)
    
    start_time = time.time()
    output = checkcommandV2(command)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"Output:\n{output}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")