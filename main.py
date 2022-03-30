import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from collections import defaultdict
import plotly.figure_factory as ff
import plotly.graph_objects as go

from diet_utils import Impact_normalised, random_diet,Diet,Impact

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

st.title("How's your diet ?")

@st.cache
def load_agribalyse():
    url = "https://drive.google.com/uc?export=download&id=1FLyHBVgPsOeChEvDhd_KZCVr9wEFh5Az"
    return pd.read_csv(url, delimiter=",", decimal=",")

agribalyse = load_agribalyse().copy(deep=True)

# Temporary
diet_list = ["Veggie", "Vegan", "Flexie", "Carnist", "Pesci", "Custom"]
DIETS = dict(zip(diet_list,[Diet(diet_name) for diet_name in diet_list]))


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


def update_weights(database, diet):
    database['weight'] = database['Ciqual Code'].map(diet)

left, right = st.columns(2)

with left:
    st.header("Chose your diet")
    st.radio(
        "Chose your diet", 
        options=DIETS.keys(), 
        key="diet_chosen",
        on_change=lambda : update_weights(agribalyse, DIETS[st.session_state.diet_chosen])
    )
    update_weights(agribalyse, DIETS[st.session_state.diet_chosen])

with right:
    st.header("Diet Composition (by weight)")
    composition = alt.Chart(agribalyse).mark_arc().encode(
        theta=alt.Theta(field="weight", type="quantitative", aggregate="sum"),
        color=alt.Color(field="Food Group", type="nominal", scale=FOOD_COLOR_SCALE),
    )
    st.altair_chart(composition)

#####################################################################################################################
    st.header("Environmental Impact")

    #############
#   Radar char using plotly
    #############
    categories = ['CO2','Ozone Layer depletion','Particles',
              'water&land acidification', 'Land use', 'Terrestrial Eutrophication']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        # st.session_state.diet_chosen représente la diet sélectionné
        r=[Impact_normalised(st.session_state.diet_chosen,indicator) for indicator in categories],
        theta=categories,
        fill='toself',
        name='Product A'
    ))
    # fig.add_trace(go.Scatterpolar(
    #     r=[4, 3, 2.5, 1, 2],
    #     theta=categories,
    #     fill='toself',
    #     name='Product B'
    # ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 11]
        )),
    showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    #############
#   Radar char using matplotlib ?
    #############

