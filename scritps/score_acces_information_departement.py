import pandas as pd
import numpy as np

'''
Accès à l'information
'''
file = r'xls/base-ic-couples-familles-menages-2016.xls'

df = pd.read_excel(file, header=5)

newdf = pd.DataFrame()
newdf['DEP'] = df['DEP']
newdf['LIBCOM'] = df['LIBCOM']
newdf['LIBIRIS'] = df['LIBIRIS']
newdf['C16_MENPSEUL'] = df['C16_MENPSEUL']
newdf['C16_FAMMONO'] = df['C16_FAMMONO']

# Part des ménages d’une personne / commune
newdf['Part des ménages d’une personne / commune'] = df['C16_MENPSEUL']*100/df['C16_MEN']

# Part des ménages d’une personne / département
newdf['Part des ménages d’une personne / département'] = np.nan

for i, r in (df.groupby(df['DEP'])['C16_MENPSEUL'].sum()*100/df.groupby(df['DEP'])['C16_MEN'].sum()).to_frame('Moyenne département').iterrows():
    newdf['Part des ménages d’une personne / département'].loc[df['DEP'] == i] = r['Moyenne département']

# Points de la part des ménages d’une personne / commune
newdf['Points de la part des ménages d’une personne / commune'] = (((newdf['Part des ménages d’une personne / commune']-newdf['Part des ménages d’une personne / département'])/newdf['Part des ménages d’une personne / département'])+1)*100

'''
Calcul des points de la part des familles monoparentales / commune
'''
# Part des familles monoparentales / commune
newdf['Part des familles monoparentales / commune'] = df['C16_FAMMONO']*100/df['C16_MEN']

# Part des familles monoparentales / département
newdf['Part des familles monoparentales / département'] = np.nan

for i, r in (df.groupby(df['DEP'])['C16_FAMMONO'].sum()*100/df.groupby(df['DEP'])['C16_MEN'].sum()).to_frame('Moyenne département').iterrows():
    newdf['Part des familles monoparentales / département'].loc[df['DEP'] == i] = r['Moyenne département']

# Points de la part des familles monoparentales / commune
newdf['Points de la part des familles monoparentales / commune'] = (((newdf['Part des familles monoparentales / commune']-newdf['Part des familles monoparentales / département'])/newdf['Part des familles monoparentales / département'])+1)*100

# Somme des points
newdf['Somme des points'] = newdf['Points de la part des ménages d’une personne / commune'] + newdf['Points de la part des familles monoparentales / commune']

# Score de fragilité sur l'accès à l'information
newdf['score_acces_information_département'] = (newdf['Somme des points']*100)/(2*100)

dftoexport = pd.DataFrame()
dftoexport['nom_iris'] = newdf['LIBIRIS']
dftoexport['nom_commune'] = newdf['LIBCOM']
dftoexport['numero_region'] = newdf['DEP']
dftoexport['score_acces_information_département'] = newdf['score_acces_information_département']


dftoexport.to_csv(r'xls/score_acces_information_département.csv', sep=';')
