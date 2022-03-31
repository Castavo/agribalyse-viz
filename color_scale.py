import numpy as np
import altair as alt

# Chosing colors for each food group
cat_20 = "1f77b4aec7e8ff7f0effbb782ca02c98df8ad62728ff98969467bdc5b0d58c564bc49c94e377c2f7b6d27f7f7fc7c7c7bcbd22dbdb8d17becf9edae5"
cat_20 = [f"#{cat_20[6*i:6*(i+1)]}" for i in range(20)]
domain = np.array([
    'Drinks', 'Baby foods', 'Fruits, vegetables, legumes and oilseeds',
    'Starters and compound dishes', 'Meat, eggs, fish', 'Cereal products', 
    'Culinary aids and various ingredients', 'Milk and dairy products', 'Fatty products',
    'Ice creams and sorbets', 'Sweet products'
])
color_range = np.array([
    cat_20[1], cat_20[13], cat_20[4],
    cat_20[14], cat_20[6], cat_20[16],
    cat_20[15], cat_20[2], cat_20[3],
    cat_20[17], cat_20[18],
])
sort_idx = np.argsort(domain)
FOOD_COLOR_SCALE=alt.Scale(domain=domain[sort_idx], range=color_range[sort_idx])