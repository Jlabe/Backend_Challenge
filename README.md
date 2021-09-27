# Backend_Challenge

## Install Dependencies
```shell script
pip install -r requirements.txt
```
## How to run the server

```shell script
python manage.py runserver
```

## How to run the tests

```shell script
python manage.py test
```

## Example JSON post body for /create

```shell script
curl --location --request POST 'http://127.0.0.1:8000/create/' --header 'Content-Type: application/json' --data-raw '[1,3,5]'
```

## Example JSON post body for /validate

```shell script
curl --location --request POST 'http://127.0.0.1:8000/validate/' --header 'Content-Type: application/json' --data-raw '{
    "access_token" :"8d2d32d1-b4e9-482d-971d-7c5de98bb59a",
    "door_id" : 1
}'
```