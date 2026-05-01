## Install Django
#### 1. Create Django project
```
django-admin startproject myproject
cd myproject
```
#### 2. Install Django & DRF
pip install django djangorestframework
#### 3. Create an app
```
python manage.py startapp api
```
```bash

```

### Install RAG packages
pip install -q -U google-genai faiss-cpu python-dotenv

    python -m venv venv && source venv/bin/activate

py install 3.12
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Setup venv
python -m venv .venv
python -m venv venv
py -3.12 -m venv venv
### ctivate your environment again
myenv\Scripts\activate  ## is manaul
.venv\Scripts\activate

Never commit .env to Git
Add .env to .gitignore:

pip install django
py -m pip install mysqlclient
py -m pip uninstall PyMySQL
py -m pip install django-environ
python -m pip install --upgrade mysqlclient
pip install pymysql
pip install django-environ
pip install mysql-connector-python
pip install djangorestframework-simplejwt

pip install drf-spectacular ##OpenAPI docs with Swagger UI.

pip install channels channels-redis
pip install daphne
run with ws:
daphne ANGKORTRANS.asgi:application

 No module named 'Crypto' install below
 pip install pycryptodome
### Check list package
pip list
pip show mysqlclient

## Stay in activated venv then install from requirements.txt to install all packages to project
pip install -r requirements.txt


pip install gunicorn
pip install redis celery

# Run websocket
``` bash
daphne ANGKORTRANS.asgi:application --port 8001 --bind [IP_ADDRESS]
daphne -p 52467 ANGKORTRANS.asgi:application # custom port only
daphne ANGKORTRANS.asgi:application # default port 8000
``` 

``` bash
# Run with address and port:
daphne -b [IP_ADDRESS] -p 9000 ANGKORTRANS.asgi:application
```

# Run api server
python manage.py runserver [IP_ADDRESS]


## Install packages to venv or environment
``` bash
Activate your virtual environment, then install Pillow:
python -m pip install Pillow


if have already please install:
pip install Pillow
```

## Render django
```bash
#Build Command:
pip install -r requirements.txt && python manage.py migrate

#Start Command:
gunicorn ANGKORTRANS.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
daphne ANGKORTRANS.asgi:application --port $PORT --bind [IP_ADDRESS]

🧠 Honest takeaway
Gunicorn = scales requests
Daphne = scales connection

# Why Gunicorn is better for Render
Because Render is a web hosting platform that runs many short-lived processes. Gunicorn is designed for this.
🧠 The real difference
🔵 Gunicorn (WSGI / ASGI with Uvicorn workers)

Best for:

normal APIs (REST)
CRUD operations
typical Django apps

👉 Handles many short-lived requests very efficiently

🟣 Daphne (ASGI, built for Channels)

Best for:

WebSockets
real-time features (chat, notifications, live updates)

👉 Handles long-lived connections


Correct architecture
Service 1: Gunicorn → HTTP (API)
Service 2: Daphne → WebSockets
Service 3: Redis → channel layer

Architecture overview
        (Nuxt frontend)
               |
        -----------------
        |               |
   Gunicorn        Daphne
   (HTTP API)     (WebSocket)
        |               |
        ------- Redis -------


=== if need 3 services different 
```bash
pip install channels channels-redis daphne gunicorn uvicorn
Service 1 — Gunicorn (HTTP API)
# local
uvicorn ANGKORTRANS.asgi:application --host 0.0.0.0 --port 52467

gunicorn ANGKORTRANS.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT

Service 2 — Daphne (WebSocket)
# Start WebSocket with Daphne
daphne -b 0.0.0.0 -p $PORT ANGKORTRANS.asgi:application
# daphne ANGKORTRANS.asgi:application --port $PORT

# Start API with Gunicorn
gunicorn ANGKORTRANS.asgi:application --bind [IP_ADDRESS]:$PORT -k uvicorn.workers.UvicornWorker
gunicorn ANGKORTRANS.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT


# In the same command but must be different port on Remder
gunicorn ANGKORTRANS.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
gunicorn ANGKORTRANS.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:52467


You should include migrations + static files:
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput

# Connect to Redis from both services
gunicorn ANGKORTRANS.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 &

