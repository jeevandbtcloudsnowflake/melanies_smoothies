# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"{st.__version__}")
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw: ")

st.write("""Choose the fruits you want in custom smoothie""")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

# session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
# convert snwopark data frame to pandas dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
ingredients_list=st.multiselect('Choose upto 5 ingredients:',my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen + ' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    st.write(ingredients_list)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('submit order')
    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+name_on_order+'!', icon="✅")


