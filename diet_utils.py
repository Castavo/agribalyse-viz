"""
Manipulating diets
Let's say a diet is just a dict like :
{ CIQUAL code (= food id) : weight (in kilograms ?) }
And each line would be how much of the food chosen you eat per year (?)
"""
from collections import defaultdict
import numpy as np
import pandas as pd
import requests


def load_agribalyse():
    synthese_url = "https://drive.google.com/uc?export=download&id=1FLyHBVgPsOeChEvDhd_KZCVr9wEFh5Az"
    detail_url = "https://drive.google.com/uc?export=download&id=1YlFMYUdDXbivkoOnrRGsolQq84zp-Rk3"
    agb_synthese =  pd.read_csv(synthese_url, delimiter=",", decimal=",")
    agb_detail = requests.get(detail_url).json()
    multi_index = pd.MultiIndex.from_product(
        [
            agb_detail[0]["impact_environnemental"].keys(), 
            agb_detail[0]["impact_environnemental"]["Score unique EF"]["etapes"].keys()], 
        names=['Impact type', 'Life cycle step'])
    life_cycle_detail = pd.DataFrame(
        data=[
            sum((list(val["etapes"].values()) for val in alim["impact_environnemental"].values()), start=[])
            for alim in agb_detail
        ], 
        columns=multi_index
    )
    return agb_synthese, life_cycle_detail


agribalyse, life_cycle_detail = load_agribalyse()
agribalyse = agribalyse.copy(deep=True)

Food_group_list = ['Fruits, vegetables, legumes and oilseeds', 'Meat, eggs, fish','Cereal products','Milk and dairy products']
agribalyse.loc[~agribalyse["Food Group"].isin(Food_group_list),"Food Group"] = "Other"

def random_diet(food_codes, mean_weight=10, std_dev_weight=5, n_foods=100, seed=42):
    """Returns a random diet"""
    random = np.random.default_rng(seed)
    chosen_foods = random.choice(food_codes, n_foods, replace=False)
    food_weights = random.normal(loc=mean_weight, scale=std_dev_weight, size=n_foods)
    return defaultdict(float, zip(chosen_foods, food_weights))

diet_list = ["Veggie", "Vegan", "Flexie", "Carnist with beef","Carnist with pork", "Pesci"]

brocoli = 20006
carotte = 20008
pomme = 13620
raisin = 13112
raclette = 12749
oeuf_dur = 22010
jus_orange = 2013
céréale = 32025
lentille = 20587
tofu = 20904
poulet = 36018
steak = 6253
saumon = 26038
pâte = 9811
riz = 9104
porc = 30701
dic_chosen_foods = {
    "Veggie":[brocoli,carotte,pomme,raisin,raclette,oeuf_dur,jus_orange,céréale,riz,pâte],
    "Vegan":[brocoli,carotte,pomme,raisin,lentille,tofu,jus_orange,céréale,riz,pâte],
    "Flexie":[brocoli,carotte,pomme,raisin,raclette,poulet,jus_orange,céréale,riz,pâte],
    "Carnist with beef":[brocoli,carotte,pomme,raisin,poulet,steak,jus_orange,céréale,riz,pâte],
    "Pesci":[brocoli,carotte,pomme,raisin,raclette,saumon,jus_orange,céréale,riz,pâte],
    "Carnist with pork":[brocoli,carotte,pomme,raisin,poulet,porc,jus_orange,céréale,riz,pâte]
    }
dic_food_weight = {
    "Veggie":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Vegan":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Flexie":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Carnist with beef":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Pesci":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Carnist with pork":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12]
    }

indicator_to_column_name = {
        'CO2':'Climate change (KG CO2 EQ / KG product)',
        'Ozone Layer depletion':'Depletion of the ozone layer (E-06 kg CVC11 Eq / kg product)',
        'Terrestrial Eutrophication':'Terrestrial eutrophication (mol N eq / kg of product)',
        'Land use':'Land use (Pt / kg of product)',
        'water&land acidification':'Terrestiral and freshwater acidification (mol h + eq / kg product)',
        'Particles':'Particles (E-06 Disease Inc, / kg of product)'
        }

def Diet(diet_name):
    '''
        input : diet_name (string)
        output : dictionnary that give for each food (identification by using Ciqual code) a weight (representing weight eaten during a day)
    '''
    chosen_foods = dic_chosen_foods[diet_name]
    food_weights = dic_food_weight[diet_name]
    return defaultdict(float, zip(chosen_foods, food_weights))


def Impact_total(diet_name,indicator):
    '''
        input : diet_name = name of the diet chosen (string), indicator = name of the indicator chosen (string)(indicator list must be coherent with indicators of radar chart)
        output : Total impact of the diet for one day according to the indicator (string)
    '''
    n = 6 # number of indicator
    
    column_name = indicator_to_column_name[indicator]
    chosen_foods = dic_chosen_foods[diet_name]
    food_weight = dic_food_weight[diet_name]
    sum = 0
    for i in range(n):
        sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
    return sum

def Impact(diet_name,indicator,food_group):
    '''
        input : diet_name = name of the diet chosen (string), indicator = name of the indicator chosen (string)(indicator list must be coherent with indicators of radar chart)
        output : Total impact of the diet for one day according to the indicator (string)
    '''
    n = 6 # number of indicator
    
    column_name = indicator_to_column_name[indicator]
    chosen_foods = dic_chosen_foods[diet_name]
    food_weight = dic_food_weight[diet_name]
    sum = 0
    for i in range(n):
        value = agribalyse[(agribalyse['Ciqual Code'] == chosen_foods[i])&(agribalyse['Food Group']==food_group)][column_name].mean()
        if np.isnan(value):
            sum += 0
        else:
            sum += food_weight[i] * value
        if np.isnan(sum):
            sum = 0
    return sum

def Impact_normalised(diet_name,indicator,food_group):

    n = 6 # number of indicator
    
    max_indicator = max([Impact_total(diet,indicator) for diet in diet_list])
    # min_indicator = min([Impact_total(diet,indicator) for diet in diet_list])
    return Impact(diet_name,indicator,food_group)/max_indicator*10