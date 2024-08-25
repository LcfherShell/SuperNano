import os, ctypes, logging
try:
    from .errrorHandler import complex_handle_errors
except:
    try:
        from errrorHandler import complex_handle_errors
    except:
        from libs.errrorHandler import complex_handle_errors

@complex_handle_errors(loggering=logging, nomessagesNormal=False)
def set_console_title(title):
    """Mengatur judul jendela Command Prompt."""
    ctypes.windll.kernel32.SetConsoleTitleW(title)

@complex_handle_errors(loggering=logging, nomessagesNormal=False)
def get_console_title():
    """Mendapatkan judul jendela Command Prompt."""
    # Buffer untuk menyimpan judul
    buffer_size = 256
    buffer = ctypes.create_unicode_buffer(buffer_size)
    
    # Memanggil fungsi API Windows untuk mendapatkan judul jendela
    ctypes.windll.kernel32.GetConsoleTitleW(buffer, buffer_size)
    
    return buffer.value