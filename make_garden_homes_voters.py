# %%
import os
os.chdir('c:/bench/bst')
import pandas as pd

# %%
all_voters = pd.read_csv('c:/bench/reps/michigan/data/voters.csv')

# %%
aa_voters = all_voters[all_voters.city=='ANN ARBOR']

# %%
nhood=pd.read_csv('data/neighborhoods/Garden_Homes.csv')
nhood

# %%
df=pd.DataFrame()
for sname in nhood.name:
    x = aa_voters[aa_voters.street_address.str.contains(sname)]
    df = pd.concat([df, x], axis=0)
len(df)

# %%
import usaddress

# %%
house_number = []
for addr in df.street_address:
    us_addr = usaddress.parse(addr)
    house_number.append(int(us_addr[0][0]))
df.insert(8, 'house_number', house_number)

# %%
def build_street(parts):
    sname = ''
    for t in parts:
        if t[1] in [
            'StreetNamePreDirectional',
            'StreetName',
            'StreetNamePostType',
            'StreetNamePostDirectional'
        ]:
            sname += t[0] + ' '
    return sname.strip()


# %%
street = []
for addr in df.street_address:
    us_addr = usaddress.parse(addr)
    street.append(build_street(us_addr))
df.insert(9, 'street', street)

# %%
x=df.drop(df[(df.street=='MILLER AVE') & ((df.house_number<2220) | (df.house_number>2260))].index)

# %%
df = x

# %%
x=df.drop(df[(df.street=='MILLER AVE') & (df.house_number % 2 != 0)].index)
len(x)

# %%
df = x

# %%
x=df.drop(df[(df.street=='N MAPLE RD') & ((df.house_number<1652) | (df.house_number>1860))].index)

# %%
df=x

# %%
x=df.drop(df[(df.street=='N MAPLE RD') & (df.house_number % 2 != 0)].index)
len(x)

# %%
df=x
df.head()

# %%
pd.unique(df.street)

# %%
df.to_csv('c:/bench/bst/data/neighborhoods/Garden_Homes_voters.csv', header=True, index=False)

# %%



