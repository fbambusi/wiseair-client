from wiseair.IdoClient import IdoClient


app_client_id="YOUR_CLIENT_ID"
app_client_secret="YOUR_CLIENT_SECRET"
api_key="YOUR_API_KEY"

stage="YOUR_STAGE" #"stage" or "prod"

ic=IdoClient(app_client_id=app_client_id,
             app_client_secret=app_client_secret,
             api_key=api_key,
             stage=stage,
             desired_resources=["measures"])

resp=ic.query_resource(resource_name="measures",query_parameters={"sensor_id":"/sensors/*",
                                                                  "start_datetime":"2021-01-01T10:00:00Z",
                                                                  "end_datetime":"2021-01-01T13:00:00Z"})

print(resp)

