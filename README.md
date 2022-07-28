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
&emsp;'default': { <br>
&emsp;&emsp;'ENGINE': 'django.db.backends.mysql', <br>
&emsp;&emsp;'NAME': '{db name}', <br>
&emsp;&emsp;'USER': '{username}', <br>
&emsp;&emsp;'PASSWORD': '{password}', <br>
&emsp;&emsp;'HOST': '{host}', <br>
&emsp;&emsp;'PORT': '{port}', <br>
&emsp;&emsp;'OPTIONS': { <br>
&emsp;&emsp;&emsp;'init_command':"SET sql_mode='STRICT_TRANS_TABLES'" <br>
&emsp;&emsp;} <br>
&emsp;} <br>
}

## Run code

#### `python manage.py runserver`

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view it in the browser.
