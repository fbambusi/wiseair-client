import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import plotly.express as px
os.chdir("..")
from WiseairClient import  WiseairUtils
measures=pd.read_csv("examples/measures.csv")
print(measures.head())
measures=measures[measures.created_at>"2019-11-01 10:10:10"]

def plotHistogramOfMeasures(measures):

    measuresByLocation=measures.groupby("location_id")
    counted=measuresByLocation.count()
    fig = go.Figure()

    fig.add_trace(go.Bar(x=counted.index,y=counted.id))
    fig.update_layout(title = 'Hello Figure')
    fig.show()

#plotHistogramOfMeasures(measures)
#interestingLocations=[135,148,182,226]
interestingLocations=[135]

condition=np.zeros(len(measures),dtype=np.int8)
for locationId in interestingLocations:
    condition=condition| (measures.location_id==locationId)
    print(condition)
measures=measures[condition]
measuresTs=WiseairUtils().getPandasDataFrameFromDataOfSingleSensor(pollutionData=measures)

#plotHistogramOfMeasures(measures)
fig = go.Figure()
for locationId in interestingLocations:
    currMeasures=measuresTs[measuresTs["location_id"] == locationId]
    print(measuresTs.columns)
    currMeasures = currMeasures.resample(rule="4H").mean()
    fig .add_trace( go.Scatter(x=currMeasures.index, y=currMeasures.pm2p5,name=locationId))
fig.update_xaxes(
    rangeslider_visible=True,
    tickformatstops = [
        dict(dtickrange=[None, None], value="%a %m-%d"),

    ]
)

fig.show()