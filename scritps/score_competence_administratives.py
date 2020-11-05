#!/usr/bin/env python
# coding: utf-8

# ## Compétences Compétences administratives

# ### 1- POUR LES COMMUNES

# In[1]:


import pandas as pd 
import numpy as np
file = r'xls/base-ic-evol-struct-pop-2016.xls'
file2 = r'xls/TCRD_087.xls'
file3 = r'xls/base-cc-filosofi-2016.xls'


# In[2]:


df = pd.read_excel(file,header=5)


# In[4]:


df2 = pd.read_excel(file2,'DEP',header=3)


# In[5]:


df3 = pd.read_excel(file3,'DEP',header=5)


# In[17]:


newdf = pd.DataFrame() 

#Grouper les communes
groupe1 = (df.groupby(['DEP','COM']).sum())[['P16_POP','P16_POP1529']]
groupe1 = groupe1.reset_index()



groupe2 = df2[['DEP','Ensemble']]

#part_chomeurs(%)
newdf=pd.merge(groupe1,groupe2)

newdf.columns=['DEP','COM','P16_POP','P16_POP1529','part_chomeurs%']

print(newdf)

#part des minima sociaux (%)
groupe3 = df3[['CODGEO','PPMINI16']]
groupe3.columns = ['DEP','minima%']
newdf=pd.merge(newdf,groupe3,how='left')




print(newdf)


# In[18]:


NcRegDep = df[['DEP','REG','COM','LIBCOM']]
newdf = pd.merge(NcRegDep,newdf)
newdf = newdf.drop_duplicates()
newdf


# In[19]:


#Part des personnes âgées de 15 et 29 ans %
newdf['P16_POP1529%'] = newdf['P16_POP1529']*100/newdf['P16_POP']

print(newdf)


# In[20]:


moyReg = (newdf.groupby(['REG']).sum())[['P16_POP','P16_POP1529']]
moyReg = moyReg.reset_index()

moyReg['REG_P16_POP1529%'] = moyReg['P16_POP1529']*100/moyReg['P16_POP']

moyReg['REG_part_chomeurs%'] = (newdf.groupby(['REG']).mean())[['part_chomeurs%']]
moyReg['REG_minima%'] = (newdf.groupby(['REG']).mean())[['minima%']]
moyReg['REG_part_chomeurs%'] = moyReg['REG_part_chomeurs%'].fillna(0)
moyReg['REG_minima%'] = moyReg['REG_minima%'].fillna(0)

print(moyReg[['REG','REG_P16_POP1529%','REG_part_chomeurs%','REG_minima%']])


# In[21]:


newdf1 = newdf[['REG','LIBCOM','P16_POP1529%','part_chomeurs%','minima%']]
moyReg = moyReg[['REG','REG_P16_POP1529%','REG_part_chomeurs%','REG_minima%']]

newdf1 = pd.merge(newdf1,moyReg)
newdf1


# In[22]:


newdf1['pointsPOP1529'] =  ((newdf1['P16_POP1529%'] - newdf1['REG_P16_POP1529%'])/newdf1['REG_P16_POP1529%'] + 1) *100
newdf1['pointspart_chomeurs'] =  ((newdf1['part_chomeurs%'] - newdf1['REG_part_chomeurs%'])/newdf1['REG_part_chomeurs%'] + 1) *100
newdf1['pointsMinima'] =  ((newdf1['minima%'] - newdf1['REG_minima%'])/newdf1['REG_minima%'] + 1) *100
newdf1['pointspart_chomeurs'].replace(np.inf, 0, inplace=True)
newdf1['pointsMinima'].replace(np.inf, 0, inplace=True)
newdf1


# In[23]:


newdf1['score_competence_administratives_region'] = (newdf1['pointsPOP1529'] + newdf1['pointspart_chomeurs'] + newdf1['pointsMinima'])*100/(2*100)
newdf1 = newdf1[['REG','LIBCOM','score_competence_administratives_region']]
newdf1


# ### Point de reference DEP

# In[24]:


moyDep = (newdf.groupby(['DEP']).sum())[['P16_POP','P16_POP1529']]
moyDep = moyDep.reset_index()

moyDep['DEP_P16_POP1529%'] = moyDep['P16_POP1529']*100/moyDep['P16_POP']

moyDep['DEP_part_chomeurs%'] = (newdf.groupby(['DEP']).mean())[['part_chomeurs%']]
moyDep['DEP_minima%'] = (newdf.groupby(['DEP']).mean())[['minima%']]
moyDep['DEP_part_chomeurs%'] = moyDep['DEP_part_chomeurs%'].fillna(0)
moyDep['DEP_minima%'] = moyDep['DEP_minima%'].fillna(0)


print(moyDep[['DEP','DEP_P16_POP1529%','DEP_part_chomeurs%','DEP_minima%']])


# In[25]:


newdf2 = newdf[['DEP','LIBCOM','P16_POP1529%','part_chomeurs%','minima%']]

newdf2 = pd.merge(newdf2,moyDep)
newdf2


# In[26]:


newdf2['pointsPOP1529'] =  ((newdf2['P16_POP1529%'] - newdf2['DEP_P16_POP1529%'])/newdf2['DEP_P16_POP1529%'] + 1) *100



newdf2['pointspart_chomeurs'] =  ((newdf2['part_chomeurs%'] - newdf2['DEP_part_chomeurs%'])/newdf2['DEP_part_chomeurs%'] + 1) *100
newdf2['pointsMinima'] =  ((newdf2['minima%'] - newdf2['DEP_minima%'])/newdf2['DEP_minima%'] + 1) *100
newdf2['pointspart_chomeurs'].replace(np.inf, 0, inplace=True)
newdf2['pointsMinima'].replace(np.inf, 0, inplace=True)
newdf2


# In[28]:


newdf1['score_competence_administratives_departement'] = ((newdf2['pointsPOP1529'] + newdf2['pointspart_chomeurs'] + newdf2['pointsMinima'])*100)/(2*100)
newdf1['DEP'] = newdf2['DEP']
newdf1


# In[29]:


newdf1 = newdf1[['DEP','REG','LIBCOM','score_competence_administratives_region','score_competence_administratives_departement']]
newdf1


# In[30]:


sortie = newdf1.round(0)
sortie


# In[32]:


sortie.to_csv(r'score_competence_administratives_communes.csv', encoding='iso-8859-1', sep=';')


# In[33]:


newdf1[newdf1['LIBCOM']=='Toulouse']


# In[ ]:




