# Art Gallery API Backend

## About

This API is designed to help create and manage an Art Gallery, with the ability to specify and organize which mediums a Curator would like to showcase. Access to endpoints is controlled by specific roles. Curators may manage which mediums and artworks are presented in the gallery, while Artists may add/update/remove artworks. Public access allows for unrestricted viewing of artwork information.

https://cgriffith-udacity-capstone.herokuapp.com

#### Key Dependencies

Be sure to have the following dependencies installed

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Getting Started

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv env
  $ source env/bin/activate
  ```
  
2. Install the dependencies. Note that some may dependencies may require a manual installation
  ```
  $ pip install -r requirements.txt
  ```

3. Configure [setup.sh](setup.sh) to your database for DATABASE_URI and TEST_URI. Then run the below commands
  ```
  $ createdb gallery # use your db name
  $ . setup.sh
  ```

4. Run the development server for local development:
  ```
  $ export FLASK_APP=manage.py
  $ export FLASK_ENV=development # enables debug mode
  $ flask run --reload
  ```

5. Backend is hosted at http://127.0.0.1:5000/

## Testing
To run the tests for local development, run the following in command line.
  ```
  $ . run_tests.sh
  ```

Otherwise, the provided Postman collection can be used to test the API endpoints and authentication.

  ```
    [udacity-capstone-gallery-live.postman_collection.json](udacity-capstone-gallery-live.postman_collection.json)
    [udacity-capstone-gallery-live.postman_test_run.json](udacity-capstone-gallery-live.postman_test_run.json)
  ```

# Roles
This API has two main roles: Curator and Artist.

### Curator
Curators are able to manage mediums and artworks in the gallery. They have access to the following permissions:
`post:medium` `patch:medium` `delete:medium` `post:artwork` `patch:artwork` `delete:artwork` 

### Artist
Curators are only able to manage artworks in the gallery. They have access to the following permissions:
`post:artwork` `patch:artwork` `delete:artwork`

# Authentication

User authentication is required to use the API endpoints. Below are examples of curl commands that can be used to test these endpoints. The Postman collection [udacity-capstone-gallery-live.postman_collection.json](udacity-capstone-gallery-live.postman_collection.json) may also be used to test the endpoints on the heroku deployment at https://cgriffith-udacity-capstone.herokuapp.com.

The required JWT Tokens may be found inside [setup.sh](setup.sh) 

## Read - Public access

#### GET /artworks

```
curl -X GET \
  https://cgriffith-udacity-capstone.herokuapp.com/artworks \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

#### GET /artworks/<int:artwork_id>

```
curl -X GET \
  https://cgriffith-udacity-capstone.herokuapp.com/artworks/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

#### GET /mediums

```
curl -X GET \
  https://cgriffith-udacity-capstone.herokuapp.com/mediums \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

#### GET /mediums/<int:medium_id>

```
curl -X GET \
  https://cgriffith-udacity-capstone.herokuapp.com/mediums/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

## Manage Artworks - Curator and Artist access

#### POST /artworks
`post:artwork`

```
curl -X POST \
  https://cgriffith-udacity-capstone.herokuapp.com/artworks \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
-H 'Content-Type: application/json' \
  -d '{
    "title": "Lorem Ipsum",
    "medium": "charcoal drawing",
    "year": 2011,
    "image_link": "https://i.picsum.photos/id/103/2592/1936.jpg?hmac=aC1FT3vX9bCVMIT-KXjHLhP6vImAcsyGCH49vVkAjPQ",
    "medium_id": 1
}'
```

#### PATCH /artworks/<int:artwork_id>
`patch:artwork`

```
curl -X PATCH \
  https://cgriffith-udacity-capstone.herokuapp.com/artworks/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Lorem Ipsum",
    "medium": "graphite drawing",
    "year": 2012,
    "image_link": "https://i.picsum.photos/id/103/2592/1936.jpg?hmac=aC1FT3vX9bCVMIT-KXjHLhP6vImAcsyGCH49vVkAjPQ",
    "medium_id": 1
}'
```

#### DELETE /artworks/<int:artwork_id>
`delete:artwork`

```
curl -X DELETE \
  https://cgriffith-udacity-capstone.herokuapp.com/artworks/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \
```

## Manage Mediums - Curator access

#### POST /mediums
`post:medium`

```
curl -X POST \
  https://cgriffith-udacity-capstone.herokuapp.com/mediums \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
-H 'Content-Type: application/json' \
  -d '{
    "title": "Drawings"
}'
```

#### PATCH /medium/<int:medium_id>
`patch:medium`

```
curl -X PATCH \
  https://cgriffith-udacity-capstone.herokuapp.com/mediums/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Mixed Media"
}'
```

#### DELETE /mediums/<int:medium_id>
`delete:medium`

```
curl -X DELETE \
  https://cgriffith-udacity-capstone.herokuapp.com/mediums/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \
