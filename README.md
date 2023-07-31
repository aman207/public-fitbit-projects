# Fitbit Fetch script and InfluxDB V2 Grafana integration
A script to fetch data from Fitbit servers using their API and store the data in a local influxdb database. 

## Dashboard Example
![Dashboard](https://github.com/arpanghosh8453/public-fitbit-projects/blob/main/Grafana_Dashboard/Dashboard.png?raw=true)

## Setup instructions

1. Create a new influxdb v2 bucket and token
    - Installation instructions for influxdb can be found at [InfluxDB Install Docs](https://docs.influxdata.com/influxdb/v2.7/install/)
2. Install grafana if not already available
    - [Grafana install instructions](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)
3. Install python dependencies (within a [venv](https://docs.python.org/3/library/venv.html) if required): `python3 -m pip install -r requirements.txt`
4. Create a fitbit application using the fitbit [getting started guide](https://docs.python.org/3/library/venv.html)
    - Many fields can be filled in arbitrarily. However the "OAuth 2.0 Application Type" must be set to `personal` and the "Redirect URL" needs to be `http://localhost:4444` (the port number can be changed. Ensure its updated in the .env file as well)
5. Edit the `.env` file with the required settings
6. On a computer with a web browser, run the token-helper.py script. This will generate the inital `refresh token` and saved to the given file path. A web browser is required for the OAuth authorization
    - If the intent is to run this script on a headless server, copy the resulting `token` file to the server
7. Add the influx database as a datasource in Grafana (if required)
8. Import the dashboard.json file. Change the datasource to your influx database and alter the `bucket` variable (located at the top of the dashboard after importing) to the previously created bucket

You can use the Fitbit_Fetch_Autostart.service template to set up an auto-starting ( and auto-restarting in case of temporary failure ) service in Linux based system ( or WSL )

## Usage

Run the script; if the `token` file does not exist, the script will request a refresh token as input and then will set up the token file. You can check the logs to see the work in progress. The script, by default, keeps running forever, calling different functions at scheduled intervals. 