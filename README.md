# testDjango

## Setup

Create virtual environment
```
virtualenv -p python3.6 venv
```
Activate it
```
. venv/bin/activate
```
Run migrations
```
python manage.py migrate
```

## Run
```
python manage.py runserver
# Will run on localhost:8000
```

## Usage
All api enpoints are accesseble on /api/v2/ .
Test models Potato and Tomato with text fields status and decription were created.
## POST
You can create objects with post requests.
```
curl -X POST -d "status=Old&description=Some potato" 127.0.0.1:8000/api/v2/potato/

{"id":1,"description":"=Some potato","status":"Old"}
```

### GET
You can get list of all objects with:
```
curl 127.0.0.1:8000/api/v2/potato/

{"count":2,"next":null,"previous":null,"results":[{"id":1,"description":"Potato object","status":"New"},{"id":2,"description":"Some potato","status":"Old"}]
```
Filter them by one or more fields:
```
curl '127.0.0.1:8000/api/v2/potato/?status=Old&description=Some%20potato'

{"count":1,"next":null,"previous":null,"results":[{"id":5,"description":"Some potato","status":"Old"}]}
```
Sort by field and limit their count in response:
```
curl '127.0.0.1:8000/api/v2/potato/?sort=status&limit=2'

{"count":2,"next":null,"previous":null,"results":[{"id":1,"description":"Potato object","status":"New"},{"id":2,"description":"Potato object","status":"New"}]}
```
Or just get object by id:
```
curl 127.0.0.1:8000/api/v2/potato/2/

{"id":2,"description":"Potato object","status":"New"}
```

### PUT
Use PUT requests for updating objects:
```
curl -X PUT -d "status=New status" '127.0.0.1:8000/api/v2/potato/2/'

{"id":2,"description":"Potato object","status":"New status"}
```

### DELETE
Use DELETE requests for deleting objects:
```
curl -X DELETE '127.0.0.1:8000/api/v2/potato/2/'

```
