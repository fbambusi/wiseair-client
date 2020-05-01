import plotly.graph_objects as go
import pandas as pd
import numpy as np
# os.chdir("..")
from wiseair.WiseairClient import WiseairUtils
import statsmodels.api as sm
import pprint

measures = pd.read_csv("examples/measures.csv")
measuresArpa19 = pd.read_csv("examples/arpa_senato_2019.csv")
measuresArpa20 = pd.read_csv("examples/arpa_senato_2020.csv")
measuresArpa = measuresArpa19.append(measuresArpa20)
print(measuresArpa.columns)
measuresArpa.index = pd.to_datetime(measuresArpa["created_at"])
measuresArpa = measuresArpa[measuresArpa["pm2p5"] > 0]

print(measures.head())
measures = measures[measures.created_at > "2019-11-01 10:10:10"]


def plotHistogramOfMeasures(measures):
    measuresByLocation = measures.groupby("location_id")
    counted = measuresByLocation.count()
    fig = go.Figure()

    fig.add_trace(go.Bar(x=counted.index, y=counted.id))
    fig.update_layout(title='Hello Figure')
    fig.show()


# plotHistogramOfMeasures(measures)
interestingLocations = [135, 148, 182, 226]
locationNames = {135: "Viale Piceno", 182: "Via Francesco Predabissi"}
# interestingLocations=[135]
wu = WiseairUtils()

measuresTs = wu.getPandasDataFrameFromDataOfSingleSensor(pollutionData=measures)
measuresTs = wu.filterByDateAndLocations(measuresTs, beginningDate="2019-11-01T10:10:10",
                                         interestingLocations=[135, 148, 182, 226])

measuresTs = measuresTs
# plotHistogramOfMeasures(measures)
fig = go.Figure()
unrestrictedModel = {"level": "smooth trend", "cycle": True, "damped_cycle": True, "stochastic_cycle": True}
dataByLoc = {}

showModel=True

for locationId in interestingLocations:
    currMeasures = measuresTs[measuresTs["location_id"] == locationId]
    currMeas = currMeasures.copy()
    id = currMeas.index
    vals = []
    for idVal in id:
        tup = np.asarray(idVal)
        vals.append(tup[1])
    # print("index is {}".format(id))
    currMeas.index = pd.DatetimeIndex(vals).to_period('4H')
    dataByLoc[locationId] = currMeas

    exceedingMeasures = currMeas[currMeas.pm2p5 > 25]

    pd.DatetimeIndex(vals).to_period('4H')

    if showModel:

        output_mod=sm.tsa.UnobservedComponents(currMeas.pm2p5,**unrestrictedModel)
        outputRes=output_mod.fit(method="powell",disp=False)
        print(outputRes.summary())
        public_props = (name for name in dir(outputRes) if not name.startswith('_'))
        #fig=outputRes.plot_components(legend_loc="lower right",figsize=(15,9))

        fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.cycle["smoothed"], name="cycle"))
        fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.trend["smoothed"], name="trend"))
        fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.predicted_state[0], name="predicted"))

        fig.add_trace(
        go.Scatter(x=currMeasures.index.get_level_values(1), y=currMeas.pm2p5, name="actual @ {}".format( locationNames.get(locationId)  ,locationId)))
        fig.show()
        fig = go.Figure()

    # fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=currMeas.voltage, name="actual"))

currYear = measuresArpa["2020-02-01":"2020-08-01"]
lastYear = measuresArpa["2019-02-01":"2019-08-01"]

wiseirAvg = wu.getPandasDataFrameFromDataOfSingleSensor(pollutionData=measures)
wiseirAvg = wiseirAvg[wiseirAvg.location_id.isin(interestingLocations)].resample(rule="24H").mean()
fig.add_trace(go.Scatter(x=wiseirAvg.index, y=wiseirAvg.pm2p5, name="wiseair avg"))

fig.add_trace(go.Scatter(x=currYear.index, y=currYear.pm2p5, name="arpa 2020"))
fig.add_trace(go.Scatter(x=currYear.index, y=lastYear.pm2p5, name="arpa 2019"))

fig.add_shape(
    # Line Horizontal
    type="line",
    x0="2020-02-01 10:10:10",
    y0=25,
    x1="2020-04-25 10:10:10",
    y1=25,
    line=dict(
        color="LightSeaGreen",
        width=4,
        dash="dashdot",
    ),
    name="limite OMS"
)

deltas = pd.DataFrame(
    dataByLoc[182]["2020-02-01":"2020-03-29"].pm2p5 - dataByLoc[135]["2020-02-01":"2020-03-29"].pm2p5).dropna()
print(deltas)

fig.add_trace(go.Scatter(x=pd.to_datetime(deltas.index.to_series().astype(str)), y=deltas.pm2p5, name="delta 2019"))
print( (dataByLoc[182]["2020-02-01":"2020-02-29"].pm2p5 - dataByLoc[135]["2020-02-01":"2020-02-29"].pm2p5).mean() )
print( ( dataByLoc[182]["2020-03-01":"2020-03-29"].pm2p5 - dataByLoc[135]["2020-03-01":"2020-03-29"].pm2p5).mean() )
fig.show()

fig.update_xaxes(
    rangeslider_visible=True,
    tickformatstops=[
        dict(dtickrange=[None, None], value="%a %m-%d"),

    ]
)
