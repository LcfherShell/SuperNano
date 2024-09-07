import os, sys
if getattr(sys, 'frozen', False):
    # Jika aplikasi telah dibundel sebagai .exe
    __file__ = str(sys.executable)

script_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
all_system_paths = ["/".join(script_dir.split("/")[:-1]), script_dir]
sys.path.extend(all_system_paths)
