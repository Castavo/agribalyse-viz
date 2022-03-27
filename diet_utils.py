"""
Manipulating diets
Let's say a diet is just a dict like :
{ CIQUAL code (= food id) : weight (in kilograms ?) }
And each line would be how much of the food chosen you eat per year (?)
"""
from collections import defaultdict
import numpy as np

def random_diet(food_codes, mean_weight=10, std_dev_weight=5, n_foods=100, seed=42):
    """Returns a random diet"""
    random = np.random.default_rng(seed)
    chosen_foods = random.choice(food_codes, n_foods, replace=False)
    food_weights = random.normal(loc=mean_weight, scale=std_dev_weight, size=n_foods)
    return defaultdict(float, zip(chosen_foods, food_weights))

def Diet(diet_name):
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

    if diet_name=="Veggie":
        chosen_foods = [brocoli,carotte,pomme,raisin,raclette,oeuf_dur,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Vegan":
        chosen_foods = [brocoli,carotte,pomme,raisin,lentille,tofu,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Flexie":
        chosen_foods = [brocoli,carotte,pomme,raisin,raclette,poulet,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Carnist":
        chosen_foods = [brocoli,carotte,pomme,raisin,poulet,steak,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Pesci":
        chosen_foods = [brocoli,carotte,pomme,raisin,raclette,saumon,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    if diet_name=="Custom":
        chosen_foods = [brocoli,carotte,pomme,raisin,raclette,oeuf_dur,jus_orange,céréale,riz,pâte]
        food_weights = [0.1,0.1,0.15,0.1,0.1,0.1,0.1,0.12]
        return defaultdict(float, zip(chosen_foods, food_weights))
    else:
        assert False, f"diet_name unknown"
