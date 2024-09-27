from cProfile import label
import json
from numpy.ma.core import filled
from streamlit import sidebar
from streamlit_option_menu import option_menu
from DataBase.Data_Editor import Products, Factor
import DataBase.json_editor as json_editor
import streamlit as st
import pandas as pd
from fpdf import FPDF
import pdfkit
import random
password = "1234"
#فراخوانی دیتا بیس  و داده های جدولmain
pro = Products("Data.db")
all = pro.get_all_products()
pro.close_query()
# Customize the UI with a modern theme
st.set_page_config(page_title="Product Catalog", page_icon=":shopping_cart:", layout="wide")

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
            st.dataframe(df, hide_index=True,use_container_width=True,column_order=("inventory","unit", "sell_price", "buy_price", "brand", "product", "id"),column_config={
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


            #####استخراج به صورت پی دی اف#####
            pro = Products("Data.db")

            #### فانکشنی که پی دی اف رو تولید می کنه ###
            def generate_pdf(df):
                html = df.to_html(index=False)
                options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': "UTF-8",
                    'no-outline': None
                }
                pdf_bytes = pdfkit.from_string(html, False, options=options)
                return pdf_bytes

            ### داده ها از جدول گرفته میشه#
            def get_table_data():
                data = pro.get_all_products()
                columns = [descripton[0] for descripton in pro.cursor.description]
                df = pd.DataFrame(data, columns=columns)
                df.columns = ["کد کالا","نام کالا","برند","قیمت خرید","قیمت فروش","واحد","موجودی"]
                return df
            #خروجی به صورت پی دی اف تولید میشه
            df = get_table_data()
            pdf_bytes = generate_pdf(df)
            st.download_button("پی دی اف", pdf_bytes, file_name="product_table.pdf", mime='application/pdf')

        #######
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
                buy_price = st.number_input("قیمت خرید",step=1)
                sell_price = int(buy_price * 1.15)
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
    factor_style = """
    <style>
    [data-testid="element-container"]{
        text-align: center;
    }
    </style>
    """
    st.markdown(factor_style, unsafe_allow_html=True)
    st.title('فاکتور دهی')
    factor = Factor("Data.db")
    factor_table = factor.factor_columns()
    factor.close_query()
    df = pd.DataFrame(factor_table, columns=[desc[0] for desc in factor.cursor.description])
    st.dataframe(df,width=1000,hide_index=True,column_order=("inventory","sell_price","brand","product"),column_config={
        "product":st.column_config.TextColumn("محصول"),
        "brand":st.column_config.TextColumn("برند"),
        "sell_price":st.column_config.NumberColumn("قیمت فروش"),
        "inventory":st.column_config.NumberColumn("موجود در انبار"),
    })
    # json_editor.add_item("a",12,"unn",5)

    name = st.text_input("نام کالا")
    if name:
        factor = Factor("Data.db")
        product_info = factor.fuzzy_search(name)
        factor.close_query()
        st.write(" کالای پیدا شده : "+product_info[0][1])
        st.write("برند کالا : "+product_info[0][2])
        st.write(" قیمت فروش : "+product_info[0][4])
        st.write(" تعداد در انبار : "+str(product_info[0][6]))
        quantity = st.number_input("تعداد فروش", value=int(product_info[0][6]),step=1)
        if st.button('add'):
            json_editor.add_item(product_info[0][1],product_info[0][2],int(product_info[0][4])*quantity, quantity)
    json_editor.show_item()
    if st.button('reset'):
        json_editor.reset_factor()


