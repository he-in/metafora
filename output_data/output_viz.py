# import necessary libraries
import matplotlib.patches
import pandas as pd
import seaborn as sns
import colorcet as cc
import matplotlib.pyplot as plt

# create DataFrame
df = pd.read_csv("demographics06-26-2023.csv")
df = df.loc[(df['pop_type'] =='ASY') | (df['pop_type']=='REF') | (df['pop_type']=='IDP')]

df_cut = df.groupby(['year', 'coo'])['total'].sum().reset_index()
df_cut = df_cut.drop(df_cut[df_cut['coo'] == "UKN"].index)
df_cut = df_cut.drop(df_cut[df_cut['coo'] == "STA"].index)
year_range = range(2010, 2020)
top_n = 10
df_year = df_cut[df_cut['year'] == 2010].nlargest(top_n, 'total')
for i in year_range[:-1]:
    df_year = pd.concat([df_year, df_cut[df_cut['year'] == i + 1].nlargest(top_n, 'total')], ignore_index=True)

applied_dict = {}
# test = df_year.loc[df_year['coo']=='ZIM'].loc[df_year['year']==2010]['applied'].item()
for coo_i in df_year['coo'].unique():
    applied_list = list()
    for i in year_range:
        if i in df_year.loc[df_year['coo'] == coo_i]['year'].values:
            applied_list.append(df_year.loc[df_year['coo'] == coo_i].loc[df_year['year'] == i]['total'].item())
        else:
            applied_list.append(0)
    applied_dict = applied_dict | {coo_i: applied_list}
df_transposed = pd.DataFrame(applied_dict, index=year_range)
#
# for i in year_range:
# 	for coo_i in df_year['applied'].unique():
# 		dictionary = {coo_i:
# 		df_transposed=pd.concat(df_transposed,df_year[])
sns.set(style="darkgrid")

_, ax = plt.subplots(figsize=(15, 30))
# ax = df_transposed.plot(kind='bar', stacked=True, ax=ax, color=sns.color_palette(cc.glasbey, n_colors=25))
ax = df_transposed.plot(kind='bar', stacked=True, ax=ax, color=sns.color_palette("Spectral", n_colors=top_n + 7),
                        edgecolor='k')

x_labels = year_range
ax.set_xlabel('Year', size=12)
ax.set_xticklabels(x_labels)

y_labels = [0, 10, 20, 30, 40, 50, 60]
ax.set_ylabel('Number of forcibly displaced people [in millions]', size=12)
ax.set_yticklabels(y_labels)
# plt.setp(ax.xaxis.get_majorticklabels(), rotation=70)
plt.title('Number of forcibly displaced people per country of origin')
ax.legend(labels=df_year['coo'].unique())

for bar in ax.containers:
    label_bars = [bar._label if i > 0 else "" for i in bar.datavalues]
    ax.bar_label(bar, labels=label_bars, label_type='center', size=8)

ax.spines['bottom'].set_color('0.5')
ax.spines['top'].set_color('0.5')
ax.spines['right'].set_color('0.5')
ax.spines['left'].set_color('0.5')


plt.show()

fig = ax.figure.savefig('top10_demographics.png', dpi=300,bbox_inches='tight')
