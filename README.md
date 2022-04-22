# Casting Agency

This capstone project developed for the Udacity Fullstack program final homework.

The deployed project demo on heroku is here.
> https://casting-agency-jack.herokuapp.com/

## Role and Permissions

There are three roles with some permissions in this project.
These permissions based on two resources. 

`Casting Assistant`
- get:movie
- get:actor

`Casting Director`
- get:movie
- get:actor
- post:actor
- delete:actor
- patch:actor
- patch:movie

`Executive Producer`
- get:movie
- get:actor
- post:actor
- delete:actor
- patch:actor
- patch:movie
- post:movie
- delete:movie

## Setting up auth0.com for authentication

The variables in `setup.sh` start with `AUTH0` is for authentication.
Make sure every variables be replaced by variables of prepared auth0 account.

The login and logout callback path is `/login_callback` and `/logout_callback` respectively in this project. To setup them, following the step 2 of the next instructions. Because the local domain is `localhost` and local server port is `8080`, the whole path of them are `http://localhost:8080/login_callback`, `http://localhost:8080/logout_callback`.

When auth0.com finished authentication and then callback the localhost, the callback page will store the token in the `localStorage` for next requests. The request module of frontend will append the token in the request header, named `Authorization`. 

If the `auth0.com` account is not prepared, please follow the next steps to prepare it.
1. register the account on auth0.com
2. creating and setting an application, https://auth0.com/docs/get-started/applications/application-settings
3. creating an API, then configure it, https://auth0.com/docs/get-started/apis/api-settings
4. creating the roles as the first section(roles and permission) described, https://auth0.com/docs/manage-users/access-control/configure-core-rbac/roles/create-roles
5. adding permissions mentioned before for these roles, https://auth0.com/docs/manage-users/access-control/configure-core-rbac/roles/add-permissions-to-roles
6. create the users for testing, https://auth0.com/docs/manage-users/user-accounts/create-users
7. attach the role to user for assigning permissions, https://auth0.com/docs/manage-users/access-control/configure-core-rbac/rbac-users/assign-roles-to-users

## Prepare postgres

Install the postgres on different platform
https://www.postgresqltutorial.com/postgresql-getting-started/

In this project, the database name is `postgres`. It can be changed in `setup.sh`.
All tables will be created automatically when the server first started.

## Local development server

1. Make sure the version of python is higher then 3.8
2. enter the project directory
3. run the following command to start the local server

```
# install virtual environment package
pip3 install virtualenv

# create local virtual environment for this project
pip3 -m virtualenv venv

# enable the virtual environment
source ./venv/bin/activate

# install all dependencies
pip3 install -r requirements.txt

# enable the environment variables
source setup.sh

# start the local development server
python3 app.py
```

If the things goes well, we can access the server by next two ways
1. browser, http://localhost:8080
2. curl http://localhost:8080

## Role based access and endpoints explanations

All access of endpoints needs login, if no, there will be an error arise.
```json
{
    "error": 401, 
    "message": "Authorization header missing.", 
    "success": false
}
```

If an user of a role without permissions to access some data, it will get this error.
```json
{
    "error": 403, 
    "message": "The action of user is forbidden.", 
    "success": false
}
```

`GET /api/movies`

> Get the movie list. 

parameters: none

payload: none

The roles with **get:movies** permission will get:
```json
{
    "count": 1, 
    "movies": [
    {
        "id": 2, 
        "release_date": "2022-11-30", 
        "title": "second movie 2"
    }
    ], 
    "success": true
}
```

`GET /api/movies/<int:id>`

> Get a movie's detail. If the movie cannot be found by given id, an 404 error will arise. 

parameters:
- id:int, the movie id

payload: none

The roles with **get:movies** permission will get:
```json
{
    "actors": [
    {
        "age": 20, 
        "gender": false, 
        "id": 1, 
        "name": "Bill"
    }
    ], 
    "movie": {
        "id": 2, 
        "release_date": "2022-11-30", 
        "title": "second movie 2"
    }, 
    "success": true
}
```

`POST /api/movies`

> Create a new movie. If any of name or release_date is missing or cannot be used, an 422 error will arise. 

parameters: none

payload:
- title:str, 
- release_date:str, the date string that will be converted to Date object

