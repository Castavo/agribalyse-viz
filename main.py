import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from collections import defaultdict
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import requests

from diet_utils import Impact_normalised, random_diet,Diet

st.title("How's your diet ?")

@st.cache
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

# Temporary
diet_list = ["Veggie", "Vegan", "Flexie", "Carnist with beef","Carnist with pork", "Pesci"]
DIETS = dict(zip(diet_list,[Diet(diet_name) for diet_name in diet_list]))


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

    st.header("Environmental impact breakdown")

    # data = LC_impact_diet(st.session_state.diet_chosen,)
    long_df = px.data.medals_long()

    # stacked_bar_chart = px.bar(long_df, x="Food Group", y="Impact", color="Life Cycle Step", title="")
    stacked_bar_chart = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")
    st.plotly_chart(stacked_bar_chart, use_container_width=True)


with right:
    st.header("Diet Composition (by weight)")
    composition = alt.Chart(agribalyse).mark_arc().encode(
        theta=alt.Theta(field="weight", type="quantitative", aggregate="sum"),
        color=alt.Color(field="Food Group", type="nominal", scale=FOOD_COLOR_SCALE),
    )
    st.altair_chart(composition)

#####################################################################################################################
    st.header("Environmental Impact")

    categories = ['CO2','Ozone Layer depletion','Particles',
              'water&land acidification', 'Land use', 'Terrestrial Eutrophication']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[Impact_normalised(st.session_state.diet_chosen,indicator,'Meat, eggs, fish') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Milk and dairy products') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Cereal products') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Fruits, vegetables, legumes and oilseeds') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Other') + 0.1 
         for indicator in categories],
        theta=categories,
        fill='toself',
        name='Other'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[Impact_normalised(st.session_state.diet_chosen,indicator,'Meat, eggs, fish') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Milk and dairy products') +0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Cereal products') +0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Fruits, vegetables, legumes and oilseeds') + 0.1
         for indicator in categories],
        theta=categories,
        fill='toself',
        name='Fruits, vegetables, legumes and oilseeds'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[Impact_normalised(st.session_state.diet_chosen,indicator,'Meat, eggs, fish') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Milk and dairy products') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Cereal products')+ 0.1
         for indicator in categories],
        theta=categories,
        fill='toself',
        name='Cereal products'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[Impact_normalised(st.session_state.diet_chosen,indicator,'Meat, eggs, fish') + 0.1 +
            Impact_normalised(st.session_state.diet_chosen,indicator,'Milk and dairy products') + 0.1
         for indicator in categories],
        theta=categories,
        fill='toself',
        name='Milk and dairy products'
    ))

    fig.add_trace(go.Scatterpolar(
        # st.session_state.diet_chosen représente la diet sélectionné
        r=[Impact_normalised(st.session_state.diet_chosen,indicator,'Meat, eggs, fish') + 0.1 for indicator in categories],
        theta=categories,
        fill='toself',
        name='Meat, eggs, fish'
    ))
    

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 11]
        )),
    showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)


