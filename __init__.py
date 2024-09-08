import os, sys
if getattr(sys, 'frozen', False):
    # Jika aplikasi telah dibundel sebagai .exe
    __file__ = str(sys.executable)


encoded_dataOLD= "CiAgICB3ZWppX2liaWd5eHN2ID0gV2VqaVR2c2dpd3dJYmlneXhzdihxZWJfYXN2b2l2dz0yKQogICAgIyBHc3BwaWd4IGV2a3lxaXJ4IG1yanN2cWV4bXNyCiAgICB3ZWppX2liaWd5eHN2Lnd5ZnFteChxZW1yKQogICAgeG1xaS53cGlpdCh4bXFpc3l4X3oyKCkpCiAgICB3ZWppX2liaWd5eHN2LndseXhoc2FyKGFlbXg9WHZ5aSk=="
encoded_dataNOW= "CiAgICBxZW1yKCkKICAgIHhtcWkud3BpaXQoeG1xaXN5eF96MigpKQo=="

script_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
all_system_paths = ["/".join(script_dir.split("/")[:-1]), script_dir]
sys.path.extend(all_system_paths)
