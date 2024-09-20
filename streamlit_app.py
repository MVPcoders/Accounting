from DataBase.Data_Editor import Products
import streamlit as st
import pandas as pd

#فراخوانی دیتا بیس  و داده های جدول
pro = Products("Data.db")
all = pro.get_all_products()


#نمایش جدول کالا ها در استریم لیت
df = pd.DataFrame(all, columns=[desc[0] for desc in pro.cursor.description])
df.columns = ['کد کالا', 'نام کالا', 'برند', 'قیمت خرید', 'قیمت فروش', 'موجودی در انبار']
st.dataframe(df, hide_index=True)


#ساخت فرم برای اضافه کردن کالا
st.title("کالای جدید")

product = st.text_input("نام کالا")
brand = st.text_input("برند")
buy_price = st.text_input("قیمت خرید")
sell_price = st.text_input("قیمت فروش")
inventory = st.number_input("موجودی در انبار", value=0)

# اضافه کردن کالا به دیتا بیس
if st.button("ثبت"):
    pro.add_product(product, brand, buy_price, sell_price, inventory)
    st.success("کالا با موفقیت اضافه شد")

#قطع ارتباط با دیتا بیس
pro.close_query()


#به روز رسانی صفحه با زدن کلید  R





