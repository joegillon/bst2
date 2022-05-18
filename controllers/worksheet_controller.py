import os
import csv
import globals as gbl
import lib.grf_lib as gfl
import lib.addr_lib as adl
import lib.date_lib as dtl
from models.neighborhood import Neighborhood
from models.election import Election
from models.neighborhood_street import NeighborhoodStreet


def get_nhoods():
    return gbl.dataset.my_neighborhoods


def show_grf(choice, nhood):
    if choice == 'All Voters':
        gdf = gfl.all_gdf(nhood)
    elif choice == 'Gender':
        gdf = gfl.gender_gdf(nhood)
    elif choice == 'Age Group':
        gdf = gfl.age_gdf(nhood)
    else:
        gdf = gfl.party_gdf(nhood)

    draw(gdf)


def draw(df):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylabel('Voters', fontsize=10)
    ax.set_xlabel('Elections', fontsize=10)
    df.T.plot(ax=ax, kind='bar', stacked=False)
    plt.show()
