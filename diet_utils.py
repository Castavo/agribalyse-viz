"""
Manipulating diets
Let's say a diet is just a dict like :
{ CIQUAL code (= food id) : weight (in kilograms ?) }
And each line would be how much of the food chosen you eat per year (?)
"""
from collections import defaultdict
import numpy as np

def random_diet(food_codes, mean_weight=10, std_dev_weight=5, n_foods=1000, seed=42):
    """Returns a random diet"""
    random = np.random.default_rng(seed)
    chosen_foods = random.choice(food_codes, n_foods, replace=False)
    food_weights = random.normal(loc=mean_weight, scale=std_dev_weight, size=n_foods)
    return defaultdict(float, zip(chosen_foods, food_weights))
