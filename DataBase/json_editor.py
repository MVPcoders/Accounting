import streamlit as st
import json
import pandas as pd
from streamlit import columns


# def read_json():


def show_item():
    try:
        with open("product_factor.json", "r") as f:
            product_factor = json.load(f)
    except FileNotFoundError:
        product_factor = {"products": []}
    total_price = 0
    st.header("فاکتور")
    # for i, product in enumerate(product_factor["products"]):
        # st.write(f"Product {i+1}: {product['product_name']} - ${product['price']}")
        # st.write(f"{product['product_name']}")
        # st.write(f" قیمت : {product['price']}")
        # st.write(f" تعداد : {product['quantity']}")
        # st.write(f" واحد : {product['unit']}")
    df = pd.DataFrame(product_factor["products"],columns=["product_name","price","unit","quantity"])
    st.table(df)
    # Calculate and display the total price
    total_price = df["price"].sum()
    st.write(f"Total Price: ${total_price:,}")



def add_item(name,price,unit,quantity):
    try:
        with open("product_factor.json", "r") as f:
            product_factor = json.load(f)
    except FileNotFoundError:
        product_factor = {"products": []}
    new_product = {"product_name": name, "price": price,'unit':unit,'quantity':quantity}
    product_factor["products"].append(new_product)
    with open("product_factor.json", "w") as f:
        json.dump(product_factor, f)
    st.write("Product added!")


def reset_factor():
    try:
        with open("product_factor.json", "r") as f:
            product_factor = json.load(f)
    except FileNotFoundError:
        product_factor = {"products": []}
    product_factor = {"products": []}
    with open("product_factor.json", "w") as f:
        json.dump(product_factor, f)


