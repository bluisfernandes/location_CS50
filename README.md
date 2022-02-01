# CITY SENSOR
#### Video Demo: https://youtu.be/o84bxhz6pPQ
#### website: https://locationcs50.herokuapp.com/
#### Description:

## Introduction

CITY SENSOR is a smart city project that collects light data across the city and displays it on the map. In this initial version, it has been collected how much light there is in the streets that the user walks through, both during day and night. 
The app collects the amount of light through the smartphone's sensor and records it with the GPS location, date and time.
The data is uploaded to a website and all the information is stored. It is possible to visualize the data using filters by time or day/night.
Through the map it is possible to identify which streets or regions are darker and need light improvements.
The initial idea was to develop the sensors using arduino or raspberry py, but due to the practicality and cost, I decided to use a smartphone. An additional advantage is that the application can be easily shared, making the tool available to everyone.

## Project explanation 

This project has two parts: the app and the website. The app was made in Android Studio with Java, and the website is a flask webapplication hosted in Heroku.

The comunication between app and website is made with a post request, sending a JSON. This JSON content must have the following format:
```
{
    "id": 1,
    "device": "device_name",
    "points":[{
        "lat": 123.456, 
        "long": 987.654 
        },
        {"lat": 123.457,
        "long": 987.655 
    }],
    "info":[{"point_id":0,
            "route_id":0,
            "sensor_light":13333.3,
            "timestamp":"2022-01-11T00:59:53.372"
            },
            {"point_id":1,
            "route_id":0,
            "sensor_light":13345.9,
            "timestamp":"2022-01-11T00:59:54.926"
    }]
}
```

The webapplication transforms this JSON and stores all the data in a database named `location.db`.

To display the data on the map, it is used a script in Javascript from [mapbox](https://docs.mapbox.com/mapbox-gl-js/api/). This creates a map and puts colored circles on it. All data transfer is in [GeoJSON](https://geojson.org/) format. Mapbox recognizes the points and sensor values, plotting the map.

It is possible to visualize the data using filters by a period of time and a function will determine which is the best map theme to show and automatically adjust the color scale.  


## Project files 

`application.py`: The project core, configures Flask and all routes to webapplication, connects to database too;  
`helpers.py`: Contains functions to handle database , JSON and GeoJSON formats;  
`aux_save.py`: Only used to manually read backup files and store them on database;  
`storage/`: backup folder and used for manual input;  
`static/`: .css and image files, used on the site;  
`templates`: .html files that communicate with each other through jinja2;  
`location.db`: SQLite[^note].


## How to run

Install the libraries of `requirements.txt` or create a virtual environment.
```
export FLASK_APP=application.py  
flask run
```
clik in the link on the prompt, like  `http://127.0.0.1:5000/`



[^note]: To store the data, it was used SQLite. But I realized that SQLite doesn´t work properly on a deployment environment. Heroku and other servers cleans the file list every day and everything updated is lost. Also the WSGI system in the server creates a copy of the environment and the changes in the files are lost when the environment is closed. To solve this issue, I'll add PostgreSQL to store every new data from app while SQLite stores the old data.
Heroku's PostgreSQL has a limit of 10.000 rows, when almost achieve its full capacity, the data will be tranfered from PostgreSQL to SQLite working together.


