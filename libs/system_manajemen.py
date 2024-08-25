import signal
import sys
import psutil
import os
import threading
import time
import multiprocessing, signal
from concurrent.futures import ProcessPoolExecutor, as_completed

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()  # Mengirim sinyal untuk menghentikan proses
        process.wait(timeout=3)  # Menunggu proses benar-benar berhenti
    except psutil.NoSuchProcess:
        os._exit(0)
    except psutil.TimeoutExpired:
        os._exit(0)


def set_low_priority(pid):
    def signal_handler(signum, frame):
        if signum == signal.SIGINT:  # Ctrl+C
            print("[INFO] Detected Ctrl+C. Shutting down gracefully...")
            terminate_process(pid)
        # SIGTSTP handling only if available
        elif signum == getattr(signal, 'SIGTSTP', None):  # Ctrl+Z (Unix-like only)
            print("[INFO] Detected Ctrl+Z. Process suspended.")
            terminate_process(pid)
            
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTSTP'):
        signal.signal(signal.SIGTSTP, signal_handler)

    if os.name == 'nt':
        process = psutil.Process(pid)
        process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    else:  # Unix-like systems
        os.nice(19)
        
        
def initializer(stop_event):
    global stop_flag
    stop_flag = stop_event
    signal.signal(signal.SIGINT, handle_child_signal)

def handle_child_signal(signum, frame):
    print(f"Child process received signal {signum}.")
    stop_flag.set()

class SafeProcessExecutor:
    def __init__(self, max_workers=None):
        # Membuat Event menggunakan Manager untuk sinkronisasi antar proses
        self.manager = multiprocessing.Manager()
        self.stop_flag = self.manager.Event()
        self.executor = ProcessPoolExecutor(
            max_workers=max_workers,
            initializer=initializer,
            initargs=(self.stop_flag,)
        )
        self.futures = []

    def submit(self, fn, *args, **kwargs):
        """Submit a function to the executor for execution."""
        future = self.executor.submit(fn, *args, **kwargs)
        self.futures.append(future)
        return future

    def shutdown(self, wait=True):
        """Shut down the executor and terminate all running processes."""
        self.stop_flag.set()  # Menghentikan semua proses yang sedang berjalan
        self.executor.shutdown(wait=wait)

    def get_results(self):
        """Get results from all completed futures."""
        results = []
        for future in as_completed(self.futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(f"Error retrieving result: {e}")
        return results
