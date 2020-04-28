import plotly.graph_objects as go
import pandas as pd
import numpy as np
# os.chdir("..")
from src.WiseairClient import WiseairUtils
import statsmodels.api as sm
import pprint

measures = pd.read_csv("examples/measures.csv")
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
# interestingLocations=[135]


measuresTs = WiseairUtils().getPandasDataFrameFromDataOfSingleSensor(pollutionData=measures)
measuresTs = WiseairUtils().filterByDateAndLocations(measuresTs, beginningDate="2019-11-01T10:10:10",
                                                   interestingLocations=[135, 148, 182, 226])

measuresTs = measuresTs
# plotHistogramOfMeasures(measures)
fig = go.Figure()
unrestrictedModel = {"level": "smooth trend", "cycle": True, "damped_cycle": True, "stochastic_cycle": True}

for locationId in interestingLocations:
    currMeasures = measuresTs[measuresTs["location_id"] == locationId]
    currMeas=currMeasures.copy()
    id=currMeas.index
    vals=[]
    for idVal in id:
        tup=np.asarray(idVal)
        vals.append(tup[1])
    #print("index is {}".format(id))
    currMeas.index=    pd.DatetimeIndex(vals).to_period('4H')
    output_mod=sm.tsa.UnobservedComponents(currMeas.pm2p5,**unrestrictedModel)
    outputRes=output_mod.fit(method="powell",disp=False)
    print(outputRes.summary())
    public_props = (name for name in dir(outputRes) if not name.startswith('_'))
    for name in public_props:
        print(name)
    print(outputRes.predicted_state)
    #pp=pprint.PrettyPrinter(depth=6)
    #pp.pprint(outputRes)
    #fig=outputRes.plot_components(legend_loc="lower right",figsize=(15,9))
    fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.cycle["smoothed"], name="cycle"))
    fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.trend["smoothed"], name="trend"))
    fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=outputRes.predicted_state[0], name="predicted"))
    fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=currMeas.pm2p5, name="actual"))

    fig.show()

    break
    #    fig.add_trace(go.Scatter(x=currMeasures.index.get_level_values(1), y=currMeasures.pm2p5, name=locationId))
fig.update_xaxes(
    rangeslider_visible=True,
    tickformatstops=[
        dict(dtickrange=[None, None], value="%a %m-%d"),

    ]
)

#fig.show()

