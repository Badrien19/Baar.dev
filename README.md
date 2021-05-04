## Set-up environement:

### First time only:

- mkdir ~/.venv
- cd ~/.venv
- python3 -m venv testproj_django

### Each time:
- source ~/.venv/testproj_django/bin/activate

## Basic command

### to run server:
- python manage.py runserver

### create admin:
- python manage.py createsuperuser

### update database:
- python manage.py makemigrations
- python manage.py migrate
- python3 manage.py collectstatic (for production)
- python manage.py sqlmigrate blog 0001 (to see sql code)

### Add a post manualy:
- python manage.py shell (interractive console)
- from blog.models import Post
- from django.contrib.auth.models import User 
- Post.objects.all()\
- user = User.objects.filter(username='admin').first()
- post_1 = Post(title='First post', content='It's alive!', author_id=user.id)
- post_1.save()
- Post.objects.all()

## Install same environement:
- pip freeze > requirements.txt (stock les config)
- pip install -r requirements.txt  (install les config)