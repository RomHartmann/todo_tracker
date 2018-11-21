[![CircleCI](https://circleci.com/gh/RomHartmann/todo_tracker.svg?style=svg)](https://circleci.com/gh/RomHartmann/todo_tracker)

Todo list tracker
=================

Simple todo list tracker and manager.

# Installation

## Local Django service

```bash
pipenv install
pipenv run python manage.py migrate
```

This will start on `:8000` by default.

### Docker

```bash
# install docker if needed
docker build -t todo_tracker .
```


## Use

**Local service**
```bash
# run service
pipenv run python manage.py runserver

# run tests
pipenv run python tests/api_tests.py
```

Then you can look at what the test script has created in the DB:
http://localhost:8000/view/

(I didn't clear the test DB on purpose, so that there is something to look at)

**Docker service**
```bash
# start service
docker run -p 8007:8007 todo_tracker

# run tests
pipenv run python tests/api_tests.py --port=8007
```

### REST API

`http://localhost:<port>/api/v1/todo/`  (Default `8000` for django, `8007` for docker)

REST api is built using Django's viewsets, so the basic CRUD functionality is pretty default:

**Create**
- `POST` to `/api/v1/todo/`
- Minimum payload = `{'text': 'todo text'}`
- Full payload = `{'text': 'todo text','state': 'IP','due_at': '2018-11-30 10:12:00'}`
- State has a choice of `(('TD', 'todo'), ('IP', 'in-progress'), ('DN', 'done'))`

**Retrieve**
- `GET` to `/api/v1/todo`  to fetch paginated todo (default = 10 per page) (page with `?page=2`)
- `GET` to `/api/v1/todo/pk/`  to fetch single todo
- `GET` to `/api/v1/todo/fetch_all`  to fetch all todo (custom action on viewset)
- `GET` to `/api/v1/todo?state=IP`  to fetch paginated todo with state `in-progress`
- `get` to `/api/v1/todo/fetch_by_due_at_range/2018-11-19T22:54:52.589846-08:00/2018-11-21T22:54:52.589934/` for todos that have `due_at` in a certain range.

**Update**
- `PATCH` to `/api/v1/todo/pk/` to update specific todo field, eg `{'state': 'DN'}`

**Delete**
- `DELETE` to `/api/v1/todo/pk/` to delete todo


### View
I'd been meaning to re-familiarize myself with web development using Django for a while, and your little project
seemed like such a good vehicle to do that.  So I've attached it in exchange for not just giving it to you sooner. :)

You can find the little UI at  `http://localhost:<port>/view/`  (Default `8000` for django, `8007` for docker)

Tied into the same db as the rest api. 
 
The pagination, sorting and search here happens client side though, so I wouldn't
recommend shipping it to google quite yet (even though it looks so nice).


## Other things in here I was playing around with 

1. `.circleci/config.yml` configuration for free-tier CircleCi.
