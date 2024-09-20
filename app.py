import tkinter as tk
from tkinter import ttk,filedialog,PhotoImage



class Mainscreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Accounting')
        self.geometry('1280x720')
        #--------------sidebar---------------
        self.sidebar = tk.Frame(self, relief=tk.RAISED, border=5,bg='#384B70',height='100')
        self.sidebar.pack(side=tk.TOP, fill=tk.X,padx=10,pady=10)
        #---btn style------------
        style = ttk.Style()
        style.layout("TMenubutton", [
            ("Menubutton.background", None),
            ("Menubutton.button", {"children":
               [("Menubutton.focus", {"children":
                      [("Menubutton.padding", {"children":
                               [("Menubutton.label",
                                 {"side": "left",
                                  "expand": 1})]
                           })]
                  })]
           }),
        ])
        # btn_style = ttk.Style(self.sidebar).configure('TButtom', padding=6, background='#C8ACD6',foreground='red',relief="flat")
        #----btn--------
        self.home_btn = ttk.Button(self.sidebar,text='خانه',style='TMenubutton',command=self.home)
        self.home_btn.pack(side=tk.RIGHT,padx=10,pady=10)

        self.product_btn = ttk.Button(self.sidebar,text='محصولات',style='TMenubutton',command=self.product_page)
        self.product_btn.pack(side=tk.RIGHT,padx=10,pady=10)

        self.content_frame = tk.Frame(self, bg='#384B70',width='100',height='100')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def home(self):
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg='#433D8B',width='100',height='100')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def product_page(self):
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg='#8C3061',width='100',height='100')
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.topbar = tk.Frame(self.content_frame, relief=tk.RAISED, border=3,bg='#D95F59',height='50')
        self.topbar.pack(side=tk.TOP, fill=tk.X,padx=5,pady=20)


        self.add_product_btn = ttk.Button(self.topbar,text='اضافه کردن محصول')
        self.add_product_btn.pack(side=tk.RIGHT,padx=100,pady=10)

        self.update_product_btn = ttk.Button(self.topbar,text='تغییر در محصول')
        self.update_product_btn.pack(side=tk.RIGHT,padx=100,pady=10)

        self.delete_product_btn = ttk.Button(self.topbar,text='حذف محصول')
        self.delete_product_btn.pack(side=tk.RIGHT,padx=100,pady=10)

        self.product_table = ttk.Treeview(self.content_frame).pack(fill=tk.X,padx=15,pady=5)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("برنامه حسابداری")
        self.geometry("800x600")
        self.config(bg="#384B70")

        self.sidebar = tk.Frame(self, bg="#2E236C", width=200, height=500)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.product_button = tk.Button(self.sidebar, text="محصولات", command=self.product_page, bg="#4CAF50",
                                        fg="#fff", font=("Arial", 12), width=10, height=2, bd=0, relief="ridge",justify='right')
        self.product_button.pack(pady=20)

        self.sales_button = tk.Button(self.sidebar, text="Sales", command=self.sales_page, bg="#03A9F4", fg="#fff",
                                      font=("Arial", 12), width=10, height=2, bd=0, relief="ridge")
        self.sales_button.pack(pady=20)

        self.management_button = tk.Button(self.sidebar, text="Management", command=self.management_page, bg="#FF9800",
                                           fg="#fff", font=("Arial", 12), width=10, height=2, bd=0, relief="ridge")
        self.management_button.pack(pady=20)

        self.content_frame = tk.Frame(self, bg="#f0f0f0", width=600, height=500)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def product_page(self):
        self.title("صفحه محصولات")
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg="#384B70", width=600, height=500)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.product_label = tk.Label(self.content_frame, text="صفحه محصولات", font=("Arial", 24), bg="#f0f0f0")
        self.product_label.pack(pady=20)

        self.product_tree = ttk.Treeview(self.content_frame,
                                         columns=("Product ID", "Product Name", "Quantity", "Price"))
        self.product_tree.pack(pady=20)

        self.product_tree.heading("#0", text="Product")
        self.product_tree.heading("Product ID", text="ID")
        self.product_tree.heading("Product Name", text="Name")
        self.product_tree.heading("Quantity", text="Quantity")
        self.product_tree.heading("Price", text="Price")

        self.product_tree.insert("", "end", values=("1", "Product 1", "10", "100.00"))
        self.product_tree.insert("", "end", values=("2", "Product 2", "20", "200.00"))
        self.product_tree.insert("", "end", values=("3", "Product 3", "30", "300.00"))

    def sales_page(self):
        self.title("Sales Page")
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg="#f0f0f0", width=600, height=500)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.sales_label = tk.Label(self.content_frame, text="Sales Page", font=("Arial", 24), bg="#f0f0f0")
        self.sales_label.pack(pady=20)

        self.sales_tree = ttk.Treeview(self.content_frame,
                                       columns=("Sale ID", "Product ID", "Quantity", "Date", "Total"))
        self.sales_tree.pack(pady=20)

        self.sales_tree.heading("#0", text="Sale")
        self.sales_tree.heading("Sale ID", text="ID")
        self.sales_tree.heading("Product ID", text="Product ID")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.heading("Total", text="Total")

        self.sales_tree.insert("", "end", values=("1", "1", "5", "2022-01-01", "500.00"))
        self.sales_tree.insert("", "end", values=("2", "2", "10", "2022-01-05", "1000.00"))
        self.sales_tree.insert("", "end", values=("3", "3", "15", "2022-01-10", "1500.00"))


    def management_page(self):
        self.title("Management Page")
        self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg="#f0f0f0", width=600, height=500)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.management_label = tk.Label(self.content_frame, text="Management Page", font=("Arial", 24), bg="#f0f0f0")
        self.management_label.pack(pady=20)

        self.management_tree = ttk.Treeview(self.content_frame, columns=("Employee ID", "Name", "Role", "Salary"))
        self.management_tree.pack(pady=20)

        self.management_tree.heading("#0", text="Employee")
        self.management_tree.heading("Employee ID", text="ID")
        self.management_tree.heading("Name", text="Name")
        self.management_tree.heading("Role", text="Role")
        self.management_tree.heading("Salary", text="Salary")

        self.management_tree.insert("", "end", values=("1", "John Doe", "Manager", "5000.00"))
        self.management_tree.insert("", "end", values=("2", "Jane Doe", "Accountant", "4000.00"))
        self.management_tree.insert("", "end", values=("3", "Bob Smith", "Salesman", "3000.00"))


if __name__ == "__main__":
    app = Mainscreen()
    app.mainloop()