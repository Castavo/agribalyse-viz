"""
Manipulating diets
Let's say a diet is just a dict like :
{ CIQUAL code (= food id) : weight (in kilograms ?) }
And each line would be how much of the food chosen you eat per year (?)
"""
from collections import defaultdict
import numpy as np
import pandas as pd

def load_agribalyse():
    url = "https://drive.google.com/uc?export=download&id=1FLyHBVgPsOeChEvDhd_KZCVr9wEFh5Az"
    return pd.read_csv(url, delimiter=",", decimal=",")

agribalyse = load_agribalyse().copy(deep=True)

def random_diet(food_codes, mean_weight=10, std_dev_weight=5, n_foods=100, seed=42):
    """Returns a random diet"""
    random = np.random.default_rng(seed)
    chosen_foods = random.choice(food_codes, n_foods, replace=False)
    food_weights = random.normal(loc=mean_weight, scale=std_dev_weight, size=n_foods)
    return defaultdict(float, zip(chosen_foods, food_weights))

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
dic_chosen_foods = {
    "Veggie":[brocoli,carotte,pomme,raisin,raclette,oeuf_dur,jus_orange,céréale,riz,pâte],
    "Vegan":[brocoli,carotte,pomme,raisin,lentille,tofu,jus_orange,céréale,riz,pâte],
    "Flexie":[brocoli,carotte,pomme,raisin,raclette,poulet,jus_orange,céréale,riz,pâte],
    "Carnist":[brocoli,carotte,pomme,raisin,poulet,steak,jus_orange,céréale,riz,pâte],
    "Pesci":[brocoli,carotte,pomme,raisin,raclette,saumon,jus_orange,céréale,riz,pâte],
    "Custom":[brocoli,carotte,pomme,raisin,raclette,oeuf_dur,jus_orange,céréale,riz,pâte]
    }
dic_food_weight = {
    "Veggie":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Vegan":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Flexie":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Carnist":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Pesci":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12],
    "Custom":[0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12,0.12,0.12]
    }

def Diet(diet_name):
    '''
        input : diet_name (string)
        output : dictionnary that give for each food (identification by using Ciqual code) a weight (representing weight eaten during a day)
    '''
    if diet_name=="Veggie":
        chosen_foods = dic_chosen_foods["Veggie"]
        food_weights = dic_food_weight["Veggie"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Vegan":
        chosen_foods = dic_chosen_foods["Vegan"]
        food_weights = dic_food_weight["Vegan"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Flexie":
        chosen_foods = dic_chosen_foods["Flexie"]
        food_weights = dic_food_weight["Flexie"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Carnist":
        chosen_foods = dic_chosen_foods["Carnist"]
        food_weights = dic_food_weight["Carnist"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Pesci":
        chosen_foods = dic_chosen_foods["Pesci"]
        food_weights = dic_food_weight["Pesci"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Custom":
        chosen_foods = dic_chosen_foods["Custom"]
        food_weights = dic_food_weight["Custom"]
        return defaultdict(float, zip(chosen_foods, food_weights))
    else:
        assert False, f"diet_name unknown"

def Impact(diet_name,indicator):
    '''
        input : diet_name = name of the diet chosen (string), indicator = name of the indicator chosen (string)(indicator list must be coherent with indicators of radar chart)
        output : Total impact of the diet for one day according to the indicator (string)
    '''
    n = 6 # number of indicator
    indicator_to_column_name = {
        'CO2':'Climate change (KG CO2 EQ / KG product)',
        'Ozone Layer depletion':'Depletion of the ozone layer (E-06 kg CVC11 Eq / kg product)',
        'Terrestrial Eutrophication':'Terrestrial eutrophication (mol N eq / kg of product)',
        'Land use':'Land use (Pt / kg of product)',
        'water&land acidification':'Terrestiral and freshwater acidification (mol h + eq / kg product)',
        'Particles':'Particles (E-06 Disease Inc, / kg of product)'
        }
    column_name = indicator_to_column_name[indicator]
    if diet_name=="Veggie":
        chosen_foods = dic_chosen_foods["Veggie"]
        food_weight = dic_food_weight["Veggie"]
        sum = 0
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    if diet_name=="Vegan":
        chosen_foods = dic_chosen_foods["Vegan"]
        food_weight = dic_food_weight["Vegan"]
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    if diet_name=="Flexie":
        chosen_foods = dic_chosen_foods["Flexie"]
        food_weight = dic_food_weight["Flexie"]
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    if diet_name=="Carnist":
        chosen_foods = dic_chosen_foods["Carnist"]
        food_weight = dic_food_weight["Carnist"]
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    if diet_name=="Pesci":
        chosen_foods = dic_chosen_foods["Pesci"]
        food_weight = dic_food_weight["Pesci"]
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    if diet_name=="Custom":
        chosen_foods = dic_chosen_foods["Custom"]
        food_weight = dic_food_weight["Custom"]
        for i in range(n):
            sum += food_weight[i] * agribalyse[agribalyse['Ciqual Code'] == chosen_foods[i]][column_name].mean()
        return sum
    else:
        assert False, f"diet_name unknown"