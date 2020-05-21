from wiseair.WiseairClient import WiseairClient

wc=WiseairClient("../personalAccessToken.csv")

details=wc.get_firmware_test_details_by_id(34)
print(details)