import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
include_files = ['src/player.py', 'images/player.png']
build_exe_options = {"packages": [], "excludes": ["pyglet", "cocos2d", "coverage", "django", "docutils", "PyQt4", "numpy", "OpenGL", "PyOpenGL"], "include_files": include_files}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32Gui"

setup(name="Flappy Pong",
    version="0.1",
    description="Mixture of flappy and pong for MiniLD 58.",
    author="Jakov Manjkas",
    author_email="jakov.manjkas@gmail.com",
    options={"build_exe": build_exe_options},
    executables=[Executable('game.py', base=base)])
