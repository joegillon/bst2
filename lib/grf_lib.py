import os
import pandas as pd
import globals as gbl


def all_gdf(nhood):
    path = '%s/my_data' % gbl.config['app_path']

    edf = pd.read_csv('%s/elections.csv' % path)
    vdf = pd.read_csv('%s/%s_voters.csv' %
                      (path, nhood.name.replace(' ', '_')))

    cols = edf.date[0:15]
    tdf = vdf.loc[:, cols]

    eligible = {}
    voted = {}
    pct = {}
    for col in tdf.columns:
        eligible[col] = 0
        voted[col] = 0
        pct[col] = 0

    for col in tdf.columns:
        cnts = tdf[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        eligible[col] += cnts['N'] + yval
        voted[col] += yval
        pct[col] = round((voted[col] / eligible[col]) * 100)

    return pd.DataFrame([eligible, voted], index=['eligible', 'voted'])


def gender_gdf(nhood):
    path = '%s/my_data' % gbl.config['app_path']

    edf = pd.read_csv('%s/elections.csv' % path)
    vdf = pd.read_csv('%s/%s_voters.csv' %
                      (path, nhood.name.replace(' ', '_')))

    cols = edf.date[0:15]

    mdf = vdf.loc[vdf.gender == 'M', cols]
    fdf = vdf.loc[vdf.gender == 'F', cols]

    eligible_m = {}
    eligible_f = {}
    voted_m = {}
    voted_f = {}
    pct_m = {}
    pct_f = {}
    for col in cols:
        eligible_m[col] = 0
        eligible_f[col] = 0
        voted_m[col] = 0
        voted_f[col] = 0
        pct_m[col] = 0
        pct_f[col] = 0

    for col in cols:
        cnts = mdf[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        eligible_m[col] += cnts['N'] + yval
        voted_m[col] += yval
        pct_m[col] = round((voted_m[col] / eligible_m[col]) * 100)

        cnts = fdf[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        eligible_f[col] += cnts['N'] + yval
        voted_f[col] += yval
        pct_f[col] = round((voted_f[col] / eligible_f[col]) * 100)

    return pd.DataFrame([eligible_m, voted_m, eligible_f, voted_f],
                        index=['Eligible(M)', 'Voted(M)', 'Eligible(F)', 'Voted(F)'])


def age_gdf(nhood):
    path = '%s/my_data' % gbl.config['app_path']

    edf = pd.read_csv('%s/elections.csv' % path)
    vdf = pd.read_csv('%s/%s_voters.csv' %
                      (path, nhood.name.replace(' ', '_')))

    cols = edf.date[0:15]

    dfg1 = vdf.loc[vdf.age_group == '18-29', cols]
    dfg2 = vdf.loc[vdf.age_group == '30-44', cols]
    dfg3 = vdf.loc[vdf.age_group == '45-64', cols]
    dfg4 = vdf.loc[vdf.age_group == '65+', cols]

    eligible1 = {}
    eligible2 = {}
    eligible3 = {}
    eligible4 = {}
    voted1 = {}
    voted2 = {}
    voted3 = {}
    voted4 = {}
    # pct1 = {}
    # pct2 = {}
    # pct3 = {}
    # pct4 = {}
    for col in cols:
        eligible1[col] = 0
        eligible2[col] = 0
        eligible3[col] = 0
        eligible4[col] = 0
        voted1[col] = 0
        voted2[col] = 0
        voted3[col] = 0
        voted4[col] = 0
        # pct1[col] = 0
        # pct2[col] = 0
        # pct3[col] = 0
        # pct4[col] = 0

    for col in cols:
        cnts = dfg1[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible1[col] += nval + yval
        voted1[col] += yval
        # pct1[col] = round((voted1[col] / eligible1[col]) * 100)

        cnts = dfg2[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible2[col] += nval + yval
        voted2[col] += yval
        # pct2[col] = round((voted2[col] / eligible2[col]) * 100)

        cnts = dfg3[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible3[col] += nval + yval
        voted3[col] += yval
        # pct3[col] = round((voted3[col] / eligible3[col]) * 100)

        cnts = dfg4[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible4[col] += nval + yval
        voted4[col] += yval
        # pct4[col] = round((voted4[col] / eligible4[col]) * 100)

    return pd.DataFrame([
        eligible1, voted1,
        eligible2, voted2,
        eligible3, voted3,
        eligible4, voted4
    ], index=[
        'Eligible(18-29)', 'Voted(18-29)',
        'Eligible(30-44)', 'Voted(30-44)',
        'Eligible(45-64)', 'Voted(45-64)',
        'Eligible(65+)', 'Voted(65+)',
    ])


def party_gdf(nhood):
    path = '%s/data/' % os.getcwd()

    edf = pd.read_csv(path + 'mi/elections.csv')
    vdf = pd.read_csv(path + ('voters/%s_voters.csv' % nhood))

    cols = edf.date[0:15]

    ddf = vdf.loc[vdf.party == 'D', cols]
    rdf = vdf.loc[vdf.party == 'R', cols]

    eligible_d = {}
    eligible_r = {}
    voted_d = {}
    voted_r = {}
    pct_d = {}
    pct_r = {}
    for col in cols:
        eligible_d[col] = 0
        eligible_r[col] = 0
        voted_d[col] = 0
        voted_r[col] = 0
        pct_d[col] = 0
        pct_r[col] = 0

    for col in cols:
        cnts = ddf[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible_d[col] += nval + yval
        voted_d[col] += yval
        pct_d[col] = round((voted_d[col] / eligible_d[col]) * 100)

        cnts = rdf[col].value_counts()
        yval = cnts['Y'] if 'Y' in cnts else 0
        nval = cnts['N'] if 'N' in cnts else 0
        eligible_r[col] += nval + yval
        voted_r[col] += yval
        pct_r[col] = round((voted_r[col] / eligible_r[col]) * 100)

    return pd.DataFrame([eligible_d, voted_d, eligible_r, voted_r],
                        index=['Eligible(D)', 'Voted(D)', 'Eligible(R)', 'Voted(R)'])
