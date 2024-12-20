import sqlitecloud
import logging
import streamlit as st
import streamlit.components.v1 as components

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the database
def setup_database():
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            image TEXT,
            name TEXT,
            price TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fetch products from the database
def fetch_products():
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('SELECT id, image, name, price FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

# Insert a new product into the database
def insert_product(image, name, price):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (image, name, price) VALUES (?, ?, ?)', (image, name, price))
    conn.commit()
    conn.close()

# Update an existing product in the database
def update_product(product_id, image, name, price):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET image = ?, name = ?, price = ? WHERE id = ?', (image, name, price, product_id))
    conn.commit()
    conn.close()

# Update an existing product's price in the database
def update_product_price(product_id, price):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET price = ? WHERE id = ?', (price, product_id))
    conn.commit()
    conn.close()

# Delete a product from the database
def delete_product(product_id):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gass?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    try:
        logging.debug(f"Attempting to delete product with ID: {product_id}")
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        st.success("Product deleted successfully!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

# Streamlit app
st.title("🛍️ Product Management Dashboard")

# Setup the database
setup_database()

# Fetch and display products
st.sidebar.header("Product List")
products = fetch_products()
for product in products:
    try:
        st.sidebar.image(product[1], width=100)
    except Exception as e:
        st.sidebar.write(f"Error loading image: {e}")
    st.sidebar.write(f"**ID:** {product[0]} | **Name:** {product[2]} | **Price:** {product[3]}")

# Add a new product
st.header("Add a New Product")
with st.form(key='add_product_form'):
    image = st.text_input("Image URL")
    name = st.text_input("Product Name")
    price = st.text_input("Price")
    submit_button = st.form_submit_button(label='Add Product')
    if submit_button:
        insert_product(image, name, price)
        st.success("Product added successfully!")

# Update an existing product's price
st.header("Update Product Price")
with st.form(key='update_product_price_form'):
    product_id = st.number_input("Product ID", min_value=1, step=1)
    new_price = st.text_input("New Price")
    update_button = st.form_submit_button(label='Update Price')
    if update_button:
        update_product_price(product_id, new_price)
        st.success("Product price updated successfully!")

# Delete a product
st.header("Delete a Product")
with st.form(key='delete_product_form'):
    delete_product_id = st.number_input("Product ID to Delete", min_value=1, step=1)
    delete_button = st.form_submit_button(label='Delete Product')
    if delete_button:
        delete_product(delete_product_id)

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
html_string='''

<script>
// To break out of iframe and access the parent window
const streamlitDoc = window.parent.document;

// Make the replacement
document.addEventListener("DOMContentLoaded", function(event){
        streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "Provided by <a href='https://yourwebsite.com' target='_blank' class='css-z3au9t egzxvld2'>Your Link Display Text Here</a>";
    });
</script>
'''
components.html(html_string)
#----------------------Hide Streamlit footer----------------------------