```

# Full Endpoint Descriptions

### Errors

The API will return the following errors:

#### 400 Bad request
- Sending invalid JSON will result in a ```400 Bad Request``` response.

    ```
    {
        "success": False,
        "error": 400,
        "message": "Bad request"
    }
    ```

#### 404 Resource not found
- Failure for the server to find the requested url will result in a ```404 Resource Not Found``` response.

    ```
    {
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }
    ```

#### 422 Unprocessable
- Sending invalid fields will result in a ```422 Unprocessable Entity``` response.

    ```
    {
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }
    ```

#### 500 Internal server error 
- Unexpected errors preventing the fullfillment of the request will result in a ```500 Internal Server Error ``` response.

    ```
    {
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }
    ```

### Endpoints

#### GET /mediums
- Fetches an array of json objects containing the id and title values of each medium
- Request Arguments: None
- Returns: Response body containing the following key
    `mediums`: An array containing json objects containing Medium id, and Medium title

```
{
    "mediums": [
        {
            "id": 1,
            "title": Drawing
        },
        {
            "id": 2,
            "title": Painting
        }
    ], 
    "success": true
}
```

#### POST /mediums
- Requires post:medium permission
- Creates a new medium and inserts it into the database
- Request Arguments: 

    `title`: A string value containing the entry name

```
{
  "medium": {
    "title": "Mixed Media"
  }
}
```

- Returns: Response body containing the following key

    `created`: An integer indicating id of the new medium entry created

```
{
    "created": 5,
    "success": true
}
```

#### GET /mediums/<int:medium_id>
- Fetches the values of an existing medium in the database based on the specified medium_id
- Request Arguments: 
    
    `medium_id`: A number value indicating the Medium id of the entry
    
- Returns: Response body containing the following keys

    `medium_id`: A number value indicating the Medium id of the entry
    
    `title`: A string value containing the entry name
    
    `artworks`: An array containing json objects containing Artwork id, Artwork title, and Artwork image_link

```
{
    "medium_id": 1,
    "title": Drawing,
    "artworks": [
        {
            "id": 3,
            "title": Lorem Ipsum,
            "image_link": "https://loremipsum..."
        },
    ],
    "success": true
}
```

#### PATCH /mediums/<int:medium_id>
- Requires patch:medium permission
- Updates the values of an existing medium in the database based on the specified medium_id
- Request Arguments:

    `medium_id`: A number value indicating the Medium id of the entry

    `title`: A string value containing the entry name

```
{
  "medium": {
    "title": "Mixed Media"
  }
}
```

- Returns: Response body containing the following key

    `updated`: An integer indicating id of the medium entry updated

```
{
    "updated": 5,
    "success": true
}
```

#### DELETE /mediums/<int:medium_id>
- Requires delete:medium permission
- Deletes an existing medium in the database based on the specified medium_id
- Request Arguments: 

    `medium_id`: A number value indicating the Medium id of the entry to be deleted
    
- Returns: Response body containing the following key

    `deleted`: A number value indicating the Medium id of the entry deleted

```
{
    "deleted": 3
}
```

#### GET /artworks
- Fetches an array of json objects containing the id, title, and image_link values of each artworks
- Request Arguments: None
- Returns: Response body containing the following key

    `artworks`: An array containing json objects containing Artwork id, Artwork title, and Artwork image_link

```
{
    "artworks": [
        {
            "id": 3,
            "title": Lorem Ipsum,
            "image_link": "https://loremipsum..."
        },
    ], 
    "success": true
}
```

#### POST /artworks
- Requires post:artwork permission
- Creates a new artwork and inserts it into the database
- Request Arguments: 

    `title`: A string value containing the entry name

    `medium`: A string value describing materials used

    `year`: A number value indicating year created

    `image_link`: A string value containing the image hyperlink

    `medium_id`: A number value indicating the Medium id of the associated medium

```
{
  "medium": {
    "title": Lorem Ipsum,
    "medium": "charcoal on paper",
    "year": 2011,
    "image_link": "https://loremipsum...",
    "medium_id": 1
  }
}
```

- Returns: Response body containing the following key

    `created`: An integer indicating id of the new medium entry created

```
{
    "created": 3,
    "success": true
}
```

#### GET /artworks/<int:artwork_id>
- Fetches the values of an existing artwork in the database based on the specified artwork_id
- Request Arguments: 

    `artwork_id`: A number value indicating the Artwork id to match

- Returns: Response body containing the following keys

    `title`: A string value containing the entry name

    `medium`: A string value describing materials used

    `year`: A number value indicating year created

    `image_link`: A string value containing the image hyperlink

    `medium_id`: A number value indicating the Medium id of the associated medium

```
{
    "artwork_id": 3,
    "title": Lorem Ipsum,
    "medium": "charcoal on paper",
    "year": 2011,
    "image_link": "https://loremipsum...",
    "medium_id": 1,
    success: true
}
```

#### PATCH /artworks/<int:artwork_id>
- Requires patch:artwork permission
- Updates the values of an existing artwork in the database
- Request Arguments: 

    `title`: A string value containing the entry name

    `medium`: A string value describing materials used

    `year`: A number value indicating year created

    `image_link`: A string value containing the image hyperlink

    `medium_id`: A number value indicating the Medium id of the associated medium

```
{
  "medium": {
    "title": Lorem Ipsum,
    "medium": "charcoal on paper",
    "year": 2011,
    "image_link": "https://loremipsum...",
    "medium_id": 1
  }
}
```

- Returns: Response body containing the following key

    `updated`: An integer indicating Artwork id of the entry updated

```
{
    "created": 3,
    "success": true
}
```

#### DELETE /artworks/<int:artwork_id>
- Requires delete:artwork permission
- Deletes an existing artwork in the database based on the specified artwork_id
- Request Arguments: 

    `artwork_id`: A number value indicating the Artwork id to match

- Returns: Response body containing the following key

    `deleted`: An integer indicating Artwork id of the entry deleted

```
{
    "deleted": 3,
    "success": true
}
```
