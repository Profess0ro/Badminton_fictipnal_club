# Racket Club

This is a page about a fictional Racket club that have some tennis courts that everyone can book to play on.
The Club also have members that play semi-professional Tennis with great results.
As a visitor to this page you can register an account so that you can book a court and comment on articles.
There are also a contact form that users can send questions to the club.

# Content
- [Introduction](#racket-club)
- [Project planning](#project-planning)
    * [Database structure](#database-structure)
    * [Wireframes](#wireframes)
    * [User stories](#user-stories)
- [Content](#content)
    * [Home page](#home-page)
    * [Rules page](#rules-page)
    * [Booking form](#booking-form)
    * [Booking success](#booking-success)
    * [Edit/delete booking](#editdelete-booking)
    * [About us page](#about-us-page)
    * [Contact us page](#contact-us-page)
- [Design](#design)
    * [Logo](#logo)
    * [Colorscheme](#colorscheme)
    * [Fonts](#fonts)
- [Resources](#resources)
- [Technologies](#technologies)
    * [Languages used](#languages-used)
    * [Packages](#packages-installed)
- [Deployment](#deployment)
    * [Github](#github)
    * [Deploy in development environment](#deploy-in-development-environment)
    * [Heroku](#heroku)
- [Testing]()
- [Problems encountered](#problems-encountered)
- [Credits](#credits)

# Project planning

## Database structure

<img src="readme/database.png">
<hr>

## Wireframes

This was my vision on how this project would be visual for the user.
Worked after this model as much as I could for the basic structure.<br>

<img src="readme/wireframe_mobile.png"><br>
<img src="readme/wireframe_tablet.png"><br>
<img src="readme/wireframe_big_screens.png"><br>

## User Stories

Here you can check out my user stories on the canban-board<br>
[Canban-board](https://github.com/users/Profess0ro/projects/6/views/1)

# Content

## Home page

## Rules page

## Booking form

## Booking success

## Edit/delete booking

## About us page

## Contact us page

# Design

## Logo
This logo was created by me with [Kittl´s](https://www.kittl.com/) creator tool. Very user friendly site with templates that makes it easier to start creating.<br>
<img src="static\images\logo.png" height="300"><br>
<hr> 

## Colorscheme

<img src="readme/colorscheme.png">

This is the colors I´ve chosen to use through the whole page, except for the black content text (#000000).<br>
**#2B3860**
This color are the darkest of them all and are used on the borders that divides the pages content such as the paginated list of articles and images. The color are also used on titles and links so they stand out as well.<br>
**#E8B272**
The usage of this color except from the logo is the hovering effect on links and social links at the footer.<br>
**#F0FBFF**
This is the background color of the navigation bars and the content divs. It´s not far from the white color (#FFFFFF) but enough difference so that it divides the comment entries from eachoter.<br> 
**#789EA7**
This color has a honorable mention since it´s only in the logo as a small line.
**#FFFFFF**
This is the background color of the "main content" area and also background color of the uneven comment entries on articles.
<hr>

## Fonts
**[Raleway](https://fonts.google.com/specimen/Raleway?query=raleway)**
This font is in my opinion a very readable font, thats why I choosed to have that on the content texts.<br>
**[Bebas Neue](https://fonts.google.com/specimen/Bebas+Neue?query=Bebas+Neue)**
This font are used on titles, links and the author info on articles. The font catched my eye when I browsed through fonts and really looked nice as a title text.



# Resources

[Pexels](https://www.pexels.com) - Image library<br>
[Google Fonts](https://fonts.google.com/) - Font library<br>
[Font Awesome](https://www.fontawesome.com) - Icon library<br>
[Kittl](https://www.kittl.com/) - Logo creator<br>
[Neon](https://neon.tech/) - Database<br>
[Mailtrap](https://mailtrap.io/) - SMTP for the contactform<br>
[Cloudinary](https://cloudinary.com/) - Database storage for images

# Technologies

### **Languages used:** 
- Django
- Python
- HTML
- CSS
- JavaScript
 

### **Packages installed:**<br>
After every time `pip3 install <package>` are used, ensure to use `pip3 freeze --local > requirements.txt` 

- [cloudinary](https://pypi.org/project/cloudinary/)
- [crispy-bootstrap5](https://pypi.org/project/crispy-bootstrap5/)
- [dj-database-url](https://pypi.org/project/dj-database-url/)
- [dj3-cloudinary-storage](https://pypi.org/project/dj3-cloudinary-storage/)
- [django](https://pypi.org/project/Django/)
- [django-allauth](https://pypi.org/project/django-allauth/)
- [django-crispy-forms](https://pypi.org/project/django-crispy-forms/)
- [django-summernote](https://pypi.org/project/django-summernote/)
- [gunicorn](https://pypi.org/project/gunicorn/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [whitenoise](https://pypi.org/project/whitenoise/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)


# Deployment

### GitHub
1. Log in to your GitHub account.
2. Create a repository by click on 'New' at the repositories page.
3. Go into your repository [This repository](https://github.com/Profess0ro/Racket_club) and click on 'Code' and copy the link.
4. Open VS code and choose 'Clone git repository..' now paste the link in the command file at the top: `https://github.com/Profess0ro/Racket_club.git` and choose a local storage in the window that pops up.

### Deploy in development environment

1. Open your repository `https://github.com/Profess0ro/Racket_club.git` with your choice of workspace (VS code or GitPod)
2. Install required dependencies with 
	```
	pip3 -r requirements.txt.
	```
3. Create `env.py` and make sure to add that file to your `.gitignore`. In `env.py` you are going to store some sensitive information.
4. Add the following info to `env.py`: <br>
    `CLOUDINARY_URL`<br>`DATABASE_URL`<br>`SECRET_KEY`
5. In your `settings.py` add your workspace URL to `ALLOWED_HOSTS`.
6. Start your project by writing this in the terminal:
```
django-admin startproject <projectname>
```
This will create following tree in your repository:
```
<projectname>/
    manage.py
    <projectname>/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```
7. Create apps by writing this in the terminal:
```
python3 manage.py startapp <appname>
```
This will create following tree:
```
<appname>/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
8. Everytime you´ve created an app and added models to each `models.py` make sure to make migrations with the following steps for adding to the database:
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
9. Create a superuser so that you have access to the adminpanel:
```
python3 manage.py createsuperuser
```
10. To preview the project type in:
```
python3 manage.py runserver
```
11. Before deploying to production:<br>
- Type in:
```
pip3 freeze > requirements.txt
``` 
- Make sure that in the `settings.py` you have: `DEBUG=False` 
12. Commit and push to GitHub.

### Heroku
1. Log in to your Heroku account
2. Go to the **'Heroku dashboard'** and click **'New'** and then **'Create new app'**
3. Choose a unique name for this application, then choose region (EU or USA)
4. Now go to **'Settings'** -> **'Reaveal config vars'** and add **'KEY'** and add following keys with the right value from your `env.py`:
- `CLOUDINARY_URL`
- `DATABASE_URL`
- `SECRET_KEY`
- `PORT` (value: 8000, can be found in settings.py)
5. In **'Settings'** click on **'Add buildpack'** and add following pack: `Python`
6. To install requirements use `pip install -r requirements.txt` at the terminal in VS Code/GitPod.
7. To create the Procfile use `echo web: node index.js > Procfile` at the terminal in VS Code/GitPod.
8. To deploy your repository to your Heroku account there are two ways. First go to **'Deploy'** in your Heroku application then scroll down and choose one of these options:<br>- **'Enable Automatic Deploys':** If you want that everytime you use `git push` in VS Code/GitPod that it deploys to Heroku<br>- **'Deploy Branch':** If you want to manually deploy your changes and have control when the code should or shouldn´t been deployed.

# Problems encountered

<img src="readme/problem1.png"><br><br>
- Suddenly the database didn´t cooperate with the page and started to search for other columns.<br>
**Solution:**<br>
Deleted and created a new database and migrated my models. Then the page found the right columns and content without changing anything of the codes.


- When trying to edit a comment on an article nothing happened when I pressed the button. No content appeared in the commentform to edit.<br>
**Solution:**<br>
Noticed that the `comments.js` searched for the wrong classnames and that´s why nothing happened. Changed name in `document.getElementsByClassName("")` and all worked again.

- When I created "About us" and was going to preview how the content was shown after installing the `SummernoteModelAdmin` I saw that all codetags was visual.<br>**Solution:**<br>
Adding `|safe` after, so that the code looks like this in the html-file: `{{ content.content|safe }}`

- Noticed after I´ve created the modal for deleting a comment this error occured:<br>
`modal.js:158 Uncaught TypeError: Cannot read properties of undefined (reading 'backdrop')
    at ne._initializeBackDrop (modal.js:158:39)
    at new ne (modal.js:69:27)
    at HTMLDocument.<anonymous> (comments.js:14:23)`<br>
Since `comments.js` are loaded into `base.html` it kept searching for the modal named `deleteModal` in every extended html-file. With this error it also blocked users from logging in.<br>
**Solution:**<br>
`const deleteModalElement = document.getElementById("deleteModal");
    let deleteModal = null;
    if (deleteModalElement) {
        deleteModal = new bootstrap.Modal(deleteModalElement);
    }` was added into `comments.js` so if the html-file doesn´t have a modal with the name `deleteModal` it doesnt initialize the modal element.

- Problems generating available times.
The final app for booking is my 4th try to make a booking system. On the first 3 times I´ve tried to give a function a span of starting and end times that it should calculate with. But after the 3rd try I came up with a solution to feed the database with start and end times that a function could calculate with. That really solved my problem with the booking system that now easier can calculate available times for the users.
# Credits

- [Mailtrap tutorial to create contactform](https://www.youtube.com/watch?v=5XFiqc8HlkE)
- Rohit Sharma - My mentor, for great meetings and helpful tips

