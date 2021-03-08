# locate-iss
Simple Python program to find the ISS using Open Notify API

This code is also prepared to run using **Heroku**(https://www.heroku.com) deployment with GitHub integration.

## Usage

### Online version (Heroku)
Access [**locate-iss**](https://locate-iss.herokuapp.com/) web to see the app running

This [tutorial](https://austinlasseter.medium.com/how-to-deploy-a-simple-plotly-dash-app-to-heroku-622a2216eb73) has been used as reference for the Heroku deployment

### Local mode
In order to run the web server in a local environment with Dash do the following:

- Localhost mode: 
run the app with the HEROKU_DEPLOY flag set to True (app.py)

start the server with
```
python app.py
```

this will create a web server running on: http://127.0.0.1:8050/

- Local network mode:
run the app with the HEROKU_DEPLOY flag set to False (app.py), set the other parameters like PORT and HOST (ip)
  
then start the server with 
```
python app.py
```

This will start the server on the given HOST ip and PORT and all the devices connected to the intranet should
be able to access the site