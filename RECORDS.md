# Installing frameworks / libaries
**Django and gunicorn**
```
pip3 install 'django<4' gunicorn
```
*gunicorn is the server we are using to run Django on Heroku.*

Next we need these to control our database
```
pip3 install dj_database_url==0.5.0 psycopg2
```

Now we need cloudinary for our storage of static files
```
pip3 install dj3-cloudinary-storage
```


# Requirements.txt file
This needs to be updated as soon as a new framework / libary is installed.
```
pip3 freeze --local > requirements.txt
```

# Start the project in Django
```
django-admin startproject rustytavern .
```
*the dot here is so we create it in the current folder.*

```
python3 manage.py startapp menu
```

Now we need to migrate the changes to the database
```
python3 manage.py migrate
```

Test the server
```
python3 manage.py runserver
```
*CTRL + Left click on the http://... to open the window for port 8000*
```
Starting development server at http://127.0.0.1:8000/ 
```