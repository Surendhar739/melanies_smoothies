# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in custom Smoothie!
    """
)


import streamlit as st

name_on_order = st.text_input('Name of Smoothie:')
st.write('The name of the Smoothie will be: ', name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()


#session = get_active_session()
#my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    "Choose up to 5 ingredients:"
    ,my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen + 'Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values
       ('""" + ingredients_string +"""','"""+name_on_order+ """')"""
    #my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients, Name_of_order) VALUES ('{ingredients_string}', '{name_of_order}')"

    st.write(my_insert_stmt)
    #st.write(name_of_order)
    st.stop
    #st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
     session.sql(my_insert_stmt).collect()
     #session.sql(name_of_order).collect()
    
     st.success('Your Smoothie '+name_on_order+ ' is ordered!', icon="✅")




