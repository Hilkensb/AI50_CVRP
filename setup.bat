set /p pcommand=Python command to use (for exmaple: python)[Default to: python]:
IF NOT DEFINED MyVar SET "pcommand=python"
%pcommand% setup.py

echo %pcommand% main.py>./run.bat
