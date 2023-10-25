import pandas
import requests
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

fruityvice_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
streamlit.text(fruityvice_response.json())
