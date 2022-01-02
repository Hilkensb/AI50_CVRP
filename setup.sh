chmod +x ./redis/Unix/redis-6.2.1/src/mkreleasehdr.sh
cd ./redis/Unix/redis-6.2.1/
make MALLOC=libc
cd ./../../../

read -p 'Python command to use (for exmaple: python3): ' pcommand
$pcommand setup.py

COUNTER_FILE="run.sh"
echo $pcommand" main.py" > $COUNTER_FILE
