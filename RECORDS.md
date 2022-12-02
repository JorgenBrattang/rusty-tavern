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

Press on **View** right below that message, to make sure it works.

## Bug encountered
For me **crispy_form** module was not found in **INSTALLED_APPS"** in settings.py, the issue for me that the **requirements.txt** didn't update when I added it. But it was a quick fix due to the error message provided.

# Now lets start to build up the menu
Navigate to the folder **menu** and open up **models.py**

```python
from django.db import models
from django.contrib.auth.models import User # This will ensure the chef who created the dish is mentioned
from cloudinary.models import CloudinaryField # This will show the image stored on Cloudinary

STATUS = ((0, 'Draft')), ((1, 'Published')) # This does what is says it does.


class Item(models.Model):
    title = models.CharField(max_length=200, unique=True) # Can't have two of the same name
    slug = models.SlugField(max_length=200, unique=True) # Slug will deprive from title later on.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='menu_items') # This will be the chef's entry and when he/she quits all the dishes related will be deleted.
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    food_image = CloudinaryField('image', default='placeholder') # Image from cloudinary, placeholder as default
    excerpt = models.TextField(blank=True) # Short text
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='menu_likes', blank=True)

    class Meta:
        ordering = ['-created_on'] # This may change later on, for now its the newest item first

    def __str__(self):
        return self.title # Always include this, so we can see the title instead of just default text.

    def number_of_likes(self):
        return self.likes.count() # Keeps track of likes
```

## Review model

```python
class Review(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='review') # Gets the food item from previous model
    name = models.CharField(max_length=80) # Name of the person who makes it
    email = models.EmailField() # Email adress
    body = models.TextField() # The review it self
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False) # Most be approved by the site owner

    class Meta:
        ordering = ['created_on']  # This may change later on, for now its the oldest item first

    def __str__(self):
        return f'Review {self.body} by {self.name}' # Returns the values for the body and name field.
```

## Migrate the changes
Now lets migrate the changes to our database
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```

# Admin panel
## Create a superuser (admin)
```
python3 manage.py createsuperuser
```

Now just follow the promts in the terminal
```python
Username (leave blank to use 'gitpod'): admin
Email address: # This is Optional
Password: # This will be invisable as you type it
Password # Same goes here
Superuser created successfully.
```

## Forgot to commit earlier
```
git add .
```

```
git commit -m "Add models for menu Items and reviews, also created superuser"
```

```
git push
```
Since we don't have autodeploy on in Heroku, so that has to be manually deployed when we like that to happen.

## Admin panel creation
Navigate to the file **admin.py** within the **menu** folder
```python
from django.contrib import admin
from .models import Item # Import our model to this file

admin.site.register(Item) # This will make the model appear on the admin panel
```

## Access the admin panel
To access run the server
```
python3 manage.py runserver
```

And CTRL + Left click on this on
```
http://127.0.0.1:8000/
```

On the **URL** add **/admin**

You will be meet by a login page and see that our **Item** model is there, so we can now add Items.

## Now we need to add Summernote
[Summernote website](https://summernote.org/)
```
pip3 install django-summernote
```

Freeze our requirements.txt file
```
pip3 freeze --local > requirements.txt
```

Add summernote to our **INSTALLED_APPS**, so navigate to the folder **rustytavern** open up **settings.py**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'menu',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_summernote', # <<<--- Add this one
]
```

Now to add this to our **urls.py** within the same folder
```python
from django.contrib import admin
from django.urls import path, include # <<<--- Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')), # <<<--- Add this
]
```

Updating the **admin.py** file within the **menu** folder
```python
from django.contrib import admin
from .models import Item
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Item) # <<<--- Add this and the code below
class ItemAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')

# admin.site.register(Item) <<<--- Delete this
```

## Update the changes
Run the migrate command
```
python3 manage.py migrate
```

To see the change, update the admin page of the server and you can now see when you adding a **Menu Item** you get a full featured editor.

## Make life easier for creating Menu items
Go back to the **admin.py** file within the **menu** folder.
```python
@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title', )} # This will autogenerate a slug field from the the title, example "Hello World" = "Hello-World"
    list_filter = ('status', 'created_on') # This will let you filter the Menu items.
    summernote_fields = ('content')
```

## Admin panel more functionality
[list_display documentation](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)<br>
[search_field documentation](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)

These functinality can really change the admin panel, lets add the basic onces we need for now.

