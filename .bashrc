NAME=`python3 /app/bin/name.py`

python /app/bin/announce.py

cd /app
export PS1="\[$(tput setaf 3)\][xSACdb:$NAME] \W>\[$(tput sgr0)\] "
alias manage=src/manage.py
