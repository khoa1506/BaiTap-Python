import tkinter as tk
from tkinter import ttk, Menu, messagebox
import psycopg2
from psycopg2 import sql


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bài tập 2")
        self.create_menu()  
        self.create_tabs() 
        
    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu) 
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        help_menu.add_command
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
    def create_tabs(self):
        self.tabControl = ttk.Notebook(self.root)
        self.tab1_frame = ttk.Frame(self.tabControl)
        self.tab2_frame = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1_frame, text="Tab 1")
        self.tabControl.add(self.tab2_frame, text="Tab 2")
        self.tabControl.pack(expand=1, fill="both")

        self.tab1 = Tab1(self.tab1_frame, self.tabControl)
        self.tab2 = Tab2(self.tab2_frame)
        
        self.tab1.set_tab2(self.tab2)
        
class Tab1:
    def __init__(self, parent, tabControl):
        self.tabControl = tabControl
        self.tab1_frame = ttk.LabelFrame(parent, text="Connect Database")
        self.tab1_frame.pack(pady=10)
        
        ttk.Label(self.tab1_frame, text="DB Name").grid(column=0, row=0)
        self.db = tk.StringVar()
        db_enter = ttk.Entry(self.tab1_frame, width=10, textvariable=self.db)
        db_enter.grid(column=0, row=1)
        
        ttk.Label(self.tab1_frame, text="Username").grid(column=0, row=2)
        self.name = tk.StringVar()
        name_enter = ttk.Entry(self.tab1_frame, width=10, textvariable=self.name)
        name_enter.grid(column=0, row=3)
        name_enter.insert(0, "postgres")
        
        ttk.Label(self.tab1_frame, text="Password").grid(column=0, row=4)
        self.mk = tk.StringVar(value="khoa1598753")
        mk_enter = ttk.Entry(self.tab1_frame, width=10, textvariable=self.mk, show="*")
        mk_enter.grid(column=0, row=5)
        
        ttk.Label(self.tab1_frame, text="Host").grid(column=0, row=6)
        self.h = tk.StringVar()
        h_enter = ttk.Entry(self.tab1_frame, width=10, textvariable=self.h)
        h_enter.grid(column=0, row=7)
        h_enter.insert(0, "localhost")
        
        ttk.Label(self.tab1_frame, text="Port").grid(column=0, row=8)
        self.p = tk.StringVar()
        p_enter = ttk.Entry(self.tab1_frame, width=10, textvariable=self.p)
        p_enter.grid(column=0, row=9)
        p_enter.insert(0, "5432")
        
        ttk.Button(self.tab1_frame, text="Connect",width=7, command=self.connect_db).grid(column=0, row=10)
        
    def set_tab2(self, tab2):
        self.tab2 = tab2
        
    def connect_db(self):
        try: 
            self.conn = psycopg2.connect(
            dbname = self.db.get(),
            user = self.name.get(),
            password = self.mk.get(),
            host = self.h.get(),
            port = self.p.get()
        )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.tab2.set_connection(self.conn, self.cur)
            # self.tabControl.select(self.tab2.tab2_frame)


        except Exception as e:
            messagebox.showerror("Error", f"Can't connecting to the database: {e}")


class Tab2:
    def __init__(self, parent):
        self.tab2_frame = ttk.LabelFrame(parent, text="Test")
        self.tab2_frame.pack(pady=10)
    

        ttk.Label(self.tab2_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        self.table_name = tk.StringVar()
        ttk.Entry(self.tab2_frame, textvariable=self.table_name).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(self.tab2_frame, text="Create Table", command=self.create_table).grid(column=0, row=2)
        ttk.Button(self.tab2_frame, text="Load Data", command=self.load_data).grid(column=0, row=3)

        self.data_display = tk.Text(self.tab2_frame, height=10, width=30)
        self.data_display.grid(column=0, row=4, columnspan=2)

        insert_frame = ttk.Frame(self.tab2_frame)
        insert_frame.grid(column=0, row=5)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        ttk.Label(insert_frame, text="Họ tên:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(insert_frame, text="Địa chỉ:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)


    def set_connection(self, conn, cur):
        self.conn = conn
        self.cur = cur
    
    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, diachi) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            self.column1.set("")  
            self.column2.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")
         
    def create_table(self):
        try:
            query = sql.SQL(f"""CREATE table if not exists {self.table_name.get()}(
                    hoten VARCHAR(100),
                    diachi VARCHAR(200)
                    )""")
            self.cur.execute(query)
            self.conn.commit()
            self.data_display.delete(1.0, tk.END)
            self.data_display.insert(tk.END, f"Table {self.table_name.get()} created successfully.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating table: {e}")     


if __name__ == "__main__":
    win = tk.Tk()
    app = App(win)
    win.mainloop()
    