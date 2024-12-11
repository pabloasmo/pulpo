# Pulpo
Pulpo is a web application that allows users to track their multimedia content (such as movies, anime, series, etc.) and their progress. It uses Django as the framework and SQLite as the database.

# Setup for development
0. *(optional)* Create Python environment:
```sh
python -m venv .venv
source .venv/bin/activate
```
1. Install required packages:
```sh
pip install -r requirements.txt
```
2. Run migrations inside "pulpo_project" folder:
```sh
cd pulpo_project/
python manage.py migrate
python manage.py makemigrations
```
3. Run server:
```sh
python manage.py runserver
```