daphne -b 0.0.0.0 -p $PORT ANGKORTRANS.asgi:application
```

## Issue with git push with security rejection
```
error: failed to push some refs to 'https://github.com/rtysnapdragon/ANGKORTRANS.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another
hint: repository pushing to the same branch.
```

1. Do this override all
```
git checkout --orphan clean-main
git add .
git commit -m "Fresh clean commit"
git branch -D main
git branch -m main
git push --force origin main
```


##### CambodiaGeographicalList2025
```bash
link: https://data.mef.gov.kh/api/v1/public-datasets/pd_68e370856a965e00074a5e7b/json?page=1&page_size=200
```

### requirements.txt
```bash
Django>=4.2,<5.0
mysqlclient>=2.2.1
django-environ>=0.11

PyMySQL>=1.1
mysql-connector-python>=8.0
djangorestframework-simplejwt>=5.3
drf-spectacular>=0.27
```



```
✅ Option 2 (Drop tables manually)

If you cannot drop DB, run this:

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS 
AUTH_AUDIT_LOG,
LOGIN_HISTORY,
PASSWORD_RESET_TOKENS,
PERMISSIONS,
REFRESH_TOKENS,
ROLES,
ROLE_PERMISSIONS,
USERS,
USER_OTP,
USER_PROFILES,
USER_ROLES,
django_migrations;

SET FOREIGN_KEY_CHECKS = 1;

✔ Disables FK constraints so drop won’t fail
```



### Disable FK checks and delete everything

Run:
```bash
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM USERS;

SET FOREIGN_KEY_CHECKS = 1;
```


```SQL

INSERT INTO USERS (
    CODE,
    USERNAME,
    EMAIL,
    PASSWORD_HASH,
    USER_TYPE,
    EMAIL_VERIFIED,
    PHONE_VERIFIED,
    STATUS,
    IS_SUPERUSER,
    FAILED_LOGIN_ATTEMPTS,
    IS_DELETED,
    CREATED_BY,
    CREATED_AT,
    UPDATED_AT
) VALUES (
    'SYS_ADMIN',
    'sysadmin',
    'riththy.learn@gmail.com',
    '<HASHED_PASSWORD>',
    'SYS',
    1,
    0,
    'ACTIVE',
    1,
    0,
    0,
    1,
    NOW(),
    NOW()
);

INSERT INTO USERS (
    password,
    last_login,
    is_superuser,
    ID,
    CODE,
    USERNAME,
    EMAIL,
    PASSWORD_HASH,
    USER_TYPE,
    EMAIL_VERIFIED,
    PHONE_VERIFIED,
    STATUS,
    FAILED_LOGIN_ATTEMPTS,
    LOCKED_UNTIL,
    PASSWORD_CHANGED_AT,
    IS_DELETED,
    IS_STAFF,
    CREATED_AT,
    UPDATED_AT,
    CREATED_BY,
    UPDATED_BY
) VALUES (
    '$2b$12$dummyhashvaluehere',
    NULL,
    1,
    NULL,
    'SYS_ADMIN',
    'sysadmin',
    'riththy.learn@gmail.com',
    '$2b$12$customhashvaluehere',
    'SYS',
    1,
    0,
    'ACTIVE',
    0,
    NULL,
    NULL,
    0,
    1,
    NOW(),
    NOW(),
    NULL,
    NULL
);

INSERT INTO USER_PROFILES (
    USER_ID,
    NAME,
    NAME_ENGLISH,
    GENDER,
    DOB,
    POB,
    MARITAL_STATUS,
    NATIONAL_ID,
    NATIONALITY,
    OCCUPATION,
    COUNTRY_ID,
    PROVINCE_ID,
    DISTRICT_ID,
    COMMUNE_ID,
    VILLAGE_ID,
    ADDRESS_LINE1,
    ADDRESS_LINE2,
    ZIP_CODE,
    POSTAL_CODE,
    PROFILE_PICTURE_URL,
    SIGNATURE_URL,
    BIO,
    LANGUAGE_PREFERENCE,
    TIMEZONE,
    IS_VERIFIED,
    FACEBOOK_LINK,
    TIKTOK_LINK,
    LINKEDIN_LINK,
    WEBSITE,
    CREATED_BY,
    CREATED_AT,
    UPDATED_AT
)
VALUES (
    1,
    'នី រិទ្ធី',
    'NY RITHY',
    'MALE',
    '1995-08-15',
    'រាជធានីភ្នំពេញ',
    'SINGLE',
    '123456789012',
    'Khmer',
    'System Administrator',
    1,
    NULL,
    NULL,
    NULL,
    NULL,
    'ផ្ទះលេខ 12, ផ្លូវ 271, ភ្នំពេញ',
    'សង្កាត់ទួលទំពូងទី 2',
    '12000',
    '12000',
    'https://example.com/profile.jpg',
    NULL,
    'System admin full access account',
    'km',
    'Asia/Phnom_Penh',
    1,
    'https://facebook.com/rithy',
    'https://tiktok.com/@rithy',
    'https://linkedin.com/in/rithy',
    'https://rithy.dev',
    1,
    NOW(),
    NOW()
);

