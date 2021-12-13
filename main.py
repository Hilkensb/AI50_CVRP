#!/usr/bin/env python3

# A supprimer !!!!
# Juste pour tester le programme facilement
from gui.app import Application
from utils.parseparameters import getOptions, SHOW_SOLUTION
import sys

def main():
    getOptions(sys.argv[1:])

    app = Application()
    app.run()

if __name__ == "__main__":
    main()
