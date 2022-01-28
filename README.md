# CITY SENSOR
#### Video Demo:  https://locationcs50.herokuapp.com/
#### Description:

- Introduction:

CITY SENSOR is a smart city project that collects sensor data across the city and displays it on the map. In this initial version, it have been collected how much lighting there is in the streets that the user walks through, it can be used both during the day and at night.
The app collects the amount of light through the smartphone's sensor and records it with the GPS location, date and time.
The data is shared with the website that stores it in the database. It is possible to visualize data using filters by time or day/night.
With the map it is possible determine which streets or regions are darker and need improvement.
The initial idea was to make the sensors together with arduino or raspberry py, but due to the practicality and cost, I decided to use a smartphone. The advantage is also the ease of sharing the application, making the tool available to everyone.

- Project explanation: 

This project has two parts: the app and the website. The app was made in Android Studio with Java and the site is a flask webapplication hosted in Heroku.

The comunication between app and website is made with a post request sending a JSON content. This JSON is must have this format:
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

The webaplication will transform this JSON and store all the data in a database named `location.db`.

To present the data on the map, is used a script in Javascript from [mapbox](https://docs.mapbox.com/mapbox-gl-js/api/). This creates a map and puts colored circles on it. All tranfer of data is in [GeoJSON](https://geojson.org/) format. Mapbox recognizes the points and sensor values plots the map.

It is possible to visualize data using filters by a period of time and a function will determine which is the best map theme to show and automatically adjust the color scale.  


- Project files: 

`application.py`: The project core, configures Flask and all routes to webapplication, connects to database too;  
`helpers.py`: Cointais functions to handle with database , JSON and GeoJSON formats;  
`aux_save.py`: Only used to mannualy read backup files and store then on database;  
`storage/`: backup folder and for manual input;  
`static/`: .css and image files, used on the site;  
`templates`: .html files that communicate each other through jinja2;  
`location.db`: SQLite[^note].  


[^note]: To store the data, it was used SQLite3. But I realized that SQLite3 is not good on a deploy environment. Heroku and other servers cleans the file list every day and everything updated is lost. Also the WSGI system in the server creates a copy of the enviroment and the changes in the files are lost when the environment is closed. To solve this, I'll add PostgreSQL to store every new data from app while SQLite3 stores the old data.
Heroku's PostgreSQL has a limit fo 10.000 rows, when it is almost full, the data will be tranfered from PostgreSQL to SQLite3 and they will work together.





