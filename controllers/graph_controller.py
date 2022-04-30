import lib.grf_lib as gfl


def show_grf_click(self, evt):
    nhood = self.view.get_current_nhood()
    grf = self.view.get_grf_selections()
    choice = grf[0].name
    if choice == 'All Voters':
        gdf = gfl.all_gdf(nhood)
    elif choice == 'Gender':
        gdf = gfl.gender_gdf(nhood)
    elif choice == 'Age Group':
        gdf = gfl.age_gdf(nhood)
    else:
        gdf = gfl.party_gdf(nhood)

    self.draw(gdf)


def draw(self, df):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylabel('Voters', fontsize=10)
    ax.set_xlabel('Elections', fontsize=10)
    df.T.plot(ax=ax, kind='bar', stacked=False)
    plt.show()
