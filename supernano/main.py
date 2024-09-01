import os, sys, platform, argparse
try:
  from supernano import install
except:
  try:
    from .supernano import install
  except:
    import install

Platform = platform.platform().lower()
mainfile = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
cureentPath = os.getcwd()
os.chdir(mainfile)



def parser():
    parser = argparse.ArgumentParser(description="Handle folders with spaces and quotes")
    
    # Argument untuk folder path
    parser.add_argument(
        'folder_path', 
        type=str, 
        help="Path to the folder (can contain spaces)"
    )
    
    args = parser.parse_args()
    
    # Mengambil nilai folder_path dari argumen
    folder_path = args.folder_path
    return folder_path


def main():
    deletefiles = os.path.join(mainfile, "MIT-LICENSE.txt")
    if os.path.isfile(deletefiles):
        try:
            os.unlink(deletefiles)
        except:
            os.remove(deletefiles)
    if os.path.isfile( os.path.join(mainfile, "supernano.py")):
        script = os.path.join(mainfile, "supernano.py")
        os.system(f'{sys.executable} {script} {parser()}')
    else:
        install.install_script()

if __name__ == "__main__":
    main()
