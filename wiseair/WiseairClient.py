# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

# In[82]:


import csv
import requests
import json
import pandas as pd
import json
import datetime
from datetime import date
from datetime import timedelta


class WiseairClient:

    def __putJson(self, url, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(self.__userToken)
        r = requests.put(url, data=json.dumps(data), headers=headers)
        return r

    def __postJson(self, url, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(self.__userToken)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return json.loads(r.content.decode("utf-8"))

    def __getJson(self, url, data):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(self.__userToken)
        r = requests.get(url, data=json.dumps(data), headers=headers)
        return json.loads(r.content.decode("utf-8"))

    def __getClientToken(self, clientId, clientSecret):
        url = self.__baseUrl + "/oauth/token"
        data = {"client_id": clientId, "client_secret": clientSecret, "grant_type": "client_credentials"}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return json.loads(r.text)["access_token"]

    def __getPersonalToken(self, userEmail, userPassword, clientToken):
        url = self.__baseUrl + "/api/auth/login"
        data = {"email": userEmail, "password": userPassword, "grant_type": "client_credentials"}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(clientToken)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return json.loads(r.text)["access_token"]

    def __init__(self, pathToClientCredentials="personalAccessToken.csv", baseUrl="https://api.wiseair.it"):

        with open(pathToClientCredentials, "r") as csvFile:
            dic = csv.DictReader(csvFile)
            for row in dic:
                token = row["personalAccessToken"]

        self.__baseUrl = baseUrl
        self.__userToken = token

    def __getIntervalBetweenLastTenMeasures(self, potId, fromDate, toDate):
        results = self.getDataOfPotByInterval(potId, fromDate, toDate)
        df = pd.DataFrame(results)
        df['ts'] = pd.DatetimeIndex(df.created_at).asi8 // (10 ** 9)
        return df["ts"].diff()[1:]

    def __isHavingRegularPace(self, timeIntervalBetweenLastMeasuresInSecond):
        variance = np.std(timeIntervalBetweenLastMeasuresInSecond)
        mean = np.mean(timeIntervalBetweenLastMeasuresInSecond)
        rep = variance / mean

        # extremely regular: std/mean close to zero: 0.003 for correct sensor
        # 1.22 for exponential sleep
        if rep > 0.2:
            return False
        return True

    def lastTenMeasuresOfSensorAreEquallyPaced(self, sensorId):
        today = date.today()
        differences = self.__getIntervalBetweenLastTenMeasures(sensorId, str(today - timedelta(days=1)),
                                                               str(today + timedelta(days=1)))
        return self.__isHavingRegularPace(differences[-10:])

    def getDataOfPotByPage(self, pot_id, pageNr):
        url = self.__baseUrl + "http://www.wiseair.it/backend-test/public/measures/by-pot/{}?page={}".format(pot_id,
                                                                                                             pageNr)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(self.__userToken)
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)["data"]
        return data

    def getDataOfPotByInterval(self, pot_id, fromDate, toDate):
        url = self.__baseUrl + "/api/measures-by-time-interval"
        data = {"until_date": toDate, "from_date": fromDate, "pot_id": pot_id}
        print(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        headers["Authorization"] = "Bearer {}".format(self.__userToken)
        r = requests.get(url, data=json.dumps(data), headers=headers)
        return json.loads(r.text)

    def createPot(self, longitude, latitude):
        data = {"latitude": latitude, "longitude": longitude, "pm2p5": -1, "pm10": -1}
        url = self.__baseUrl + "/api/create-pot"
        print(url)
        print(data)
        response = self.__postJson(url, data)
        return response

    def registerPot(self, activationCode, country, city, streetName, houseNumber, postalCode):
        data = {
            "activation_token": activationCode,
            "streetname": streetName,
            "housenumber": houseNumber,
            "city": city,
            "postalcode": postalCode
        }
        url = self.__baseUrl + "/api/activate-pot"
        response = self.__putJson(url, data)
        print(response)
        print(response.content)

    def createMeasure(self, chipId="", pm1=-1, pm2p5=-1, pm4=-1, pm10=-1, humidity=-1, temperature=-1, voltage=-1):
        data = {
            "chip_id": chipId,
            "pm2p5": pm2p5,
            "pm10": pm10,
            "humidity": humidity,
            "temperature": temperature,
            "voltage": voltage,
            "pm1SPS": pm1,
            "pm2p5SPS": pm2p5,
            "pm10SPS": pm10,
            "pm4SPS": pm4}
        url = self.__baseUrl + "/measures/createV2"
        response = self.__postJson(url, data)
        return response

    def getAllLocations(self):
        url = self.__baseUrl + "/api/get-all-locations"
        response = self.__getJson(url, {})
        return response

    def getStateOfPots(self, page=1):
        data = {
            "page": page,
        }
        url = self.__baseUrl + "/api/get-state-of-pots"
        response = self.__getJson(url, data)
        return response

    def getLiveAirQuality(self, latitude="45.458453", longitude="9.1782493", page=0):
        data = {
            "longitude": longitude,
            "latitude": latitude,
            "tolerance": "40",
            "untilDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": 100,
            "page": page
        }
        url = self.__baseUrl + "/api/live-air-quality"
        response = self.__getJson(url, data)
        return response


class WiseairUtils:
    def __init__(self):
        pass

    def getPandasDataFrameFromDataOfSingleSensor(self, pollutionData):
        data = pd.DataFrame(pollutionData)
        data["created_at"] = pd.to_datetime(data["created_at"])
        data.index = data["created_at"]
        # data.drop("created_at",axis=1,inplace=True)
        return data

    FORMAT_STRING_WITH_HOURS = "%Y-%m-%dT%H:%M:%S"
    THRESHOLDS = {"pm2p5": {"limit": 25}, "pm10": {"limit": 25}}

    def filterByDateAndLocations(self, pollutionData, beginningDate="2000-01-01T10:10:10",
                                 endDate="2100-01-01T10:10:10", interestingLocations=[]):
        condition = np.zeros(len(pollutionData), dtype=np.int8)
        for locationId in interestingLocations:
            condition = condition | (pollutionData.location_id == locationId)
            # print(condition)
        pollutionData = pollutionData[condition]
        begD = datetime.datetime.strptime(beginningDate, "%Y-%m-%dT%H:%M:%S")
        endD = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")
        pollutionData = pollutionData[pollutionData.created_at > begD]
        pollutionData = pollutionData[pollutionData.created_at < endD]
        return pollutionData.groupby("location_id").resample(rule="4H").mean()

    def getSummaryOfPeriod(self, pollutionData, beginningDate="2000-01-01T10:10:10",
                           endDate="2100-01-01T10:10:10"):
        formatStringWithHour = WiseairUtils.FORMAT_STRING_WITH_HOURS
        begD = datetime.datetime.strptime(beginningDate, formatStringWithHour)
        endD = datetime.datetime.strptime(endDate, formatStringWithHour)
        pollutionData = pollutionData[pollutionData.created_at > begD]
        pollutionData = pollutionData[pollutionData.created_at < endD]
        summary = {}
        quantities = ["pm2p5", "pm10"]
        for quantity in quantities:
            curr = {}
            curr["mean"] = pollutionData[quantity].mean()
            curr["std"] = pollutionData[quantity].var() ** 0.5
            dailyMean=pollutionData.resample(rule="24H").mean()
            dailyMeanTooMuch=len(dailyMean[dailyMean[quantity]>WiseairUtils.THRESHOLDS[quantity]["limit"]])
            dailyMeanOk = len(dailyMean[dailyMean[quantity] <= WiseairUtils.THRESHOLDS[quantity]["limit"]])
            curr["excessDays"]=dailyMeanTooMuch
            curr["daysOk"] = dailyMeanOk

            summary[quantity] = curr
        return summary
