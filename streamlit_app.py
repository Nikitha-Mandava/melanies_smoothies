import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(""" Choose the fruit you want in custom smoothie!""")

name_on_order = st.text_input('Name of the Smoothie')
st.write('The name on your smoothie will be:', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()  

# convert snowpark dataframe to pandas datfram
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect(
   'choose upto 5 ingredients:',
   my_dataframe,
   max_selections= 5
    
)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

        
    st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients,name_on_order) VALUES ('{}', '{}')""".format(ingredients_string, name_on_order)
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order+ "!" ,icon="✅")