```json
{
    "name": "the movie",
    "release_date": "2022-09-30"
}
```

The roles with **post:movies** permission will get:
```json
{
    "movie_id": 16, 
    "success": true
}
```

`PATCH /api/movies/<int:id>/actors`

> Establish the connection between movie and actor. When this process finished, the detail of an actor's movie list will include this movie, plus, the detail of movie's actor list will include this actor. If the given actor is not exist or attach_state is not boolean, 422 error will arise.

parameters:
- id:str, the movie id for associating actors for it

payload:
- actor_id:int, the actor with this will be attached to a movie
- attach_state:bool, true means attach, false means detach

```json
{
    "actor_id": "1",
    "attach_state": true
}
```

The roles with **patch:movies** permission will get:
```json
{
    "success": true
}
```

`PATCH /api/movies/<int:id>`

> Edit the exist movie. If there are not any of two available variables or their type is wrong, it will raise 422 error. If the movie cannot be found by given id, the 404 error will arise.

parameters:
- id:int, the id of movie

payload:
- title:str
- release_date:str

```json
{
    "name": "the movie",
    "release_date": "2022-09-30"
}
```

The roles with **patch:movies** permission will get:
```json
{
    "success": true
}
```

`DELETE /api/movies/<int:id>`

> Delete the exist movie by its id. If the movie is not exist, the 404 error will arise.

parameters:
- id:int, the movie's id

payload: none

The roles with **delete:movies** permission will get:
```json
{
    "success": true
}
```

`GET /api/actors`

parameters: none

The roles with **get:actors** permission will get:
```json
{
    "actors": [
    {
        "age": 20, 
        "gender": true, 
        "id": 1, 
        "name": "Bill"
    }
    ], 
    "count": 1, 
    "success": true
}
```

`GET /api/actors/<int:id>`

> Get the given actor's detail by its id, the result will also include movies his or her associated. If the actor does not exist, there will be an 404 error.

parameters:
- id:int, actor's id

payload: none

The roles with **get:actors** permission will get:
```json
{
    "actor": {
        "age": 20,
        "gender": true,
        "id": 1,
        "name": "Bill"
    },
    "movies": [
        {
            "id": 3,
            "release_date": "2022-09-30",
            "title": "third movie"
        },
        {
            "id": 2,
            "release_date": "2022-12-01",
            "title": "second movie 2"
        }
    ],
    "success": true
}
```

`POST /api/actors`

> To create an actor. If any of parameters in payload is mission or cannot be used, the 422 error will arise.

parameters: none

payload:
- name:str, actor's name
- age:int, actor's age
- gender:bool, true means female, false means male

```json
{
    "name": "Lin",
    "age": 15,
    "gender": false
}
```

The roles with **post:actors** permission will get:
```json
{
    "actor_id": 11,
    "success": true
}
```

`PATCH /api/actors/<int:id>`

> Edit the exist actor by its id. There are three variables can be accepted. Once the request be lunched, at least one variable must load in payload, such as name, age or gender. If the type of variables is wrong, an 422 error will be returned.

parameters:
- id:int, actor's id

payload:
- name:str
- age:int
- gender:bool, true means female, false means male

```json
{
    "name": "Lin",
    "age": 20,
    "gender": false
}
```

The roles with **patch:actors** permission will get:
```json
{
    "success": true
}
```

`DELETE /api/actors/<int:id>`

> Delete the exist actor by its id. If the actor does not exist yet, the 404 error will arise.

parameters:
- id:int, actor's id

payload: none

The roles with **delete:actors** permission will get:
```json
{
    "success": true
}
```

The other common errors' format.

```json
{
    "success": false,
    "error": 404,
    "message": "Not Found"
}

{
    "success": false,
    "error": 405,
    "message": "Method not allowed"
}

{
    "error": 422, 
    "message": "Unprocessable entity", 
    "success": false
}

{
    "error": 500, 
    "message": "Please try again later", 
    "success": false
}
```

## Unit test

Because of authorization, the token should provide with the **test_app.py**. In the root directory of this project, the **test_token.json** includes three roles token for endpoint behavior and role-based access. 

When the token refreshed, the test token should be replaced.

The test-database config can be found in **setup.sh**

Run the unit test command:
```sh
source setup.sh
python3 test_app.py
```