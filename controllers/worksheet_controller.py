import os
import csv
import globals as gbl
import lib.grf_lib as gfl
import lib.addr_lib as adl
import lib.date_lib as dtl
from models.voter import Voter
from models.neighborhood import Neighborhood
from models.election import Election
from models.neighborhood_street import NeighborhoodStreet


def init_view(view):
    view.voter_panel.Hide()
    view.load_nhood_list(gbl.dataset.my_neighborhoods)
    view.nhood_select(0)


def show_turnout_grf(choice, nhood):
    if choice == 'All Voters':
        gdf = gfl.turnout_all_gdf(nhood)
    elif choice == 'Gender':
        gdf = gfl.turnout_gender_gdf(nhood)
    elif choice == 'Age Group':
        gdf = gfl.turnout_age_gdf(nhood)
    else:
        gdf = gfl.turnout_party_gdf(nhood)

    draw(gdf)


def show_makeup_grf(choice, nhood):
    if choice == 'Score':
        gdf = gfl.makeup_score_gdf(nhood)
    elif choice == 'Gender':
        gdf = gfl.makeup_gender_gdf(nhood)
    elif choice == 'Age Group':
        gdf = gfl.makeup_age_gdf(nhood)
    else:
        gdf = gfl.makeup_party_gdf(nhood)


def draw(df):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylabel('Voters', fontsize=10)
    ax.set_xlabel('Elections', fontsize=10)
    df.T.plot(ax=ax, kind='bar', stacked=False)
    plt.show()
