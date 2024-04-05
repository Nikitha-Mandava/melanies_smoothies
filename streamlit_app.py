import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(""" Choose the fruit you want in custom smoothie!""")

name_on_order = st.text_input('Name of the Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
   'choose upto 5 ingredients:',
   my_dataframe,
   max_selections= 5
    
)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen
    st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients,name_on_order) VALUES ('{}', '{}')""".format(ingredients_string, name_on_order)
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order+ "!" ,icon="✅")