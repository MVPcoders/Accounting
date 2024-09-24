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
    df = pd.DataFrame(product_factor["products"],columns=["product_name","brand","price","quantity"])
    st.dataframe(df,width=900,column_config={
        "product_name":"نام محصول",
        "brand": st.column_config.TextColumn("برند",),
        "price":st.column_config.NumberColumn("قیمت"),
        "quantity":st.column_config.NumberColumn("تعداد"),
    },hide_index=True,column_order=("quantity","price","brand","product_name"))
    # Calculate and display the total price
    total_price = df["price"].sum()
    st.write(f"قیمت کل: {total_price:,}  ریال")



def add_item(name,brand,price,quantity):
    try:
        with open("product_factor.json", "r") as f:
            product_factor = json.load(f)
    except FileNotFoundError:
        product_factor = {"products": []}
    new_product = {"product_name": name, "brand": brand,'price':price,'quantity':quantity}
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


