import pandas
import streamlit

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

streamlit.title('My Parents new healthy dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build your own Fruit Smoothie')
strealit.dataframe(my_fruit_list)
