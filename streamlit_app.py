# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":tropical_drink: Customize Your Smoothie :tropical_drink:")
st.write(
    """Choose the fruit you want in your custom smoothie
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be', name_on_order)


# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingrédients",
    my_dataframe,
    max_selections=5,
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string+=fruit +' '
        st.subheader(fruit + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width=True)
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')
    # st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# st.dataframe(data=my_dataframe, use_container_width=True)



