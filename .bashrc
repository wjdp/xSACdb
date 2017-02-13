NAME=`python /app/bin/name.py`

python /app/bin/announce.py

cd /app
source env/bin/activate
export PS1="\[$(tput setaf 3)\][xSACdb:$NAME] \W>\[$(tput sgr0)\] "
alias manage=src/manage.py
