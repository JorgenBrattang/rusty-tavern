# Installing frameworks / libaries
## Django and gunicorn
```
pip3 install 'django<4' gunicorn
```
*gunicorn is the server we are using to run Django on Heroku.*

## Control our database
```
pip3 install dj_database_url==0.5.0 psycopg2
```

## Cloudinary for our storage of static files
```
pip3 install dj3-cloudinary-storage
```

## Install Bootstrap
```
pip install crispy-bootstrap5
```

## Requirements.txt file
This needs to be updated as soon as a new framework / libary is installed.
```
pip3 freeze --local > requirements.txt
```

# Start the project in Django
```
django-admin startproject rustytavern .
```
*the dot here is so we create it in the current folder.*

## Create an app for our project
```
python3 manage.py startapp menu
```

## Now to install our apps to the project
Within the folder **rustytavern** (project) in the **settings.py** add your app.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'menu',  # <<<---- your main app >>>
    'crispy_forms',  # <<<---- Crispy_forms (for later use) >>>
    'crispy_bootstrap5',  # <<<---- And Crispy bootstrap >>>
]
```

## Now we need to migrate the changes to the database
```
python3 manage.py migrate
```

## Test the server
```
python3 manage.py runserver
```
*CTRL + Left click on the http://... to open the window for port 8000*
```
Starting development server at http://127.0.0.1:8000/ 
```

## When opened up the message should be like this:
```
The install worked successfully! Congratulations!
```

# Heroku and PostGreSQL
## Navigate to the Heroku website
- Click here to navigate the website <a>https://id.heroku.com/login</a>
- Login to your account.
- Press on **New** *(up in the right corner)* -> **Create new app**
- App name: **rustytavern** *(This is what I used, can't be used again!)*
- Choose Region: **Europe** *(Again, this is what I used)*
- Create App

## Navigate to the ElephantSQL website
- Click here to navigate the website <a>https://customer.elephantsql.com/login</a>
- Sign in using your github account. 
(if you have no account, please follow the instructions provided by <a>https://codeinstitute.net/</a>)
    - Navigate to <a>ElephantSQL.com</a> and **"Get a managed databse today"**
    - Select **"Try now for FREE"** in the TINY TURTLE database plan
    - Select **"Log in with GitHub"** and authorize ElephantSQL with your selected GitHub account
    - In the **Create new team** form:
        - Add a **team name** (You can add your own name here)
        - Read and agree to Terms of Service
        - Select **Yes** for GDPR
        - Provide your email adress
        - Click **"Create Team"**
    - Your account is successfully created!
- Create New Instance *(Big green button to the upper right.)*
- Set up your plan
    - Give your plan a **Name** (This is commonly the name of the project)
    - Select the **Tiny Turtle (Free)** plan
    - You can leave the **Tags** field
- Press on **Select Region"**
- Select a data center near you *(This is automated, but if you like to change. Please do.)*
- Check if the details that you added are correct and then click **"Create instance"**
- Return to the ElephantSQL dashboard and click on the **database instance name** for this project
- In the URL section, click on the copy icon to copy the databse URL

# Now we need an env.py file to accomidate the URL
Create a new env.py file
```
touch env.py
```
Open it and add this
```python
import os

os.environ["DATABASE_URL"] = "<copiedURL>"
```
*(replace the <copiedURL> with the one from ElephantSQL)*

## Now we need a Django Secret key that is unique
I used this <a>https://djecrety.ir/</a> to generate my key.
Go back into env.py file add this
```python
os.environ["SECRET_KEY"] = "<copiedKEY>"
```

## Making our project aware of env.py file
This env.py file is ignored by .gitIgnore so we need to make sure our Django project knows that.
Within the **rustytavern** folder go into **settings.py** and below the **Path** import add the following
```python
import os
import dj_database_url
if os.path.isfile('env.py'):
    import env
```

## Now add the filepath to the secret key
Within the **settings.py** file a bit further down a default generated **SECRET_KEY** is created, lets replace that with the reference from **env.py** file.
```python
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## Now for the Database
A bit further down comment out the original **DATABASES** variable and add the code below.
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

## Now we need to migrate the changes.
```
python3 manage.py migrate
```

## Go back to Heroku Dashboard
And open the **Settings** tab:
Add the following config vars:
```
KEY: DATABASES_URL
VALUE: Add the databaseURL from ElephantSQL *(without quotations marks)*
```
```
KEY: SECRET_KEY 
VALUE: Add the generated Django unique code from env.py file.
```
```
KEY: PORT
VALUE: 8000
```

## Commit the changes that are made
```
git add .
```
```
git commit -m "Add connection to database and its working"
```
```
git push
```

# Cloudinary
## Create an account
Instructions provided by <a>https://codeinstitute.net/</a>
- Visit the Cloudinary website
- Click on the Sign Up For Free button
- Provide your name, email address and choose a password
- For Primary interest, you can choose Programmable Media for image and video API
- Optional: edit your assigned cloud name to something more memorable
- Click Create Account
- Verify your email and you will be brought to the dashboard

## Installing it to the project
In the cloudinary Dashboard copy the **API Environment variable** by pressing on the copy icon to the right.

Within the env.py file add this
```python
os.environ["CLOUDINARY_URL"] = "<copiedURL>"
```
*Your URL will start with **CLOUDINARY_URL=** remove this so it looks like this in the start
```
cloudinary://...
```

## Now back to Heroku
In the **Config Vars** within settings, add this
```
KEY: CLOUDINARY_URL
VALUE: <copiedURL>
```
*(Value most be the same as in the env.py file)*

Another thing we need to add for now is
```
KEY: DISABLE_COLLECTSTATIC
VALUE: 1
```
*(This will be removed later)*

## Back to settings.py file
in the **settings.py** file add cloudinary in this order!
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage', # <<--- This needs to be before djangos staticfiles
    'django.contrib.staticfiles',
    'cloudinary', # <<--- This is added as usual
    'menu',
    'crispy_forms',
    'crispy_bootstrap5',
]
```

A bit further down we need to create the static connection to cloudinary
```python
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR), 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

# Templates and folder creation
Add our **TEMPLATES_DIR**
```python
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates') # <<--- This is the one we need to add
```

Now we need to tell django where the templates directory is
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## Tell Django about our Heroku app
Still in the **settings.py** file
```python
ALLOWED_HOSTS = ['rustytavern.herokuapp.com', 'localhost']
```
*(your app name first, the followed by herokuapp.com)*

Now we need to create these folders within our project in the top level.
```
media
static
templates
```
*(Spellcheck them!)*

# Deployment to Heroku
## Procfile
Now for the push towards Heroku, we need to create a Procfile *(spelling is crucial!)*
```
touch Procfile
```
*(Notice when you create it has the Herkou logo, otherwise the spelling is incorrect)*

Within that file add this
```
web: gunicorn rustytavern.wsgi
```
*(Change **rustytavern** to your app name)*

## Commit the changes
```
git add .
```
```
git commit -m "deployment commit"
```
```
git push
```

## Navigate to Heroku
- Go to the Deploy tab and select **Deployment method** as **GitHub**
- Search for your repository
- I entered **rustytavern**
- Now press Connect
- Click on **Deploy Branch**

So if you followed correctly you should see this glorified message popup!
```
Your app was successfully deployed.
```