import os, sys, platform, argparse, install

Platform = platform.platform().lower()
mainfile = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
cureentPath = os.getcwd()
os.chdir(mainfile)


def parser():
    parser = argparse.ArgumentParser(
        description="Handle folders with spaces and quotes"
    )

    # Argument untuk folder path
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder (can contain spaces)"
    )

    args = parser.parse_args()

    # Mengambil nilai folder_path dari argumen
    folder_path = args.folder_path
    return str(folder_path)


def main():
    deletefiles = os.path.join(mainfile, "MIT-LICENSE.txt")
    if os.path.isfile(deletefiles):
        try:
            os.unlink(deletefiles)
        except:
            os.remove(deletefiles)
    script, exeApp = os.path.join(mainfile, "supernano.py"), os.path.join(
        mainfile, "dist", "supernano.exe"
    )
    if os.path.isfile(exeApp):
        os.system(f"start {exeApp} {parser()}")
    elif os.path.isfile(script):
        os.system(f"{sys.executable} {script} {parser()}")
    else:
        install.install_script()


if __name__ == "__main__":
    main()
