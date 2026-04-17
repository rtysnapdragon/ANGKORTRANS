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
py install 3.12

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


### Check list package
pip list
pip show mysqlclient

## Stay in activated venv then install from requirements.txt to install all packages to project
pip install -r requirements.txt

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