# macommune
![Logo](mc_frontend/static/mc_frontend/img/logoaccueil_120.png)

- Source code of https://macommune.wikipedia.fr/
- See https://fr.wikipedia.org/wiki/Projet:Ma_Commune_Wikip%C3%A9dia

## Install
### Packages
- `apt install libmysqlclient-dev libffi-dev libssl-dev libssl-doc zlib1g-dev python3-dev python3-venv`

### Prepare database
- Connect to MySQL and create a database for the tool:
 
- `CREATE DATABASE macommune;`
- `CREATE USER 'macommune'@'localhost' IDENTIFIED BY 'password';`
- `GRANT ALL PRIVILEGES ON macommune.* TO 'macommune'@'localhost';`
- `ALTER DATABASE `macommune` CHARACTER SET utf8`; 
- `FLUSH PRIVILEGES;`

### Install the project

- `git clone` this repository somewhere and `cd` in.
- `cp config.ini.sample config.ini`
- Fill the config.ini file
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install wheel`
- `pip install -r requirements.txt`
- `python3 manage.py migrate`
- `python3 manage.py collectstatic`

### Launch it
 - `python3 manage.py runserver`
