import numpy as np
import altair as alt

# Chosing colors for each food group
# cat_20 = "1f77b4aec7e8ff7f0effbb782ca02c98df8ad62728ff98969467bdc5b0d58c564bc49c94e377c2f7b6d27f7f7fc7c7c7bcbd22dbdb8d17becf9edae5"
cat_20 = np.array(['#847685','#17d11a','#f7161a','#fffb00','#00fffb'])
domain = np.array([
    'Other', 'Fruits, vegetables, legumes and oilseeds',
    'Meat, eggs, fish', 'Cereal products', 
    'Milk and dairy products'
])
color_range = np.array([
    cat_20[0], cat_20[1], cat_20[2],
    cat_20[3], cat_20[4]])
sort_idx = np.argsort(domain)
FOOD_COLOR_SCALE=alt.Scale(domain=domain[sort_idx], range=cat_20[sort_idx])