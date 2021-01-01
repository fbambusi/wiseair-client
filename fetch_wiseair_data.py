from wiseair.WiseairClient import WiseairClient

wc=WiseairClient()
live_aq_data=wc.getLiveAirQuality(45.4773,9.1815)["data"]
for measure in live_aq_data:
  BEGIN_DATE,END_DATE="2020-02-15","2020-03-11"
  data=wc.getDataOfPotByInterval(measure["pot_id"],BEGIN_DATE,END_DATE)
  print(measure)
  print(data)


