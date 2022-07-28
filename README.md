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
'default': { <br>
'ENGINE': 'django.db.backends.mysql', <br>
'NAME': '{db name}', <br>
'USER': '{username}', <br>
'PASSWORD': '{password}', <br>
'HOST': '{host}', <br>
'PORT': '{port}', <br>
'OPTIONS': { <br>
'init_command':"SET sql_mode='STRICT_TRANS_TABLES'" <br>
} <br>
} <br>
}

## Run code

### `python manage.py runserver`

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view it in the browser.
