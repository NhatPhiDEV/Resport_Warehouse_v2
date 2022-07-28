# Getting Started with Report WareHouse

This is a project used to visualize data in the form of charts and data tables

## Clean data

Open [https://bom.so/3pPdcK] copy content file clean_data.txt and run file in mysql workbench

## Create a virtual env and install requirements

#### `virtualenv env`

#### `source env/Scripts/activate`

#### `python -m pip install -r requirements.txt`

## Change file setting

DATABASES = { <br>
&nbsp;'default': { <br>
&nbsp;&nbsp;'ENGINE': 'django.db.backends.mysql', <br>
&nbsp;&nbsp;'NAME': '{db name}', <br>
&nbsp;&nbsp;'USER': '{username}', <br>
&nbsp;&nbsp;'PASSWORD': '{password}', <br>
&nbsp;&nbsp;'HOST': '{host}', <br>
&nbsp;&nbsp;'PORT': '{port}', <br>
&nbsp;&nbsp;'OPTIONS': { <br>
&nbsp;&nbsp;&nbsp;'init_command':"SET sql_mode='STRICT_TRANS_TABLES'" <br>
&nbsp;&nbsp;} <br>
&nbsp;} <br>
}

## Run code

#### `python manage.py runserver`

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view it in the browser.
