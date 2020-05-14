from wiseair.WiseairClient import WiseairClient

wc=WiseairClient()

details_of_pot=wc.get_pot_details(11)
print(details_of_pot)

details_of_pot=wc.update_pot_sleeping_time(11,901,23,1)