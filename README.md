# Racket Club

### Database structure

<img src="readme/database.png">
<hr>

### Wireframes

<img src="readme/wireframe_mobile.png"><br>
<img src="readme/wireframe_tablet.png"><br>
<img src="readme/wireframe_big_screens.png"><br>

### Resources

[Pexels](https://www.pexels.com) - Image library<br>
[Google Fonts](https://fonts.google.com/) - Font library<br>
[Font Awesome](https://www.fontawesome.com) - Icon library<br>
[Kittl](https://www.kittl.com/) - Logo creator

### Technologies

[Django](https://www.djangoproject.com/) 

<b>Packages installed:</b><br>
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



### Deployment

### Problems encountered

<img src="readme/problem1.png"><br><br>
- Suddenly the database didn´t cooperate with the page and started to search for other columns.
<b>Solution:</b><br>
Deleted and created a new database and migrated my models. Then the page found the right columns and content without changing anything of the codes.
<hr>

- When trying to edit a comment on an article nothing happened when I pressed the button. No content appeared in the commentform to edit.<br>
<b>Solution:</b><br>
Noticed that the `comments.js` searched for the wrong classnames and that´s why nothing happened. Changed name in `document.getElementsByClassName("")` and all worked again.

### Credits


