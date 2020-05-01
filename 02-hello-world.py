#!/usr/bin/env python
# coding: utf-8

# How to use: create a client, specifying the path to the file where credentials are stored.
# Example of file:
# 
# "client_id","client_secret","user_email","user_password"
# CLIENT_ID_HERE,CLIENT_SECRET_HERE,YOUR_PERSONAL_EMAIL_HERE,YOUR_PERSONAL_PASSWORD_HERE
# 

# In[1]:


from WiseairClient.WiseairClient import WiseairClient
client=WiseairClient()


# In[2]:


currentMeasures=client.getLiveAirQuality()


# In[3]:


potId=currentMeasures["data"][0]["pot_id"]
#13
BEGIN_DATE,END_DATE="2020-02-15","2020-03-11"
data=client.getDataOfPotByInterval(potId,BEGIN_DATE,END_DATE)


# In[4]:


from WiseairClient.WiseairClient import WiseairUtils


# In[5]:


utils=WiseairUtils()
data=utils.getPandasDataFrameFromDataOfSingleSensor(data)

data.to_csv("sampleData.csv")

