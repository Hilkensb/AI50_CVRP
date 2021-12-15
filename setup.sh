read -p 'Python command to use (for exmaple: python3): ' pcommand
$pcommand setup.py

COUNTER_FILE="run.sh"
echo $pcommand" main.py" > $COUNTER_FILE
