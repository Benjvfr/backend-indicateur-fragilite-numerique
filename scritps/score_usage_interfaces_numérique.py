#!/usr/bin/env python
# coding: utf-8

# ## Capacité d’usage des interfaces numériques

# In[8]:


import pandas as pd 

file = r'xls/base-ic-evol-struct-pop-2016.xls'
file2 = r'xls/base-ic-diplomes-formation-2016.xls'


# In[10]:


df = pd.read_excel(file,header=5)
df2 = pd.read_excel(file2,header=5)


# In[245]:


newdf = pd.DataFrame() 

newdf['REG']  =  df['REG']
newdf['DEP']  =  df['DEP']
newdf['nom_commune']  =  df['LIBCOM']
newdf['nom_iris']  =  df['LIBIRIS']
newdf['POP'] = df['P16_POP']
newdf['POP65P'] = df['P16_POP65P']
newdf['NSCOL15P_DIPLMIN'] = df2['P16_NSCOL15P_DIPLMIN']


poTotal = df['P16_POP']
#Part des personnes âgées de 65 ans / +
newdf['POP65P%'] = df['P16_POP65P']*100/poTotal

#Part de la population de 15/+ sans diplôme
newdf['NSCOL15P_DIPLMIN%'] = df2['P16_NSCOL15P_DIPLMIN']*100/poTotal

print(newdf)


# In[265]:


moyReg = (newdf.groupby(['REG']).sum())[['POP','POP65P','NSCOL15P_DIPLMIN']]
moyReg = moyReg.reset_index()

moyReg['REG_POP65P%'] = moyReg['POP65P']*100/moyReg['POP']
moyReg['REG_NSCOL15P_DIPLMIN%'] = moyReg['NSCOL15P_DIPLMIN']*100/moyReg['POP']

print(moyReg[['REG','REG_POP65P%','REG_NSCOL15P_DIPLMIN%']])


# In[267]:


newdf1 = newdf[['REG','nom_commune','nom_iris','POP65P%','NSCOL15P_DIPLMIN%']]
moyReg = moyReg[['REG','REG_POP65P%','REG_NSCOL15P_DIPLMIN%']]

newdf1 = pd.merge(newdf1,moyReg)
newdf1


# In[268]:


newdf1['pointsPOP65P'] =  ((newdf1['POP65P%'] - newdf1['REG_POP65P%'])/newdf1['REG_POP65P%'] + 1) *100
newdf1['pointsNSCOL15P_DIPLMIN'] =  ((newdf1['NSCOL15P_DIPLMIN%'] - newdf1['REG_NSCOL15P_DIPLMIN%'])/newdf1['REG_NSCOL15P_DIPLMIN%'] + 1) *100
newdf1


# In[269]:


newdf1['score_acces_interface_numerique_region'] = (newdf1['pointsPOP65P'] + newdf1['pointsNSCOL15P_DIPLMIN'])*100/(2*100)
newdf1 = newdf1[['REG','nom_commune','nom_iris','score_acces_interface_numerique_region']]
newdf1


# In[273]:


moyDep = (newdf.groupby(['DEP']).sum())[['POP','POP65P','NSCOL15P_DIPLMIN']]
moyDep = moyDep.reset_index()

moyDep['DEP_POP65P%'] = moyDep['POP65P']*100/moyDep['POP']
moyDep['DEP_NSCOL15P_DIPLMIN%'] = moyDep['NSCOL15P_DIPLMIN']*100/moyDep['POP']

moyDep[['DEP','DEP_POP65P%','DEP_NSCOL15P_DIPLMIN%']]


# In[274]:


newdf2 = newdf[['DEP','REG','nom_commune','nom_iris','POP65P%','NSCOL15P_DIPLMIN%']]
moyDep = moyDep[['DEP','DEP_POP65P%','DEP_NSCOL15P_DIPLMIN%']]

newdf2 = pd.merge(newdf2,moyDep)
newdf2


# In[275]:


newdf2['pointsPOP65P'] =  ((newdf2['POP65P%'] - newdf2['DEP_POP65P%'])/newdf2['DEP_POP65P%'] + 1) *100
newdf2['pointsNSCOL15P_DIPLMIN'] =  ((newdf2['NSCOL15P_DIPLMIN%'] - newdf2['DEP_NSCOL15P_DIPLMIN%'])/newdf2['DEP_NSCOL15P_DIPLMIN%'] + 1) *100
newdf2


# In[276]:


newdf1['score_acces_interface_numerique_departement'] = ((newdf2['pointsPOP65P'] + newdf2['pointsNSCOL15P_DIPLMIN'])*100)/(2*100)
newdf1['DEP'] = newdf2['DEP']
newdf1


# In[277]:


newdf1 = newdf1[['DEP','REG','nom_commune','nom_iris','score_acces_interface_numerique_region','score_acces_interface_numerique_departement']]
newdf1


# In[278]:


sortie = newdf1.round(0)
sortie


# In[263]:


#sortie.to_excel(r'CapUsaIntNum.csv', index = False)
sortie.to_csv(r'xls/CapUsaIntNum.csv', sep=';')


