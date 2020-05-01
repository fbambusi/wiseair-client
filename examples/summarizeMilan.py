import plotly.graph_objects as go
import pandas as pd
import numpy as np
# os.chdir("..")
from wiseair.WiseairClient import WiseairUtils
import statsmodels.api as sm


measures = pd.read_csv("examples/measures.csv")

wu=WiseairUtils()
measures=wu.getPandasDataFrameFromDataOfSingleSensor(measures)
summary=wu.getSummaryOfPeriod(measures,beginningDate="2020-02-01T00:00:00",endDate="2020-02-28T23:59:59")
report={}
report["feb"]=summary
summary=wu.getSummaryOfPeriod(measures,beginningDate="2020-03-01T00:00:00",endDate="2020-03-31T23:59:59")
report["mar"]=summary
print(report)