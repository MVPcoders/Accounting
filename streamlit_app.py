from numpy.ma.core import filled
from streamlit import sidebar
from streamlit_option_menu import option_menu
from DataBase.Data_Editor import Products
import streamlit as st
import pandas as pd
import random
password = "1234"
#فراخوانی دیتا بیس  و داده های جدول
pro = Products("Data.db")
all = pro.get_all_products()
pro.close_query()
st.set_page_config(layout="wide")

with sidebar:
    selected = option_menu(
        menu_title="حسابداری",
        options=["مدیریت","فاکتور","فروش"],
        icons=["house","person-check","check-all"],
        menu_icon="cast",
        default_index=0,
        )

if selected == 'مدیریت':
    user_pass = st.text_input('رمز مدیریت را وارد کنید')
    if user_pass == password:
        st.success("joind")
        table_style = """
            <style>
            [data-testid="stDataFrameResizable"]{
                text-align: right;        
            }
            [data-testid="stHeadingWithActionElements"]{
                text-align: center;
            }
            [data-testid="stAppViewContainer"]{
        
            }
            </style>
        """
        st.markdown(table_style, unsafe_allow_html=True)
        editor, table = st.columns(2)
        with table:
            df = pd.DataFrame(all, columns=[desc[0] for desc in pro.cursor.description])
            st.dataframe(df, hide_index=True,use_container_width=True,column_config={
                "id": st.column_config.NumberColumn(
                    'کد کالا',
                    width= 10,
                ),
                "product": st.column_config.TextColumn(
                    'نام کالا',
                ),
                "brand" : st.column_config.TextColumn(
                    "برند"
                ),
                "buy_price" : st.column_config.NumberColumn(
                    "قیمت خرید",
                    help= 'قیمت به ریال'
                ),
                "sell_price" : st.column_config.NumberColumn(
                    "قیمت فروش",
                    help= 'قیمت به ریال'
                ),
                "unit": st.column_config.TextColumn(
                    "واحد",
                    width=10,
                ),
                "inventory" : st.column_config.NumberColumn(
                    "موجودی انبار",
                    width= 10,
                )
            })
        with editor:
            crud = option_menu(
                menu_title=None,
                options=['کالای جدید','ویرایش کالا','حذف کالا'],
                default_index=0,
                orientation='horizontal',
            )
            if crud == 'کالای جدید':
                pro = Products("Data.db")
                #ساخت فرم برای اضافه کردن کالا
                st.title("کالای جدید")
                product = st.text_input("نام کالا", key="add_product")
                brand = st.text_input("برند")
                buy_price = st.text_input("قیمت خرید")
                sell_price = st.text_input("قیمت فروش")
                unit = st.text_input("واحد")
                inventory = st.number_input("موجودی", value=0)
                # اضافه کردن کالا به دیتا بیس
                if st.button("ثبت"):
                    pro.add_product(product, brand, buy_price, sell_price, unit, inventory)
                    st.success("کالا با موفقیت اضافه شد")
                    #قطع ارتباط با دیتا بیس
                    pro.close_query()
            if crud == 'ویرایش کالا':
                pro = Products("Data.db")
                st.title('تغییر در کالا')
                edit_chose = st.radio("نوع جستجو",options=[
                    'جستجو بر اساس نام',
                    'جستجو بر اساس شماره کالا'
                ])
                if edit_chose == "جستجو بر اساس نام":
                    product_name = st.text_input("نام کالا", key="update_product_by_name")
                    if product_name:
                        product_by_name = pro.get_product_by_name(product_name)
                        st.subheader('مشخصات کالای مورد نظر')
                        product = st.text_input("نام کالا", value=product_by_name[1])
                        brand = st.text_input("برند", value=product_by_name[2])
                        buy_price = st.text_input("قیمت خرید", value=product_by_name[3])
                        sell_price = st.text_input("قیمت فروش", value=product_by_name[4])
                        unit = st.text_input("واحد", value=product_by_name[5])
                        inventory = st.number_input("موجودی انبار", value=product_by_name[6])
                else:
                    product_id = st.text_input("شماره کالا", key="update_product_by_id")
                    if product_id :
                        try:
                            product_by_id = pro.get_product_by_id(product_id)
                            st.subheader('مشخصات کالای مورد نظر')
                            product = st.text_input("نام کالا", value=product_by_id[1])
                            brand = st.text_input("برند",value=product_by_id[2])
                            buy_price = st.text_input("قیمت خرید",value=product_by_id[3])
                            sell_price = st.text_input("قیمت فروش",value=product_by_id[4])
                            unit = st.text_input("واحد", value=product_by_id[5])
                            inventory = st.number_input("موجودی انبار", value=product_by_id[6])
                        except:
                            st.error('چنین محصولی نداریم')
                            pro.close_query()
                        if st.button("تغییر"):
                            try:
                                pro.update_product(product_id,product, brand, buy_price, sell_price, unit, inventory)
                                pro.close_query()
                                st.success('با موفقیت تغییر پیدا کرد')
                            except:
                                st.error('نتونستم تغییرش بدم')
                                pro.close_query()



            if crud == 'حذف کالا':
                pro = Products("Data.db")
                st.title("حذف کالا")
                product_id = st.text_input("شماره کالا",key="delete_product_by_id")
                if product_id :
                    try:
                        prodict_name = pro.get_product_by_id(product_id)
                        st.subheader(" مشخصات کالای مورد نظر")
                        st.write(f"##### نام کالا:  {prodict_name[1]}")
                        st.write(f"##### برند: {prodict_name[2]}")
                        st.write(f"##### قیمت خرید:  {prodict_name[3]} ")
                        st.write(f"##### قیمت فروش: {prodict_name[4]} ")
                        st.write(f"##### واحد : {prodict_name[5]} ")
                        st.write(f"##### موجودی انبار : {prodict_name[6]} ")
                        if st.button("##### حذف کالا"):
                            # button click logic here
                            pro.delete_product(product_id)
                            pro.close_query()
                    except:
                        st.error('چنین محصولی نداریم')
                        pro.close_query()
if selected == 'فاکتور':
    st.title('فاکتور دهی')
    df = pd.DataFrame(all, columns=[desc[0] for desc in pro.cursor.description])
    st.table(df)
    name = st.text_input("نام کالا")
    if name:
        pro = Products("Data.db")
        product_info = pro.fuzzy_search(name)
        st.write(product_info)




# df = pd.DataFrame(all, columns=[desc[0] for desc in pro.cursor.description])
# # df.style.set_properties(subset=['id', 'inventory'], **{'text-align': 'right', 'width': '40px', 'max-width': '40px'})
# # df.columns = ['کد کالا', 'نام کالا', 'برند', 'قیمت خرید', 'قیمت فروش', 'موجودی در انبار']
# st.markdown("""
#   <style>
#   table {
#       background-color: #f0f0f0;
#       font-size: 18px;
#       text-align: right;
#   }
#   </style>
#   """, unsafe_allow_html=True)
# st.table(df)




