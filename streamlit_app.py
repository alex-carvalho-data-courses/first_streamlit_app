import pandas
import requests
import snowflake.connector
import streamlit


my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents new healthy dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build your own Fruit Smoothie')

# put a pick list, enabling to pick the desired fruits
fruits_selected = streamlit.multiselect('Pick some fruits', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# New section to show Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
streamlit.write('the user entered', fruit_choice)

fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it on screen as a table
streamlit.dataframe(fruityvice_normalized)

# query metadata from snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
my_cur = my_cnx.cursor()
my_cur.execute('select * from pc_rivery_db.public.fruit_load_list')
my_data_row = my_cur.fetchall()
streamlit.text('The fruit load contains:')
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
my_cur.execute(f'insert into pc_rivery_db.public.fruit_load_list values (\'{add_my_fruit}\')')
