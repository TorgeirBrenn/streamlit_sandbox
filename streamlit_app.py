import streamlit
import pandas
import requests
import snowflake.connector

from urllib.error import URLError

# Set up page
streamlit.title("My Parents' New Healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Read data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # Better selection later.

# Let's put a pick list here so they can pick the fruit they want to include.
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")


def get_fruityvice_data(fruit: str):
  try: 
    response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
  except URLError as e:
    streamlit.error(f"Error '{e}'")
  
  normalized = pandas.json_normalize(response.json())
  return normalized


fruit_choice = streamlit.text_input("What fruit would you like information about?")
if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
else:
  fruityvice_normalized = get_fruityvice_data(fruit_choice)
  streamlit.dataframe(fruityvice_normalized)

# Snowflake Hello World!
streamlit.header("The fruit load list contains:")
 

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
 
def insert_snowflake_row(fruit: str):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{fruit}')")
  
  streamlit.text(f"Thanks for adding {add_my_fruit}")
  
 
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = my_cur.get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
