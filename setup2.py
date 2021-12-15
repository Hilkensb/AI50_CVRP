##ce code permet de faire l'executable
import sys
import os
import cx_Freeze
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

setup(
      name = "AI50 - CVRP project",
      version = "0.1",
      description = "Find solution and optimization for CVRP",
      options = {'build_exe' : {
        'build_exe': './/build'
    }},
      executables = [Executable("main.py",base=base)]
      )
