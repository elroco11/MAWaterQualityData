import urllib.request
import ast
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
    
def getData(chem,town):
    op=open("MAWaterQuality_{}.csv".format(town),'w',newline='')
    opf=csv.writer(op)
    
    opener = AppURLopener()
    #response=opener.open("http://eeaonline.eea.state.ma.us/EEA/DataLake/V1.0/DataLakeAPI/drinkingWater/export-to/excel?ChemicalName={}&Town={}".format(chem.replace(" ","+").upper(),town.upper()))
    url="https://eeaonline.eea.state.ma.us/EEA/DataLake/V1.0/DataLakeAPI/drinkingWater?ChemicalName={}&Town={}&_end=10000&_start=0".format(chem.replace(" ","+").upper(),town.upper())
    r=opener.open(url)
    data=r.read().decode("UTF-8")
    d=ast.literal_eval(data).get("Items")

    fieldnames=d[0].keys()
    opf.writerow(fieldnames)

    x=[]
    y=[]

    for i in range(len(d)):
        ls=[d[i].get(key) for key in d[i]]
        opf.writerow(ls)
    for i in range(len(d)):
        if d[i].get("LocationName")=="ENGINE #3":
            x.append(d[i].get("CollectedDate"))
            y.append(d[i].get("Result"))
   
    xpoints=np.array(x)
    ypoints=np.array(y)
    #xpoints=np.array([1,2,3])
    #ypoints=np.array([4,5,6])
    plt.scatter(xpoints,ypoints)
    plt.show(block=True)

    op.close()
getData("TOTAL TRIHALOMETHANES","CAMBRIDGE")