Within the **admin.py** file
```python
@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'slug', 'status', 'created_on') # <<<--- Add this
    search_fields = ['title', 'content'] # <<<--- And this
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')
```

Now lets add one for **Review**
```python
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'item', 'created_on', 'approved')
    search_fields = ['name', 'email', 'body']
    list_filter = ('approved', 'created_on')
    actions = ['approved_reviews']

    def approved_reviews(self, request, queryset):
        queryset.update(approved=True)
```

## Changes to the model Reviews
I changed the model name **Reviews** to **Review**, this is changed within this file but will add it to gitpod as a commit message as well a migrate to make the change to the database by doing the **makemigrations** command again followed by **migrate**
```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```

The commit commands again.

```
git add .
```

```
git commit -m "add functionality to admin panel, and renamed Reviews model to Review"
```

```
git push
```

## Small update, that I forgot
```
git add .
```

```
git commit -m "small update actions on review to turn approved into True"
```

```
git push
```

# Time for our visual aspect
## Views file
Navigate to **menu** folder and open up **views.py**

[Django genereic views documentation](https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/)

```python
from django.shortcuts import render
from django.views import generic
from .models import Item

class ItemList(generic.ListView):
    model = Item
    queryset = Item.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6 # This is temporary will see how it turns out later on.
```

## Bootstrap in settings.py
This needs to be in the **settings.py** file for Django to accept the template

