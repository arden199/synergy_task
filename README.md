Firstly make this command to create database with test data:
mysql -u root -p < mycourse.sql

Then run this command:
python manage.py runserver

=======================================================================================
As database I use MariaDB
Keep in mind that you have to install modules that are in requirements.txt file.
Also you should know that Django use code standard which slightly different from PEP8.
For example Django 119 symbols in line vs PEP8 79.

