# Welcome to WiseairClient!

WiseairClient is a wrapper to access Air Quality data provided by  [Wiseair](https://www.wiseair.it).


## Data

Our data are gathered real-time by a distributed and capillar network of sensors. 
You can find the openapi specification of the API and the data [here](https://wiseair-development-utils.s3.eu-central-1.amazonaws.com/api-specifications/production/v1/openapi.yml).

## Structure
The main files in this repository are:

- WiseairClient.py: This python module is the bulk of the software. 
- 01-hello-world.ipynb: A "hello world" Jupyter Notebook that shows the functionlities of WiseairClient. 
- 02-hello-world.py: A  "hello world" Python script that shows the functionlities of WiseairClient. 
- sampleData.csv: a short sample of the dataset, to give an immediate idea of the featured dimensions

## Setup

To use WiseairClient:

 1. Download Wiseair App: [here](https://play.google.com/store/apps/details?id=com.wiseair) the Google Play Store link, [here](https://apps.apple.com/it/app/wiseair/id1489703565?l=en&fbclid=IwAR3cegztyvSOKsc2cMU7msV5Lirz5XxA7ZKEV_uAmhrDd39CON5wHU7UmI4) the Apple App Store link
 2. Open the App and register an account.
 3. Visit [https://api.wiseair.it/home](http://api.wiseair.it/home) and login using the credentials of your Wiseair account.
 4. Click "create a new token", insert a name for the token and click "create". The token will appear. Copy it, you will need it in the next step.
 5. Rename "personalAccessTokenMock.csv" in "personalAccessToken.csv".
 6. Open the file with a text editor. Replace XXXXXXXX with your token, and save the file.
 8. Launch the "hello world" script: it will download the data gathered in the last week by one sensor, and store them in sampleData.csv

```
`python3 02-hello-world.py`
```
  ## Troubleshooting & Feedback

If you meet any problem, please [open an issue](https://gitlab.com/wiseair-group/wiseair-client/-/issues/new). If you have cool ideas for new functionalities or you simply want to share with us your opinion, contact us at [contact@wiseair.it](mailto:contact@wiseair.it).



 


