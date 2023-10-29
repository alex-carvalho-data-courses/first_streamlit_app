import pandas
import requests
import snowflake.connector
import streamlit
from urllib.error import URLError


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


def get_fruityvice_data(fruit_choice: str) -> pandas.DataFrame:
  fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit_choice}')
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

  return fruityvice_normalized
  

# Section to show Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information about.')
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

# query metadata from snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
my_cur = my_cnx.cursor()
my_cur.execute('select * from pc_rivery_db.public.fruit_load_list')
my_data = my_cur.fetchall()
streamlit.text('The fruit load contains:')
streamlit.dataframe(my_data)

streamlit.stop()

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
my_cur.execute(f'insert into pc_rivery_db.public.fruit_load_list values (\'{add_my_fruit}\')')
streamlit.write(f'Thanks for adding {add_my_fruit}')
