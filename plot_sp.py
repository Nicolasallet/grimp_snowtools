import numpy as np
import pandas as pd
import glob as glob 
import os
import matplotlib.pyplot as plt
import scipy.stats as stats




def set_height_as_index(df_density):
    if df_density.columns[0] == 'Height (cm)' :
        df_density.index = df_density.iloc[:,0]
    elif df_density.columns[0] == 'Htop (cm)' :
        index = []
        for i in range(df_density.shape[0]-1):
            index.append((df_density.iloc[i,0]+df_density.iloc[i+1,0])/2)
        index.append((df_density.iloc[df_density.shape[0]-1,0])/2)
        df_density.index=index
    else :
        df_density.index = (df_density.iloc[:,0]+df_density.iloc[:,1])/2


def all_data(fold_of_snowpit):

    ### Plot all available data ####

    
    #### read data ###
    df_strati = pd.read_csv(os.path.join(fold_of_snowpit,'stratigraphy','sp.csv'))
    df_density = pd.read_csv(os.path.join(fold_of_snowpit,'density','sp.csv'))
    df_ssa = pd.read_csv(os.path.join(fold_of_snowpit,'iris','sp.csv'))
    df_temp = pd.read_csv(os.path.join(fold_of_snowpit,'temp','sp.csv'))
    set_height_as_index(df_density)
    
    th_tot = max(max(df_strati.iloc[:,0]),max(df_ssa.iloc[:,0]),max(df_density.iloc[:,0]))
    #z = np.linspace(0,int(th_tot),2*int(th_tot)+1)
    fig, ax = plt.subplots()
    
    ### Plot density data ###
    ax.scatter(df_density.iloc[:,-1],df_density.index,marker = '|',s = 100)
    ax.set_xlabel('density kg m$^{-3}$', color='b')
    for tl in ax.get_xticklabels():
        tl.set_color('b')
       
    ### Plot ssa data ###
    ax2 = ax.twiny()
    ax2.scatter(df_ssa.iloc[:,-2],df_ssa.iloc[:,0],marker = '+',color = 'r',s = 100)
    ax2.set_xlabel('SSA m kg $^{-1}$', color='r')
    for tl in ax2.get_xticklabels():
        tl.set_color('r')
        
    ### Plot temp data ###
    ax3 = ax.twiny()
    ax3.scatter(df_temp.iloc[:,-1],df_temp.iloc[:,0],marker = 'x',color = 'g',s = 50)
    ax3.set_xlabel('Temperature (°C)', color='g')
    
    ax3.spines.top.set_position(("axes", 1.2))
    
    for tl in ax3.get_xticklabels():
        tl.set_color('g')
    
    ax.set_ylabel('Depth (cm)')
    
    #### Plot stratugraphy and snow type###
    xmin = ax.get_xticks()[0]
    xmax = ax.get_xticks()[-1]
    for i in range(len(df_strati.iloc[:,0])):
        htop = df_strati.iloc[i,0]
        hbot = df_strati.iloc[i,1]
        graintype = df_strati.iloc[i,-1]
        ax.hlines(htop,xmin = xmin, xmax = xmax, color = 'black' )
        ax.text(xmax,(htop+hbot)/2,graintype)
    
    ax.set_ylim(0,th_tot+1)
    plt.show()
