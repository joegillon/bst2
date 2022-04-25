import pandas as pd


elections = pd.read_csv('data/my_elections.csv')
hx = pd.read_csv('data/mi/hx.csv')

hx_eids = list(hx.election_id)
dates = []
for eid in hx_eids:
    erec = elections[elections.id==eid]
    if erec.empty:
        continue
    pass