[Crispy BootStrap Documentation](https://pypi.org/project/crispy-bootstrap5/)

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```

## Bootstrap for html
Create two new files within **templates** folder
```
base.html
index.html
```

Open up **base.html** and get this code installed
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    
    <title>Rusty Tavern</title>
</head>

<body>

    {% block content %}
    <!-- Our content will go here -->
    {% endblock %}

    <!-- Bootstrap Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous">
    </script>
</body>

</html>
```

Open up **index.html** and get this code
```html
{% extends 'base.html' %}
{% block content %}

<h1>Hello World</h1>

{% endblock %}
```

This is just the start of our journey, but it is a start!

## Commiting the changes
```
git add .
```

```
git commit -m "Add index and base html starting point"
```

```
git push
```

# Building up the site with bare minimum
## base.html
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <!-- Font Awesome -->
    <script src="https://kit.fontawesome.com/b66a8a8811.js" crossorigin="anonymous"></script>

    <!-- Google fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IM+Fell+English+SC&family=Lato&display=swap" rel="stylesheet">

    <!-- Stylesheet link -->
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <title>Rusty Tavern</title>
</head>

<body>
    <!-- Main content -->
    <main>
        {% block content %}
        <!-- Our content will go here -->
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer>

    </footer>
    <!-- Bootstrap javascript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous">
    </script>
</body>

</html>
```

## index.html
```html
<!-- Base Code provided from Code Institute walkthrough -->
{% extends 'base.html' %}
{% block content %}

<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="row">
                <!-- For loop for item_list -->
                {% for item in item_list %}
                <div class="col-md-2">
                    <div class="card md-2">
                        <div class="card-body">
                            <!-- Image place holder -->
                            {% if 'placeholder' in item.food_image.url %}
                            <img src="https://codeinstitute.s3.amazonaws.com/fullstack/blog/default.jpg"
                                alt="default image" class="card-img-top">
                            {% else %}
                            <img src="{{ item.food_image.url }}" alt="food image" class="card-img-top">
                            {% endif %}
                        </div>
                        <a href="{% url 'item_detail' item.slug %}" class="post-link">
                            <!-- Title and excerpt -->
                            <h2 class="card-title">{{ item.title }}</h2>
                            <p class="card-text">{{ item.excerpt }}</p>
                        </a>
                        <hr />
                        <!-- Displaying created on and number of likes -->
                        <p class="card-text text-muted h6">{{ item.created_on }}
                            <i class="fa-solid fa-heart"></i>{{ item.number_of_likes }}
                        </p>
                    </div>
                </div>
                <!-- If divisable by 3 it changes the page -->
                {% if forloop.counter|divisibleby:3 %}
            </div>
            <div class="row">
                {% endif %}
                {% endfor %}
            </div>
        </div>
    </div>
    <!-- If more then 3 pages exists paginate them -->
    {% if is_paginated %}
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
            <!-- Goes back to the previous page -->
            {% if page_obj.has_previous %}
            <li><a href="?page={{ page_obj.previous_page_number }}" class="page-link">&laquo; PREV </a></li>
            {% endif %}
            <!-- Goes forward to the next page -->
            {% if page_obj.has_next %}
            <li><a href="?page={{ page_obj.next_page_number }}" class="page-link"> NEXT &raquo;</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>

{% endblock %}
<!-- End provided -->
```

## Commiting updates to index and base html
```
git add .
```

```
git commit -m "Base structure to index and base html, from code institute"
```

```
git push
```

# Now to get it visable
## The Path in new file
First create a new **urls.py** file within the **menu** folder

```python
from . import views
from django.urls import path

urlpatterns = [
    path('', views.ItemList.as_view(), name='home')
]
```

## The Path in the original file
Now refer this in the original **urls.py** file within the **rustytavern** folder
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('menu.urls'), name='menu.urls') # <<<--- Add this one
]
```

## Test it out to see if you can see
```
python3 manage.py runserver
```

If you can see the Menu Item now, good, otherwise go back and see what the issue may have been.

## Commit
```
git add .
```

```
git commit -m "Add so the Paths are aligned correctly"
```

```
git push
```

# Item details views
[Documentation Path Converters](https://docs.djangoproject.com/en/3.2/topics/http/urls/#how-django-processes-a-request)

## views.py in menu folder
```python
from django.shortcuts import render, get_object_or_404 # <<<--- Import get_object_or_404 (later usage)
from django.views import generic, View # <<<--- Import View
from .models import Item


class ItemList(generic.ListView):
    model = Item
    queryset = Item.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class ItemDetail(View): # <<<--- Add this code section
    def get(self, request, slug, *args, **kwargs):
        queryset = Item.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        reviews = item.reviews.filter(approved=True).order_by('created_on')
        liked = False
        if item.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'item_detail.html',
            {
                'item': item,
                'reviews': reviews,
                'liked': liked,
            }
        )

```

## Create a new html template
Create a new html template named **item_detail.html**
```html
<!-- This code is based on Code institute's code (will be changed for our needs) -->
{% extends 'base.html' %} {% block content %}
<div class="masthead">
    <div class="container">
        <div class="row g-0">
            <!-- Displays the title, author and created on -->
            <div class="col-md-6 masthead-text">
                <h1 class="post-title">{{ item.title }}</h1>
                <p class="post-subtitle">{{ item.author }} | {{ item.created_on }}</p>
            </div>
            <!-- Default image if none exists -->
            <div class="d-none d-md-block col-md-6 masthead-image">
                {% if "placeholder" in post.featured_image.url %}
                <img src="https://codeinstitute.s3.amazonaws.com/fullstack/blog/default.jpg" width="100%">
                {% else %}
                <img src=" {{ post.food_image.url }}" width="100%">
                {% endif %}
            </div>
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col card mb-4 mt-3 left top">
            <div class="card-body">
                <!-- displays the content -->
                <p class="card-text">
                    {{ item.content | safe }}
                </p>
                <div class="row">
                    <!-- Number of likes -->
                    <div class="col-1">
                        <strong class="text-secondary">
                            {{ item.number_of_likes }}
                        </strong>
                    </div>
                    <!-- Displays total reviews -->
                    <div class="col-1">
                        {% with reviews.count as total_reviews %}
                        <strong class="text-secondary">
                            {{ total_reviews}}
                        </strong>
                        {% endwith %}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <!-- Displays Reviews -->
        <div class="col-md-8 card md-4 mt-3">
            <h3>Reviews:</h3>
            <div class="card-body">
                {% for review in reviews %}
                    <div class="reviews" style="padding: 10px">
                    <p class="font-weight-bold">
                        {{ review.name }}
                        <span class="text-muted font-weight-normal">
                            {{ review.created_on }}
                        </span> Wrote:
                    </p>
                    {{ review.body | linebreaks }}
                </div>
                {% endfor %}
            </div>
        </div>
        <!-- Add reviews -->
        <div class="col-md-4 card mb-4 mt-3">
            <div class="card-body">

            </div>
        </div>
    </div>
</div>
{% endblock %}
<!-- End Credit -->
```

## urls.py within the menu folder
```python
urlpatterns = [
    path('', views.ItemList.as_view(), name='home'),
    path('<slug:slug>/', views.ItemDetail.as_view(), name='item_detail'), # <<<--- Add this one
]
```

## index.html url path
Navigate to the index.html file and under the placeholder image there is an **a href**, change it to this
```html
<a href="{% url 'item_detail' item.slug %}" class="post-link">
```

## Check if it's working
```
python3 manage.py runserver
```

Press on one of the Item made, and see if it works, if not. Go back and check!

## Commit the changes
```
git add .
```

```
git commit -m "Add item_detail.html update the views.py and urls.py"
```

```
git push
```

# Authentication
## Install django allAuth
```
pip3 install django-allauth
```

Updating the requirements.txt file accordingly
```
pip3 freeze --local > requirements.txt
```

Within the **settings.py** file add allAuth
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites', # <<<--- This
    'allauth', # <<<--- This
    'allauth.account', # <<<--- This
    'allauth.socialaccount', # <<<--- This
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'menu',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_summernote',
]

SITE_ID = 1 # <<<--- This

LOGIN_REDIRECT_URL = '/' # <<<--- This
LOGOUT_REDIRECT_URL = '/' # <<<--- This

ACCOUNT_EMAIL_VERIFICATION = 'none' # <<<--- This
```

## urls path for accounts
**urls.py** file within **rustytavern** folder
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('menu.urls'), name='menu.urls'),
    path('accounts/', include('allauth.urls')), # <<<--- Add this
]
```

## Migrate the changes
```
python3 manage.py migrate
```

## Test if it works
Start the server
```
python3 manage.py runserver
```

add this behind the URL
```
/accounts/signup
```

Make sure your logout first, by going to the /admin page.

## Lets add the functionality to base.html
```html
<!-- Navigation -->
    <nav class="navbar">
        <div class="container-fluid">
            <ul class="navbar-nav me-auto mb-2">
                <li class="nav-item"><a href="{% url 'home' %}" class="nav-link">Home</a></li>
                {% if user.is_authenticated %}
                <li class="nav-item"><a href="{% url 'account_logout' %}" class="nav-link">Logout</a></li>
                {% else %}
                <li class="nav-item"><a href="{% url 'account_signup' %}" class="nav-link">Register</a></li>
                <li class="nav-item"><a href="{% url 'account_login' %}" class="nav-link">Login</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>
```

This goes above the 
```html
 <!-- Main content -->
```

## Lets lock this up in a commit

```
git add .
```

```
git commit -m "Add django-allauth and implement it to the site"
```

```
git push
```

# Now lets get the templates from django for allauth
## First lets ask for the python version
```
ls ../.pip-modules/lib
```

```
python3.8
```

This will download the folders from our server into our **templates** folder.

```
 $ cp -r ../.pip-modules/lib/python3.8/site-packages/allauth/templates/* ./templates
```

Now you have 4 new folders in the **templates** folder
```
account
openid
socialaccount
tests
```

## Edit the templates
Open upp **account** folder and edit these files
```
login.html
logout.html
signup.html
```

By modify this
```
{% extends "account/base.html" %}
```

Into this
```
{% extends "base.html" %}
```

Now they will extend our **base.html** instead

## Modify the login.html
First we need to take away the socialaccounts part, which we don't need for this project.

This is how your file should look at this stage

```html
{% extends "base.html" %}

{% load i18n %}
{% load account socialaccount %}

{% block head_title %}{% trans "Sign In" %}{% endblock %}

{% block content %}

<div class="container">
  <div class="row">
    <div class="col-md-8 mt-5 offset-md-4">

        <h1>{% trans "Sign In" %}</h1>

        <p>{% blocktrans %}If you have not created an account yet, then please
        <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}</p>

        <form class="login" method="POST" action="{% url 'account_login' %}">
        {% csrf_token %}
        {{ form.as_p }}
        {% if redirect_field_value %}
        <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
        {% endif %}
        <a class="button secondaryAction" href="{% url 'account_reset_password' %}">{% trans "Forgot Password?" %}</a>
        <button class="primaryAction" type="submit">{% trans "Sign In" %}</button>
        </form>

    </div>
  </div>
</div>

{% endblock %}
```

## Modify the logout.html and signup.html
For this stage we will have the same template for all three html files, so just wrap the remaining two like the login.html

```html
{% block content %}
<div class="container">
  <div class="row">
    <div class="col-md-8 mt-5 offset-md-4">
        <!-- The rest of the content goes here -->
    </div>
  </div>
</div>
{% endblock %}
```

## Commit the changes

```
git add .
```

```
git commit -m "Basic template modifying for login, logout, signup"
```

```
git push
```

# Review Form
## Create new forms.py file
Within our **menu** folder create a new file called **forms.py**
```python
from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)

```

## Updating views.py
```python
from .forms import ReviewForm # <<<--- Import this

class ItemDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Item.objects.filter(status=1)
        item = get_object_or_404(queryset, slug=slug)
        reviews = item.reviews.filter(approved=True).order_by('created_on')
        liked = False
        if item.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'item_detail.html',
            {
                'item': item,
                'reviews': reviews,
                'liked': liked,
                'review_form': ReviewForm(),
            }
        )
```

## Update item_detail.html
```html
<!-- Add reviews -->
<div class="col-md-4 card mb-4 mt-3">
    <div class="card-body">
        {% if reviewed %}
        <div class="alert alert-success" role="alert">
            Your review is awaiting approval
        </div>
        {% else %}
        {% if user.is_authenticated %}

        <h3>Leave a Review:</h3>
        <p>Posting as: {{ user.username }}</p>
        <form method="post">
            {{ review_form | crispy }}
            {% csrf_token %}
            <button type="submit" class="btn btn-success btn-lg">Submit</button>
        </form>
        {% endif %}
        {% endif %}
    </div>
</div>
```

## Commit the changes

```
git add .
```

```
git commit -m "Add form for reviews, not functinal yet"
```

```
git push
```

# Making the review function working
## Updating the views.py file
In the class **ItemDetail()** add this

```python
request,
    'item_detail.html',
    {
        'item': item,
        'reviews': reviews,
        'reviewed': False, # <<<--- This one
        'liked': liked,
        'review_form': ReviewForm(),
    }
```
Then copy paste the **def get()** and rename it to **post**

```python
def post(self, request, slug, *args, **kwargs): # <<<--- post instead of get
    queryset = Item.objects.filter(status=1)
    item = get_object_or_404(queryset, slug=slug)
    reviews = item.reviews.filter(approved=True).order_by('created_on')
    liked = False
    if item.likes.filter(id=self.request.user.id).exists():
        liked = True

    # --- Add this section ---
    review_form = ReviewForm(data=request.POST)

    if review_form.is_valid():
        review_form.instance.email = request.user.email
        review_form.instance.name = request.user.username
        review_form.instance.item = item
        review_form.save()
    else:
        review_form = ReviewForm()
    # --- end section ---

    return render(
        request,
        'item_detail.html',
        {
            'item': item,
            'reviews': reviews,
            'reviewed': True, # <<<--- Set this to True
            'liked': liked,
            'review_form': review_form,
        }
    )

```

## Commit the updated working review form

```
git add .
```

```
git commit -m "Updated and working review function"
```

```
git push
```


# Like function
## Open views.py
Add this so we can toggle the **like** function

```python
class ItemLike(View):
    def post(self, request, slug):
        item = get_object_or_404(Item, slug=slug)

        if item.likes.filter(id=request.user.id).exists():
            item.likes.remove(request.user)
        else:
            item.likes.add(request.user)

        return HttpResponseRedirect(reverse('item_detail', args=[slug]))
```

## Open urls.py in the menu folder
And make a new path for our **ItemLike** view

```python
path('like/<slug:slug>', views.ItemLike.as_view(), name='item_like'),
```

## Open template item_detail.html
And update this section

```html
<!-- Number of likes -->
<div class="col-1">
    <strong class="text-secondary">
        {% if user.is_authenticated %}
        <form class="d-inline" action="{% url 'item_like' item.slug %}" method="POST">
            {% csrf_token %}
            {% if liked %}
            <button class="btn" type="submit" value="{{ item.slug }}">
                <i class="fa-solid fa-heart"></i>
            </button>
            {% else %}
            <button class="btn" type="submit" value="{{ item.slug }}">
                <i class="fa-regular fa-heart"></i>
            </button>
            {% endif %}
        </form>
        {% else %}
        <span class="text-secondary"><i class="fa-regular fa-heart"></i></span>

        {% endif %}
        <span class="text-secondary">{{ item.number_of_likes }}</span>
    </strong>
</div>
<!-- Displays total reviews -->
```

## Commit the working like function

```
git add .
```

```
git commit -m "Add functinal like function to Items"
```

```
git push
```