# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title("Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Snowflake session
cnx = st.connection("snowflake",type="snowflake")
session = cnx.session()

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get fruit names as a Python list
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))
fruit_list = [r["FRUIT_NAME"] for r in fruit_df.collect()]

# Ingredients selector
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

# Submit button
time_to_insert = st.button("Submit Order")

if time_to_insert:
    if not (1 <= len(ingredients_list) <= 5):
        st.error("Please choose 1–5 ingredients.")
    elif not name_on_order:
        st.error("Please enter a name for the smoothie.")
    else:
        ingredients_string = " ".join(ingredients_list)
        # Escape single quotes
        ing = ingredients_string.replace("'", "''")
        nom = name_on_order.replace("'", "''")

        # Correct INSERT: specify both columns
        my_insert_stmt = f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ing}', '{nom}')
        """
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
