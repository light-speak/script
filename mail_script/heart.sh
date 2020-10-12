# /bin/bash
nohup python3 -u ~/script/heart.py -U $1 -W $2 -S $3 > nohup.out 2>&1 &
echo "ok"