import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import requests

from diet_utils import Impact_normalised, Diet, DIET_LIST, FOOD_GROUP_LIST, INDICATOR_TO_COLUMN_NAME
import requests

from color_scale import FOOD_COLOR_SCALE


@st.cache
def load_agribalyse():
    synthese_url = "https://drive.google.com/uc?export=download&id=1FLyHBVgPsOeChEvDhd_KZCVr9wEFh5Az"
    agb_synthesis =  pd.read_csv(synthese_url, delimiter=",", decimal=",")
    print("Synthesis loaded", len(agb_synthesis))

    agb_synthesis.set_index("Ciqual Code", inplace=True, drop=False)
    global FOOD_GROUP_LIST
    agb_synthesis.loc[~agb_synthesis["Food Group"].isin(FOOD_GROUP_LIST), "Food Group"] = "Other"

    nutrition_url = "https://drive.google.com/uc?export=download&id=1sHOHK52i1LLv2WEnSWMlE9TbgL3pyQtJ"
    nutrition =  pd.read_csv(nutrition_url, delimiter=";", decimal=",")
    print("Nutritional values loaded", len(nutrition))

    nutrition = nutrition[nutrition["HYPOTH"]=="MB"]
    nutrition.set_index("alim_code", inplace=True)
    nutrition.drop(["FOOD_LABEL", "HYPOTH"], axis=1)
    agb_synthesis = agb_synthesis.join(nutrition, how="inner")

    detail_url = "https://drive.google.com/uc?export=download&id=1dxL_5Mm67ncoC28FCJsvaOJgAjH5DMD7"
    agb_detail = requests.get(detail_url).json()
    print("Detail loaded", len(agb_detail))

    env_impact_cats = list(sorted(agb_detail[0]["environmental_impact"].keys()))
    step_names = list(agb_detail[0]["environmental_impact"]["Single Score EF"]["steps"].keys())
    multi_index = pd.MultiIndex.from_product(
        [env_impact_cats, step_names], 
        names=['Impact type', 'Life cycle step'])

    impact_data=[
        [food["environmental_impact"][cat]["steps"][step] for cat in env_impact_cats for step in step_names]
        for food in agb_detail
    ]
    life_cycle_detail = pd.concat(
        (
            pd.DataFrame(
                data=[int(food["ciqual_AGB"]) for food in agb_detail], columns=["Ciqual Code"]
            ),
            pd.DataFrame(data=impact_data, columns=multi_index),
        ), 
        axis=1
    )
    return agb_synthesis, life_cycle_detail, env_impact_cats, step_names

AGRIBALYSE_ORIG, LIFE_CYCLE_DETAIL_ORIG, ENV_IMPACT_CATS, STEP_NAMES = load_agribalyse()
AGRIBALYSE = AGRIBALYSE_ORIG.copy(deep=True)
LIFE_CYCLE_DETAIL = LIFE_CYCLE_DETAIL_ORIG.copy(deep=True)
if not "Other" in FOOD_GROUP_LIST:
    FOOD_GROUP_LIST += ["Other"]
DIETS = dict(zip(DIET_LIST, [Diet(diet_name) for diet_name in DIET_LIST]))


# =========================== Charts  ================================


st.title("How's your diet ?")

def update_weights(diet):
    AGRIBALYSE['weight'] = AGRIBALYSE['Ciqual Code'].map(diet)
    LIFE_CYCLE_DETAIL['weight'] = LIFE_CYCLE_DETAIL['Ciqual Code'].map(diet)


left, right = st.columns(2)

with left:
    # =========================== Diet choice ================================
    st.header("Chose your diet")
    st.radio(
        "Chose your diet", 
        options=DIETS.keys(), 
        key="diet_chosen",
        on_change=lambda : update_weights(DIETS[st.session_state.diet_chosen])
    )
    update_weights(DIETS[st.session_state.diet_chosen])

    # =========================== Diet nutritional value ================================
    st.header("Nutritional value")


with right:
    # =========================== Composition ================================
    st.header("Diet Composition (by weight)")
    composition = alt.Chart(AGRIBALYSE).mark_arc().encode(
        theta=alt.Theta(field="weight", type="quantitative", aggregate="sum"),
        color=alt.Color(field="Food Group", type="nominal", scale=FOOD_COLOR_SCALE),
    )
    st.altair_chart(composition)


# =========================== Environmental impact ================================
st.header("Environmental Impact")

st.markdown("This spider chart is normalized by dividing each indicator by the maximum value over all diets.")

fig = go.Figure()

cumulated_impacts = np.array([
    .1 + np.cumsum(
        [
            Impact_normalised(
                st.session_state.diet_chosen, 
                indicator, 
                food_group, 
                AGRIBALYSE
            ) 
            for food_group in FOOD_GROUP_LIST
        ]
    )
    for indicator in INDICATOR_TO_COLUMN_NAME
])

for i, group in enumerate(FOOD_GROUP_LIST[::-1]):
    fig.add_trace(go.Scatterpolar(
        r=cumulated_impacts[:, -i-1],
        theta=list(INDICATOR_TO_COLUMN_NAME.keys()),
        fill='toself',
        name=group
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

# =========================== Life cycle step environmental impact ================================
st.header("Environmental impact at each step of the life cycle")

st.selectbox(
    label="Impact indicator",
    options=ENV_IMPACT_CATS,
    key="env_impact_cat",
    index=ENV_IMPACT_CATS.index("Single Score EF")
)

st.markdown("For more information about the meaning of each indicator, see the [Agribalyse documentation](https://doc.agribalyse.fr/documentation/methodologie-acv). We do not report them here because what matters most in this visualization is the comparison of the different food groups and life cycle steps inside the diet.")

weighted_impacts = LIFE_CYCLE_DETAIL[
    [(st.session_state.env_impact_cat, step) for step in STEP_NAMES]
].mul(LIFE_CYCLE_DETAIL["weight"], axis=0)
weighted_impacts.columns = STEP_NAMES
weighted_impacts = pd.concat([LIFE_CYCLE_DETAIL[["Ciqual Code"]], weighted_impacts], axis=1)

data = weighted_impacts.merge(AGRIBALYSE[["Ciqual Code", "Food Group"]], on="Ciqual Code")
life_cycle_impact = alt.Chart(data).mark_bar().transform_fold(
    STEP_NAMES, as_=["step", "value"]
).encode(
    x=alt.X("Food Group:N", sort="-y"),
    y=alt.Y("sum(value):Q", title="Impact in the given category"),
    color=alt.Color("step:N", title="Life cycle step"),
).properties(
    height=500,
)

st.altair_chart(life_cycle_impact, use_container_width=True)

