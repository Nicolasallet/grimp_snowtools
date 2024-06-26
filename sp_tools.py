import numpy as np
import pandas as pd
import glob as glob 
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

def get_coord(fold_of_snowpit):
    df_info = pd.read_csv(os.path.join(fold_of_snowpit,'site','sp.csv'))
    lat = df_info['Latitude (° N)'].iloc[0]
    lon = df_info['Longitude (° E)'].iloc[0]
    return(lat,lon)

    
def unwrapSnowpit(fold_of_snowpit) :
### Cette fonction lit les données de snowpits dans 'fold' et renvoie 4 array avec les données de respecivement : Epaisseur, densité, ssa et température des couches.
### Les couches sont déterminée selon la stratigraphie et l'existence ou non de mesure dans la couche.

    
    df_strati = pd.read_csv(os.path.join(fold_of_snowpit,'stratigraphy','sp.csv'))
    df_density = pd.read_csv(os.path.join(fold_of_snowpit,'density','sp.csv'))
    df_ssa = pd.read_csv(os.path.join(fold_of_snowpit,'iris','sp.csv'))
    df_temp =  pd.read_csv(os.path.join(fold_of_snowpit,'temp','sp.csv'))
    
    n_layer = df_strati.shape[0]                                                #Get the numbers of layers
    layer_thickness = np.asarray(df_strati.iloc[:,-2])                          #Get the Thickness of each layer in cm
    
    # Création of output array
    layer_density = np.zeros((n_layer))
    layer_ssa = np.zeros((n_layer))
    layer_temp = np.zeros((n_layer))
    
    if df_density.columns[0] == 'Height (cm)' :                                               #set height as index for groupby operation
        df_density.index = df_density.iloc[:,0]
    elif df_density.columns[0] == 'Htop (cm)' :
        index = []
        for i in range(df_density.shape[0]-1):
            index.append((df_density.iloc[i,0]+df_density.iloc[i+1,0])/2)
        index.append((df_density.iloc[df_density.shape[0]-1,0])/2)
        df_density.index=index
    else :
        df_density.index = (df_density.iloc[:,0]+df_density.iloc[:,1])/2
        
    df_ssa.index = df_ssa.iloc[:,0]                                                            #set height as index for groupby operation
    df_temp.index = df_temp.iloc[:,0]                                                          #set height as index for groupby operation
    
    i = 0
    j = 0
    while i < (n_layer) :
    
        # on définit les limites de la couches considérée. +1 pour que les valeurs prisent aux interface superieurs soient dans la couche (arbitraire)
        layertop = df_strati.iloc[j,0]+1
        layerbot = df_strati.iloc[j,1]+1
    
        #Créé des df de deux lignes, la ligne "true" est la moyenne des valeurs satisfaiant les condition ds groupby si ces valeurs existent
        
        ssa = df_ssa.groupby(by = (df_ssa.index <= layertop) & (df_ssa.index > layerbot)).mean()                                
        dens = df_density.groupby(by = (df_density.index <= layertop) & (df_density.index > layerbot)).mean()
        temp = df_temp.groupby(by = (df_temp.index <= layertop) & (df_temp.index > layerbot)).mean()
    
        #Si aucune valeur de densité ou de ssa ou de température n'existe entre layertop et layerbottom : 
            # - L'epaisseur de la couche suivante (dessous) est ajoutée a la couche considérée
            # - On recommemce le processus avec une couche constituée de la couche i et i+1
        
        if ssa.index[-1] != True or dens.index[-1] != True or temp.index[-1] != True:           
            n_layer -= 1 
            if i < n_layer :
                layer_thickness[i] = layer_thickness[i]+layer_thickness[i+1]
                layer_thickness = np.delete(layer_thickness,i+1)
            else :                                                                   # Si c'est la dernière couche : on merge avec la couche du dessus
                layer_thickness[i-1] = layer_thickness[i]+layer_thickness[i-1]
                layer_thickness = np.delete(layer_thickness,i)
    
            # On s'assure que les df de sortis aient la bonne taille, et soient consistant avec le df Layer_thickness
            layer_density = np.delete(layer_density,i)
            layer_ssa = np.delete(layer_ssa,i)
            layer_temp = np.delete(layer_temp,i)  
            j += 1      # Ainsi layerbot passe a la couche du dessus mais layertop rest le mm
    
         # Si on a tt les valeurs (SSA, density, température) : 
            # On sauve les moyenne des variables a l'interieure de la couche dans les array de sortie
        else :
            layer_ssa[i] = ssa.loc[True].iloc[-2]                             #-2 car -1 c'est la colonne Ropt
            layer_density[i] = dens.loc[True].iloc[-1]
            layer_temp[i] = temp.loc[True].iloc[-1]
            i += 1 
            j += 1 
    

    return(layer_thickness,layer_density,layer_ssa,layer_temp)


def unwrap_tsoil(fold_of_snowpit): 

    df_info = pd.read_csv(os.path.join(fold_of_snowpit,'site','sp.csv'))
    df_temp = pd.read_csv(os.path.join(fold_of_snowpit,'temp','sp.csv')).dropna()

    if np.isnan(df_info['Soil temperature (°C)'][0]) == True :
        t_soil = stats.linregress(df_temp['Height (cm)'][-3:],df_temp['Temperature (°C)'][-3:])[1]
    else :
        t_soil = df_info['Soil temperature (°C)'][0]

    return(t_soil)

