# Reads manifest.py files and generates mpremote cp command list to copy source files to filesystem

import os
import re
import subprocess

BOARD_DIR_RE = re.compile(r"\$\(BOARD_DIR\)")
PORT_DIR_RE = re.compile(r"\$\(PORT_DIR\)")
MPY_DIR_RE = re.compile(r"\$\(MPY_DIR\)")
# MPY_LIB_DIR_RE = re.compile(r"\$\(MPY_LIB_DIR\)")

dirs = {
    "BOARD_DIR": os.environ["BOARD_DIR"],
    "PORT_DIR": os.environ["PORT_DIR"],
    "MPY_DIR": os.environ["MPY_DIR"],
    "MANIFEST_DIR": os.getcwd()
}

MANIFEST_DIR = None
MPY_DIR = None
PORT_DIR = None
BOARD_DIR = None

def manifest_relative_path(path):
    """
    Return the path if absolute, or if relative, relative to the manifest directory.
    """
    global MANIFEST_DIR
    if os.path.isabs(path):
        return path
    else:
        return os.path.join(MANIFEST_DIR, path)


def copy_file(src, dest):
    """
    Copy a file from src (on the host) to dest (on the device).
    Uses 'mpremote cp' to copy files.
    """
    src = manifest_relative_path(src)
    # subprocess.run(["mpremote", "cp", src, ":" + dest])
    print(f"mpremote cp {src} :{dest}")


def freeze(path):
    """
    Recursively copy all.py files in path to the root of the firmware.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                copy_file(os.path.join(root, file))


def include(path):
    """
    Recursively copy all.py files in path to the root of the firmware.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                copy_file(os.path.join(root, file))


def require(path):
    """
    Use "mpremote mip install" to install the given library
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                copy_file(os.path.join(root, file))


def package(package_path, files=None, base_path=".", opt=None):
    """
    Copy files from package_path to /lib/package_path.
    """
    for file in files:
        copy_file(os.path.join(base_path, file),
                  os.path.join("/lib", package_path))


def module(module_path, base_path=".", opt=None):
    """
    Include a single Python file as a module in the root of the filesystem.
    """
    copy_file(os.path.join(base_path, module_path),
              os.path.join("/", module_path))



def read_manifest_file(path):
    """
    Read the given manifest file, translating the 
    BOARD_DIR, PORT_DIR, and MPY_DIR variables.
    Return a string.
    """
    data = open(path).read()
    data = BOARD_DIR_RE.sub(BOARD_DIR, data)
    data = PORT_DIR_RE.sub(PORT_DIR, data)
    data = MPY_DIR_RE.sub(MPY_DIR, data)
    return data


def run_manifest_file(path):
    """
    Run the given manifest file, translating the
    BOARD_DIR, PORT_DIR, and MPY_DIR variables.
    """
    exec(read_manifest_file(path))
