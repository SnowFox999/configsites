# Computers' configurator

<br />

## Start the app 

> 👉 **Step 1** 

```bash
$ git clone https://github.com/app-generator/django-adminlte.git
$ cd django-adminlte
```
<br />

> 👉 **Step 2** 

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Important information

<br />

> All fields with foreign keys must be filled during creation of new computer (Customer, Employee, Windows) 
> Date must be filled
