git pull;
python3 manage.py collectstatic --no-input;
service uwsgi restart;
