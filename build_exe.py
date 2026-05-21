import PyInstaller.__main__
import sys
import os

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

PyInstaller.__main__.run([
    "run.py",
    "--onefile",
    "--name=axioma",
    "--distpath=" + output_dir,
    "--clean",
    "--noconfirm",
    "--console",
])
