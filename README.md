# capstone
This is the final project of Udacity's FSND course.
I signed up for this course in order to sharpen my web development skills.

# Start Server 
To start server, on the Command Line:
pip3 install -r requirements.txt
python3 app.py

# Automated Testing
To run tests, on the Command Line:
source ./setup.sh
python3 tests.py

# Manual Testing
I saved the Postman export as capstone.postman_collection.json.

# JWTs
Saved in setup.sh, as well as in the Postman Collection.

# JWT Expiration
I disabled the option for JWT Expiration Checking in the jwt.decode() method call so that my JWTs wouldn't expire prior to code review.


# Expected endpoints and behaviors

GET '/actors'
Fetches a dictionary of actors and their attributes.
Request Arguments: None
Returns: see below
{
    "actors": [
        {
            "age": 60,
            "gender": "M",
            "id": 1,
            "movies": [],
            "name": "Tom Cruise"
        }
    ],
    "success": true
}


POST '/actors'
Sends a post request in order to add a new actor.
Request Arguments: None
Input: actor attributes - see example below
{
    "name": "Tom Cruise",
    "age": 60,
    "gender": "M"
}
Returns: see example below
{
    "actor": {
        "age": 60,
        "gender": "M",
        "id": 1,
        "movies": [],
        "name": "Tom Cruise"
    },
    "success": true
}



PATCH '/actors/<actor_id>'
Input - 1 or more attributes to be updated - see example below
Request Arguments: actor_id
{
    "name": "Tom Hanks",
    "age": 66
}
returns: updated actor record - see example below
{
    "success": true,
    "updated": {
        "age": 66,
        "gender": "M",
        "id": 1,
        "movies": [],
        "name": "Tom Hanks"
    }
}


DELETE '/actors/<actor_id>'
Deletes a specified actor using actor_id.
Request Arguments: actor_id 
Returns: actor_id of deleted actor, and success status.  See example below -
{
    "delete": "1",
    "success": true
}


GET '/movies'
Fetches a dictionary of movies and their attributes.
Request Arguments: None
Returns: see below
movies": [
        {
            "actors": [
                {
                    "age": 60,
                    "gender": "M",
                    "id": 1,
                    "name": "Tom Cruise"
                }
            ],
            "id": 1,
            "release_date": "Fri, 16 May 1986 05:00:00 GMT",
            "title": "Top Gun"
        }
    ],
    "success": true
}


POST '/movies'
Sends a post request in order to add a new movie.
Request Arguments: None
Input: movie attributes - see example below
{
    "title": "Top Gun",
    "release_date": "1986-05-16"
}
Response:
{
    "movie": {
        "actors": [],
        "id": 1,
        "release_date": "Fri, 16 May 1986 05:00:00 GMT",
        "title": "Top Gun"
    },
    "success": true
}


PATCH '/movies/<movie_id>'
Input - 1 or more attributes to be updated - see example below
Request Arguments: see example below
{
    "title": "Rainman",
    "release_date": "1988-12-12"
}
Returns: see example below
{
    "success": true,
    "updated": {
        "actors": [],
        "id": 1,
        "release_date": "Mon, 12 Dec 1988 05:00:00 GMT",
        "title": "Rainman"
    }
}


DELETE '/movies/<movie_id>'
Deletes a specified movie using movie_id.
Request Arguments: movie_id 
Returns: movie_id of deleted movie, and success status.  See example below -
{
    "delete": "1",
    "success": true
}


PATCH /movies/1/add_actor
Associates an actor to a movie.
Request Arguments: movie_id of movie to be updated
Input: actor_id of actor to add to the movie
{
    "actor_id": 1
}
Returns: the updated movie
{
    "success": true,
    "updated_movie": {
        "actors": [
            {
                "age": 60,
                "gender": "M",
                "id": 1,
                "name": "Tom Cruise"
            }
        ],
        "id": 1,
        "release_date": "Fri, 16 May 1986 05:00:00 GMT",
        "title": "Top Gun"
    }
}


PATCH /movies/1/delete_actor
Deletes an actor from a movie.
Request Arguments: movie_id of movie to be updated
Input: actor_id of actor to delete from the movie
{
    "actor_id": 1
}
Returns: the updated movie
{
    "success": true,
    "updated_movie": {
        "actors": [],
        "id": 1,
        "release_date": "Fri, 16 May 1986 05:00:00 GMT",
        "title": "Top Gun"
    }
}
