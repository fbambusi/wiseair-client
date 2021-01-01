from wiseair.WiseairClient import WiseairClient
client=WiseairClient()
currentMeasures=client.getLiveAirQuality()
potId=currentMeasures["data"][0]["pot_id"]
BEGIN_DATE,END_DATE="2020-11-01","2020-11-11"
data=client.getDataOfPotByInterval(potId,BEGIN_DATE,END_DATE)
from wiseair.WiseairClient import WiseairUtils
utils=WiseairUtils()
data=utils.getPandasDataFrameFromDataOfSingleSensor(data)
data.to_csv("sampleData.csv")