```


### SQL
SET FOREIGN_KEY_CHECKS = 0; # disable FK checks:
SET FOREIGN_KEY_CHECKS = 1; # enable FK checks:








## Error conflict or rollback
```bash
# ALTERNATIVE (if you CANNOT delete DB):
python manage.py migrate accounts 0001 --fake
python manage.py migrate admin_address 0001 --fake
python manage.py migrate
```

## Error or rollback
```bash
python manage.py migrate admin_address 0001 --fake
python manage.py migrate
```

``` 
ALTER TABLE DISTRICT
DROP FOREIGN KEY DISTRICT_PROVINCE_ID_02a6617e_fk_PROVINCE_ID;

ALTER TABLE DISTRICT
DROP COLUMN PROVINCE_ID;

ALTER TABLE DISTRICT
ADD COLUMN PROVINCE_ID INT AFTER ID; 

SELECT * FROM DISTRICT
WHERE PROVINCE_ID IS NULL;

ALTER TABLE DISTRICT
ADD CONSTRAINT FK_DISTRICT_PROVINCE
FOREIGN KEY (PROVINCE_ID)
REFERENCES PROVINCE(ID)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE COMMUNE
ADD CONSTRAINT FK_COMMUNE_DISTRICT
FOREIGN KEY (DISTRICT_ID)
REFERENCES DISTRICT(ID)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE VILLAGE
DROP COLUMN COMMUNE_ID;

ALTER TABLE VILLAGE
DROP FOREIGN KEY VILLAGE_COMMUNE_ID_91b7bcad_fk_COMMUNE_ID;

ALTER TABLE PROVINCE
ADD COLUMN COUNTRY_ID INT AFTER ID; 

ALTER TABLE PROVINCE
ADD CONSTRAINT FK_PROVINCE_COUNTRY
FOREIGN KEY (COUNTRY_ID)
REFERENCES COUNTRY(ID)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE VILLAGE
ADD CONSTRAINT FK_VILLAGE_COMMUNE
FOREIGN KEY (COMMUNE_ID)
REFERENCES COMMUNE(ID)
ON DELETE RESTRICT
ON UPDATE CASCADE;
``` 



```
INSERT INTO COUNTRY (
    CODE, CODE3, NAME_EN, NAME_KH,
    NATIONALITY_EN, NATIONALITY_KH,
    PHONE_CODE, CURRENCY_CODE,
    ISO_NAME, ISO_NUMERIC,
    CAPITAL_CITY, TIMEZONE,
    CURRENCY_NAME, CURRENCY_SYMBOL,
    LATITUDE, LONGITUDE,
    FLAG_URL,
    SORT_ORDER, IS_ACTIVE,
    CREATED_AT, UPDATED_AT,
    CREATED_BY, UPDATED_BY
) VALUES

-- 🇰🇭 Cambodia
(
    'KH', 'KHM', 'Cambodia', 'កម្ពុជា',
    'Cambodian', 'ខ្មែរ',
    '+855', 'KHR',
    'Kingdom of Cambodia', '116',
    'Phnom Penh', 'Asia/Phnom_Penh',
    'Riel', '៛',
    11.5564, 104.9282,
    'https://flagcdn.com/w320/kh.png',
    1, 1,
    NOW(), NOW(),
    1, NULL
),

-- 🇬🇧 United Kingdom
(
    'GB', 'GBR', 'United Kingdom', 'ចក្រភពអង់គ្លេស',
    'British', 'អង់គ្លេស',
    '+44', 'GBP',
    'United Kingdom of Great Britain and Northern Ireland', '826',
    'London', 'Europe/London',
    'Pound Sterling', '£',
    51.5074, -0.1278,
    'https://flagcdn.com/w320/gb.png',
    2, 1,
    NOW(), NOW(),
    1, NULL
),

-- 🇺🇸 United States
(
    'US', 'USA', 'United States', 'សហរដ្ឋអាមេរិក',
    'American', 'អាមេរិកាំង',
    '+1', 'USD',
    'United States of America', '840',
    'Washington, D.C.', 'America/New_York',
    'US Dollar', '$',
    38.9072, -77.0369,
    'https://flagcdn.com/w320/us.png',
    3, 1,
    NOW(), NOW(),
    1, NULL
);

```