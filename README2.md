
sudo apt-get update
pip install django
#Entrer dans le dossier dezippé
sudo apt install python3-virtualenv
virtualenv env


source env/bin/activate
pip install django
sudo apt-get install libffi-dev
pip install cffi
pip install psycopg2-binary
pip install psycopg2
pip install -r requirements.txt

py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser # Cette commande permet de creer un username et un mot de passe pour pouvoir se connecter en tant qu'admin 
py manage.py runserver





