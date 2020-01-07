# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 12:28:47 2019

@author: Lab-722
"""
import time
import pandas as pd
import numpy as np
from pathlib import Path

# Manual path
dataset_name = "USA_Bankrupt"
directory_path = r"C:\Users\Lab-722\Desktop\ReadyForCombine\20190104\USA_Bankrupt"


# Load File Path for combine
xlsxpath = []
for filename in Path(directory_path).rglob('*.xlsx'):
    xlsxpath.append(filename)

# Load data 
## Ex. JPN-Adaboost
full_dataset_result = pd.DataFrame()
for result_path in xlsxpath:
    
    # Add Function Name & Rename Unnamed Column   
    dataSource = pd.read_excel(directory_path+"\\"+result_path.name)
    dataSource.rename( columns={'Unnamed: 0':'Discretize Method'}, inplace=True )
    function_name = result_path.name.split('_')[-2]
    dataSource.insert(0, 'Classifier', str(function_name))
    coloumn_names = ['Accuracy','AUC','TypeI','TypeII']
    for i in range(0,len(coloumn_names)):
        gap_baseline_dataframe = pd.DataFrame(columns=[coloumn_names[i]+' Gap',coloumn_names[i]+' Gap > 5%'])
        for idx,value in enumerate(dataSource[coloumn_names[i]]):
            gap_baseline = value -dataSource[coloumn_names[i]][0]
            if coloumn_names[i] =='TypeI' or coloumn_names[i] =='TypeII':
                gap_baseline = -gap_baseline
            gap_baseline_bigger_than_5_percent = ""
            if gap_baseline>=0.05:
                gap_baseline_bigger_than_5_percent = "Positive"
            elif gap_baseline<=-0.05:
                gap_baseline_bigger_than_5_percent = "Negative"
            gap_baseline_dataframe = gap_baseline_dataframe.append(
                    {coloumn_names[i]+' Gap': gap_baseline, coloumn_names[i]+' Gap > 5%': gap_baseline_bigger_than_5_percent}, ignore_index=True)
            #dfObj.append()
        dataSource = pd.concat([dataSource,gap_baseline_dataframe], axis=1)
    
    # Adjust Coloumn Position    
    new_order = ['Classifier', 'Discretize Method', 'Accuracy', 'Accuracy Gap', 'Accuracy Gap > 5%', 'AUC','AUC Gap', 'AUC Gap > 5%', 'TypeI','TypeI Gap', 'TypeI Gap > 5%', 'TypeII',   'TypeII Gap', 'TypeII Gap > 5%', 'Time(Second)']
    dataSource = dataSource[new_order]
    full_dataset_result = full_dataset_result.append(dataSource)

full_dataset_result.reset_index()
#dataSource["Accuracy"][0]
#dataSource.insert(0, 'Classifier', )
# Add Column(Function Name & Difference to Baseline & Baseline>5% )

file_time = time.strftime("%Y-%m-%d-%H%M%S", time.localtime()) 
file_name = "CombineResult_{dataset_name}_{file_timeA}.xlsx".format(
        file_timeA = file_time,dataset_name=dataset_name)
pd.DataFrame(full_dataset_result).to_excel("CombineResult/"+file_name)

#dataSource[""]

    
# Add Function Name to each data (first column)
## Ex.  

print(xlsxpath[0].name.split('_')[-2]) 
#dataSource = pd.read_excel(r'C:\Users\Lab-722\Documents\GitHub\Discretize_Classification\resultsexcel\Classifier_result_list_5Fold_Japanese_Bankrupt_mlp_2019-12-28-222232.xlsx')
#print (dataSource)