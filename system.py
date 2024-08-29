from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg
import pandas as pd
from datetime import date, datetime
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Combobox
import sqlite3
import os
import sys

import pandas as pd


mainframe = Tk()
mainframe.geometry('1700x950+50+50')
mainframe.title('Vuno Kuu System')

conn = sqlite3.connect('member_data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS members (
    reg_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    reg_date TEXT NOT NULL,
    national_id TEXT DEFAULT 'N/A',
    bank TEXT DEFAULT 'N/A',
    account_no TEXT DEFAULT 'N/A',
    phone TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()



def welcome():
    welcomeframe.destroy()
    navigationFrame.configure(width=400)
    hideButton.config(text='HIDE MENU', bg='#07531f', fg='white')
    hideButton.place(x=275, y=2)
    hideButton.config(command=hidebutton)
def homepage():
    registration = IntVar()
    Date = StringVar()

    def reg_no():
        cursor.execute("SELECT MAX(Reg_No) FROM members")
        max_row_value = cursor.fetchone()[0]

        if max_row_value is not None:
            registration.set(max_row_value + 1)
        else:
            registration.set(1)

    def clear():
        Name.set('')
        nationalId.set('')
        bank.set('')
        acc_number.set('')
        phone.set('')
        reg_no()
        saveButton.config(state='normal')

    def Save():
        R1 = registration.get()
        N1 = Name.get()
        NI1 = nationalId.get() if nationalId.get() else "N/A"
        B1 = bank.get() if bank.get() else "N/A"
        AC1 = acc_number.get() if acc_number.get() else "N/A"
        D1 = Date.get()
        P1 = phone.get()

        if N1 == '' or P1 == '':
            messagebox.showerror('error', 'Name and Phone fields are required.')
        else:
            cursor.execute('''
            INSERT INTO members (name, reg_date, national_id, bank, account_no, phone)
            VALUES (?, ?, ?, ?, ?, ?)''', (N1, D1, NI1, B1, AC1, P1))
            conn.commit()

            messagebox.showinfo("info", "Successfully added!!!")
            clear()
            reg_no()

    def search1():
        text = search.get()
        clear()
        updateButton.config(state='normal')
        saveButton.config(state='disabled')

        if search.get() == '':
            messagebox.showerror('Search', 'Enter the member number')
        else:
            cursor.execute("SELECT * FROM members WHERE Reg_No=?", (text,))
            record = cursor.fetchone()

            if record:
                registration.set(record[0])
                Name.set(record[1])
                Date.set(record[2])
                nationalId.set(record[3])
                bank.set(record[4])
                acc_number.set(record[5])
                phone.set(record[6])
            else:
                messagebox.showerror('Invalid', 'Registration number not found')

    def update():
        R1 = registration.get()
        N1 = Name.get()
        NI1 = nationalId.get()
        B1 = bank.get()
        AC1 = acc_number.get()
        D1 = Date.get()
        P1 = phone.get()

        cursor.execute('''UPDATE members SET Name=?, Reg_Date=?, National_ID=?, Bank=?, Account_No=?, Phone_Number=? 
                              WHERE Reg_No=?''',
                       (N1, D1, NI1, B1, AC1, P1, R1))
        conn.commit()
        messagebox.showinfo("Info", "Updated successfully!!!")
        clear()
        reg_no()

        Srch.config(state='normal')


    homeframe= Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com",font='arial 12 italic', width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER REGISTRATION", width=10, height=2, bg="#07531f", fg='#fff', font='arial 25 bold underline').pack(
        side=TOP, fill=X, pady=60, padx=30)
    inputframe = Frame(workingFrame, bg='#07531f')
    inputframe.pack(pady=10)
    inputframe.configure(width=990, height=1000)
    ###Search box to search for member
    search = StringVar()
    Entry(inputframe, textvariable=search, width=12, bd=0, font='arial 30 bold', fg='#07531f').place(x=35, y=20)
    Srch = Button(inputframe, text="Search",width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', command=search1)
    Srch.place(x=370, y=16)
    updateButton = Button(inputframe, text="Update", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', state='disabled', command=update)
    updateButton.place(x=693, y=16)

    registration = IntVar()
    Date = StringVar()
    Label(inputframe,text='Reg_ID:',  font='arial 20 bold', fg='white', bg='#07531f').place(x=35, y=120)
    Reg_ID = Entry(inputframe, textvariable=registration,width=15, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=200, y=120)
    reg_no()

    Name = StringVar()
    Label(inputframe, text='Name:', font='arial 20 bold', fg='white', bg='#07531f').place(x=35, y=220)
    nameEntry = Entry(inputframe,textvariable=Name,  width=15, bd=0, font='arial 23 bold', fg='#07531f').place(x=200, y=220)

    nationalId = StringVar()
    Label(inputframe, text='National ID:', font='arial 20 bold', fg='white', bg='#07531f').place(x=35, y=320)
    natId = Entry(inputframe,textvariable=nationalId, width=15, bd=0, font='arial 23 bold', fg='#07531f').place(x=200, y=320)

    bank = StringVar()
    Label(inputframe, text='Bank:', font='arial 20 bold', fg='white', bg='#07531f').place(x=35, y=420)
    bankEntry = Entry(inputframe,textvariable=bank, width=15, bd=0, font='arial 23 bold', fg='#07531f').place(x=200, y=420)



    Label(inputframe, text='Reg_Date:', font='arial 20 bold', fg='white', bg='#07531f').place(x=535, y=120)
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    Reg_Date = Entry(inputframe,textvariable=Date, width=15, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=700, y=120)
    Date.set(d1)

    phone = StringVar()
    Label(inputframe, text='Phone_No:', font='arial 20 bold', fg='white', bg='#07531f').place(x=535, y=220)
    phoneEntry = Entry(inputframe,textvariable=phone, width=15, bd=0, font='arial 23 bold', fg='#07531f').place(x=700, y=220)

    acc_number = StringVar()
    Label(inputframe, text='Acc_No:', font='arial 20 bold', fg='white', bg='#07531f').place(x=535, y=320)
    accnumber = Entry(inputframe, textvariable=acc_number, width=15, bd=0, font='arial 23 bold', fg='#07531f').place(
        x=700, y=320)

    prof_frame = Frame(inputframe, bd=3, bg="white", width=925, height=100, relief=GROOVE)
    prof_frame.place(x=35, y=520)



    saveButton = Button(prof_frame, text='Save',width=10, font='arial 20 bold', fg='#07531f', bg='lightblue', command=Save)
    saveButton.place(x=20, y=20)
    resetButton = Button(prof_frame, text='Reset', width=10, font='arial 20 bold', fg='#07531f', bg='#e96c6c', command=clear)
    resetButton.place(
        x=380, y=20)
    exitButton = Button(prof_frame, text='Exit', width=10, font='arial 20 bold', fg='#07531f', bg='red')
    exitButton.place(x=720, y=20)






    homeframe.pack(pady=20)
    homeframe.configure(width=1600, height=1150)


def add_page():


    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS member_records (
        top_id INTEGER PRIMARY KEY AUTOINCREMENT,
        reg_no INTEGER NOT NULL,
        name TEXT NOT NULL,
        topping_date TEXT NOT NULL,
        time TEXT NOT NULL,
        amount_kgs REAL NOT NULL,
        FOREIGN KEY(reg_no) REFERENCES members(reg_no)
    )
    ''')
    conn.commit()

    def Top_ID():
        cursor.execute('SELECT MAX(top_id) FROM member_records')
        max_row_value = cursor.fetchone()[0]
        Topping_ID.set(max_row_value + 1 if max_row_value is not None else 1)

    def Clear():
        search.set('')
        Name.set('')
        addition.set('')
        Reg_No.set('')

    def search2():
        text = search.get()

        if text == '':
            messagebox.showerror('Search', 'Enter the member number')
        else:
            cursor.execute('SELECT reg_no, name FROM members WHERE reg_no = ?', (text,))
            result = cursor.fetchone()

            if result:
                Reg_No.set(result[0])
                Name.set(result[1])
            else:
                messagebox.showerror('Invalid', 'Registration number not found')

    def save2():
        today = date.today()
        Date = today.strftime("%d/%m/%Y")
        top_time = datetime.now().strftime("%H:%M:%S")

        T1 = Topping_ID.get()
        R1 = Reg_No.get()
        N1 = Name.get()
        TD = Date
        TT = top_time
        A1 = addition.get()

        if A1 == '' or R1 == '' or N1 == '':
            messagebox.showerror('Error', 'Cannot leave blank fields')
        else:
            cursor.execute('''
            INSERT INTO member_records (reg_no, name, topping_date, time, amount_kgs)
            VALUES (?, ?, ?, ?, ?)''', (R1, N1, TD, TT, A1))
            conn.commit()

            messagebox.showinfo("Info", "Record saved successfully!")
            Clear()
            Top_ID()








    add_frame = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S DELIVERY", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(
        side=TOP, fill=X, pady=60, padx=30)

    inputframe = Frame(workingFrame, bg='#07531f')
    inputframe.pack(pady=10)
    inputframe.configure(width=990, height=1000)

    #Search box to search for member
    search = IntVar()
    SearchEntry=Entry(inputframe, textvariable=search, width=12, bd=0, font='arial 30 bold', fg='#07531f').place(x=35, y=20)
    Srch = Button(inputframe, text="Search", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', command=search2)
    Srch.place(x=370, y=16)


    Label(inputframe, text='Reg_No:', font='arial 20 bold', fg='white', bg='#07531f').place(x=150, y=120)
    Topping_ID = IntVar()
    Topping = Entry(inputframe, textvariable=Topping_ID, width=20, bd=0, font='arial 23 bold', fg='#07531f',
                     state='disabled')
    #Topping.place(x=700, y=150)
    Top_ID()
    Reg_No = StringVar()
    regEntry = Entry(inputframe, textvariable=Reg_No, width=20, bd=0, font='arial 23 bold', fg='#07531f',
                      state='disabled').place(x=615, y=120)

    Label(inputframe, text='Name:', font='arial 20 bold', fg='white', bg='#07531f').place(x=150, y=190)
    Name = StringVar()
    nameEntry = Entry(inputframe,textvariable=Name, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=190)


    Label(inputframe, text='Delivery (Kgs):', font='arial 20 bold', fg='white', bg='#07531f').place(x=150, y=260)
    addition = StringVar()
    newaddEntry = Entry(inputframe,textvariable=addition, width=20, bd=0, font='arial 23 bold', fg='#07531f').place(x=615, y=260)

    prof_frame = Frame(inputframe, bd=3, bg="white", width=925, height=100, relief=GROOVE)
    prof_frame.place(x=35, y=470)


    saveButton = Button(prof_frame, text='Save', width=10, font='arial 20 bold', fg='white', bg='lightblue', cursor='hand2', command=save2).place(
        x=25, y=20)
    resetButton = Button(prof_frame, text='Reset', width=10, font='arial 20 bold', fg='white', bg='#e96c6c',cursor='hand2', command=Clear()).place(
        x=260, y=20)
    printButton = Button(prof_frame, text='Print', width=10, font='arial 20 bold', fg='white', bg='darkblue', cursor='hand2').place(
        x=490, y=20)
    exitButton = Button(prof_frame, text='Exit', width=10, font='arial 20 bold', fg='white', bg='red',cursor='hand2').place(
        x=720, y=20)
    add_frame.pack(pady=20)
    add_frame.configure(width=1600, height=1150)


def members_page():
    membersdataframe = Frame(workingFrame, bg='#07531f')

    def load_data():
        # Connect to SQLite database
        conn = sqlite3.connect('member_data.db')
        cursor = conn.cursor()

        # Fetch data from the SQLite member_records table
        cursor.execute('SELECT * FROM member_records')
        rows = cursor.fetchall()

        # Define column names
        column_names = ['Top ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)']
        tv1['column'] = column_names
        tv1['show'] = 'headings'

        for column in column_names:
            tv1.heading(column, text=column)
            tv1.column(column, width=150)
            tv1.tag_configure(column, background='#07531f')

        # Insert rows into the Treeview
        for row in rows:
            tv1.insert('', 'end', values=row)

        # Close the database connection
        conn.close()

    def search_data():
        query = search.get()

        for item in tv1.get_children():
            values = tv1.item(item, 'values')
            if query == str(values[1]):  # Index 1 corresponds to the "Reg_No" column
                tv1.selection_add(item)
                tv1.see(item)  # Scroll to the matched item
            else:
                tv1.selection_remove(item)

    def cumulative():
        # Connect to the database
        conn = sqlite3.connect('members_data.db')
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS member_records (
                    top_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reg_no INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    topping_date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    amount_kgs REAL NOT NULL,
                    FOREIGN KEY(reg_no) REFERENCES members(reg_no)
                )
            ''')


        # Dictionary to store cumulative kilos for each farmer
        cumulative_data = {}

        # Fetch all records from the member_records table
        cursor.execute("SELECT top_id, reg_no, name, amount_kgs FROM member_records")
        rows = cursor.fetchall()

        for row in rows:
            top_id, reg_no, name, amount_kgs = row

            if reg_no in cumulative_data:
                cumulative_data[reg_no]['total_kilos'] += amount_kgs
            else:
                cumulative_data[reg_no] = {
                    'top_id': top_id,
                    'name': name,
                    'total_kilos': amount_kgs
                }

        # Print the cumulative data
        for reg_no, data in cumulative_data.items():
            print(f"Top ID: {data['top_id']}")
            print(f"Reg No: {reg_no}")
            print(f"Name: {data['name']}")
            print(f"Total Kilos: {data['total_kilos']}")
            print('-' * 50)

        # Close the connection
        conn.close()

    def copy_selected_row_data():
        selected_item = tv1.selection()

        if selected_item:
            item = tv1.item(selected_item)
            values = item['values']

            if values:
                Top_ID.set(str(values[0]))
                Reg_No.set(str(values[1]))
                Name.set(str(values[2]))
                Topping_Date.set(str(values[3]))
                Time.set(str(values[4]))
                Amount.set(str(values[5]))
            else:
                clear_variables()
        else:
            clear_variables()

    def clear_variables():
        Top_ID.set('')
        Reg_No.set('')
        Name.set('')
        Topping_Date.set('')
        Time.set('')
        Amount.set('')

    factoryframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S ADDITION", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)

    inputframe = Frame(workingFrame, bg='grey')
    inputframe.pack(fill=X, padx=10)
    inputframe.configure(width=990, height=1000)

    style = ttk.Style(inputframe)

    tv1 = ttk.Treeview(inputframe)
    style.configure('Treeview', background='#07531f', foreground='white', font='arial 13 bold', bordercolor='#07531f')
    style.configure('Treeview.Heading', font='arial 13 bold', foreground='#07531f')
    tv1.pack(side=LEFT, fill=BOTH, expand=TRUE)
    treescrolly = ttk.Scrollbar(inputframe, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side=LEFT, fill=Y)

    load_data()  # Load data from SQLite

    navigationFrame2 = Frame(inputframe, bg='grey')
    navigationFrame2.pack(side=RIGHT)
    navigationFrame2.configure(width=250, height=1000)

    search = StringVar()
    SearchEntry = Entry(navigationFrame2, textvariable=search, bd=0, width=17, font='arial 17 bold', fg='#07531f',
                        bg='white').place(x=10, y=10)

    Top_ID = StringVar()
    Reg_No = StringVar()
    Name = StringVar()
    Topping_Date = StringVar()
    Time = StringVar()
    Amount = StringVar()

    Button(navigationFrame2, text='Totals', bd=0, width=20, height=2, fg='white', bg='#07531f',
           activeforeground='white', activebackground='#07531f', command=cumulative).place(x=10, y=100)

    Button(navigationFrame2, text='Search', bd=0, width=20, height=2, fg='white', bg='#07531f',
           activeforeground='white', activebackground='#07531f', command=search_data).place(x=10, y=50)

    membersdataframe.pack(pady=20)
    membersdataframe.configure(width=1600, height=100)


def factory_page():

    def load_data():
        # Connect to SQLite database
        conn = sqlite3.connect('member_data.db')
        cursor = conn.cursor()

        # Fetch data from the SQLite members table
        cursor.execute('SELECT * FROM members')
        rows = cursor.fetchall()

        # Get column names from the table
        column_names = [description[0] for description in cursor.description]
        tv1['column'] = column_names
        tv1['show'] = 'headings'

        for column in column_names:
            tv1.heading(column, text=column)
            tv1.column(column, width=150)
            tv1.tag_configure(column, background='#07531f')

        # Insert rows into the Treeview
        for row in rows:
            tv1.insert('', 'end', values=row)

        # Close the database connection
        conn.close()

    def search_data():
        query = search.get().lower()

        for item in tv1.get_children():
            values = tv1.item(item, 'values')
            if query in str(values[1]).lower():  # Index 1 corresponds to the "Name" column
                tv1.selection_add(item)
                tv1.see(item)  # Scroll to the matched item
            else:
                tv1.selection_remove(item)

    # GUI Setup
    factoryframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S ADDITION", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)

    inputframe = Frame(workingFrame, bg='grey')
    inputframe.pack(fill=X, padx=10)
    inputframe.configure(width=990, height=1000)

    style = ttk.Style(inputframe)

    tv1 = ttk.Treeview(inputframe)
    style.configure('Treeview', background='#07531f', foreground='white', font='arial 13 bold', bordercolor='#07531f')
    style.configure('Treeview.Heading', font='arial 13 bold', foreground='#07531f')
    tv1.pack(side=LEFT, fill=BOTH, expand=TRUE)
    treescrolly = ttk.Scrollbar(inputframe, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.pack(side=LEFT, fill=Y)

    load_data()  # Load data from SQLite

    navigationFrame2 = Frame(inputframe, bg='grey')
    navigationFrame2.pack(side=RIGHT)
    navigationFrame2.configure(width=250, height=1000)

    search = StringVar()
    SearchEntry = Entry(navigationFrame2, textvariable=search, bd=0, width=17, font='arial 17 bold', fg='#07531f', bg='white').place(x=10, y=10)

    column_var = StringVar()
    column = ['Reg_No', 'Name', 'Reg_Date', 'National_ID', 'Bank', 'Account_No', 'Phone Number']
    column_dropdown = Combobox(navigationFrame2, textvariable=column_var, values=column)
    column_var.set('Select criteria')
    column_dropdown.place(x=10, y=100)

    Button(navigationFrame2, text='Search', bd=0, width=20, height=2, fg='white', bg='#07531f', activeforeground='white', activebackground='#07531f', command=search_data).place(x=10, y=50)

    factoryframe.pack(pady=20)
    factoryframe.configure(width=1600, height=1150)

def cumulative_page():
    # Initialize the frame for the cumulative data
    cumulative_frame = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="CUMULATIVE", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)
    cumulative_frame.pack(fill=BOTH, expand=True, padx=10)

    # Create a Treeview widget to display the cumulative data
    tree = ttk.Treeview(cumulative_frame, columns=('reg_no', 'name', 'phone', 'last_date', 'total_kilos'),
                        show='headings')
    tree.heading('reg_no', text='Reg No')
    tree.heading('name', text='Name')
    tree.heading('phone', text='Phone')
    tree.heading('last_date', text='Last Date of Delivery')
    tree.heading('total_kilos', text='Total Kilos')

    tree.column('reg_no', width=100)
    tree.column('name', width=200)
    tree.column('phone', width=150)
    tree.column('last_date', width=150)
    tree.column('total_kilos', width=100)

    # Add scrollbar
    scrollbar = Scrollbar(cumulative_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=LEFT, fill=Y)

    # Pack the treeview
    tree.pack(fill=BOTH, expand=TRUE)

    # Create another Treeview for detailed deliveries
    detail_tree = ttk.Treeview(cumulative_frame, columns=('top_id', 'topping_date', 'time', 'amount_kgs'),
                               show='headings')
    detail_tree.heading('top_id', text='Top ID')
    detail_tree.heading('topping_date', text='Topping Date')
    detail_tree.heading('time', text='Time')
    detail_tree.heading('amount_kgs', text='Amount (Kgs)')

    detail_tree.column('top_id', width=100)
    detail_tree.column('topping_date', width=150)
    detail_tree.column('time', width=100)
    detail_tree.column('amount_kgs', width=100)

    # Add scrollbar to detailed Treeview
    detail_scrollbar = Scrollbar(cumulative_frame, orient='vertical', command=detail_tree.yview)
    detail_tree.configure(yscrollcommand=detail_scrollbar.set)
    detail_scrollbar.pack(side=LEFT, fill=Y)

    # Pack the detailed Treeview
    detail_tree.pack(fill=BOTH, expand=TRUE)

    # Query the database and populate the main Treeview
    conn = sqlite3.connect('member_data.db')
    query = '''
        SELECT 
            m.reg_no,
            m.name,
            m.phone,
            MAX(r.topping_date) AS last_date,
            SUM(r.amount_kgs) AS total_kilos
        FROM members m
        LEFT JOIN member_records r ON m.reg_no = r.reg_no
        GROUP BY m.reg_no
        '''
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Insert data into the main Treeview
    for row in rows:
        tree.insert('', 'end', values=row)

    # Function to display detailed deliveries for the selected member
    def show_detailed_deliveries(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            reg_no = item['values'][0]  # Get the reg_no of the selected member

            # Clear the detailed Treeview
            detail_tree.delete(*detail_tree.get_children())

            # Query to get the detailed deliveries for the selected member
            detailed_query = '''
                SELECT top_id, topping_date, time, amount_kgs
                FROM member_records
                WHERE reg_no = ?
                ORDER BY topping_date ASC
                '''
            cursor.execute(detailed_query, (reg_no,))
            detailed_rows = cursor.fetchall()

            # Insert the detailed deliveries into the detailed Treeview
            for detailed_row in detailed_rows:
                detail_tree.insert('', 'end', values=detailed_row)

            # Calculate and display the total kilos at the bottom of the detailed Treeview
            total_kilos = sum(row[3] for row in detailed_rows)
            detail_tree.insert('', 'end', values=('Total', '', '', total_kilos))

    # Bind the selection event to the Treeview
    tree.bind('<<TreeviewSelect>>', show_detailed_deliveries)


def analytics_page():
    # Initialize window

    analyticsframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="ANALYTICS", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)

    analyticsframe.pack(fill=BOTH, expand=True, padx=10)

    # Create a frame for the plots
    plot_frame = ttk.Frame(analyticsframe)
    plot_frame.pack(fill=BOTH, expand=True)

    # Function to plot Member Growth
    def plot_member_growth():
        conn = sqlite3.connect('member_data.db')
        df = pd.read_sql_query("SELECT COUNT(*) AS members, reg_date FROM members GROUP BY reg_date", conn)
        conn.close()

        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df['reg_date'], df['members'], marker='o', color='green')
        ax.set_title("Member Growth Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Members")

        # Clear previous plot and display new plot
        for widget in plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    # Function to plot Kilo Trends
    def plot_kilo_trends(period='daily'):
        conn = sqlite3.connect('member_data.db')
        if period == 'daily':
            query = "SELECT SUM(amount_kgs) AS total_kgs, topping_date FROM member_records GROUP BY topping_date"
        elif period == 'monthly':
            query = "SELECT SUM(amount_kgs) AS total_kgs, strftime('%Y-%m', topping_date) AS month FROM member_records GROUP BY month"
        elif period == 'yearly':
            query = "SELECT SUM(amount_kgs) AS total_kgs, strftime('%Y', topping_date) AS year FROM member_records GROUP BY year"

        df = pd.read_sql_query(query, conn)
        conn.close()

        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df.iloc[:, 1], df['total_kgs'], marker='o', color='blue')
        ax.set_title(f"Kilo Trends ({period.capitalize()})")
        ax.set_xlabel(period.capitalize())
        ax.set_ylabel("Total Kilos")

        # Clear previous plot and display new plot
        for widget in plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    # Create buttons to trigger the plots

    # GUI Setup
    button_frame = ttk.Frame(analyticsframe)
    button_frame.pack(side=BOTTOM, fill=BOTH)

    Button(button_frame, text="Member Growth", bd=0, width=20, height=3, fg='white', bg='#07531f', activeforeground='white', activebackground='#07531f', command=plot_member_growth).pack(side=LEFT, padx=10, pady=10)
    Button(button_frame, text="Daily Kilo Trends", bd=0, width=20, height=3, fg='white', bg='#07531f', activeforeground='white', activebackground='#07531f', command=lambda: plot_kilo_trends('daily')).pack(side=LEFT,
                                                                                                       padx=10, pady=10)
    Button(button_frame, text="Monthly Kilo Trends", bd=0, width=20, height=3, fg='white', bg='#07531f', activeforeground='white', activebackground='#07531f', command=lambda: plot_kilo_trends('monthly')).pack(side=LEFT,
                                                                                                           padx=10,
                                                                                                           pady=10)
    Button(button_frame, text="Yearly Kilo Trends", bd=0, width=20, height=3, fg='white', bg='#07531f', activeforeground='white', activebackground='#07531f', command=lambda: plot_kilo_trends('yearly')).pack(side=LEFT,
                                                                                                         padx=10,
                                                                                                         pady=10)


    plot_member_growth()

def hide_indicators():
    home_indicate.config(bg='#c3c3c3')
    menu_indicate.config(bg='#c3c3c3')
    contact_indicate.config(bg='#c3c3c3')
    about_indicate.config(bg='#c3c3c3')
    cumulative_indicate.config(bg='#c3c3c3')
    analytics_indicate.config(bg='#c3c3c3')


def delete_pages():
    for frame in workingFrame .winfo_children():
        frame.destroy()


def indicate(lb, page):
    hide_indicators()
    lb.config(bg='#07531f')
    delete_pages()
    page()


def theme():
    # Determine the base path depending on whether we're running as a script or as a bundled executable
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # Construct the full path to the image
    darkmode_image_path = os.path.join(base_path, 'images/darkmode.png')

    # Update the image configuration
    img2.config(file=darkmode_image_path)
    themeButton.config(activebackground='black',bg='black', command=light)
    navigationFrame.config(bg='black')
    logo.config(bg='black')
    register_btn.config(fg='black')
    menu_btn.config(fg='black')
    contact_btn.config(fg='black')
    about_btn.config(fg='black')
    cumulative_btn.config(fg='black')
    analytics_btn.config(fg='black')





def light():
    # Determine the base path depending on whether we're running as a script or as a bundled executable
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # Construct the full path to the image
    lightmode_image_path = os.path.join(base_path, 'images/lightmode.png')

    # Update the image configuration
    img2.config(file=lightmode_image_path)

    themeButton.config(activebackground='white', bg='white', command=theme)
    navigationFrame.config(bg='white')
    logo.config(bg='white')
    register_btn.config(fg='#07531f')
    menu_btn.config(fg='#07531f')
    contact_btn.config(fg='#07531f')
    about_btn.config(fg='#07531f')
    cumulative_btn.config(fg='#07531f')
    analytics_btn.config(fg='#07531f')
def hidebutton():
    navigationFrame.configure(width=0)
    hideButton.place(x=5, y=2)
    hideButton.config(text='UNHIDE MENU', bg='white', fg='#07531f')
    hideButton.config(command=unhidebutton)

def unhidebutton():
    navigationFrame.configure(width=400)
    hideButton.config(text='HIDE MENU', bg='#07531f', fg='white')
    hideButton.place(x = 275, y = 2)
    hideButton.config(command=hidebutton)

def opening():
    hideButton.config(text='', bg='#07531f', fg='#07531f')
    hideButton.config(command=hidebutton)



def sign_up():
    loginframe.configure(width=0)
    sign_upframe.configure(width=987)
    forgotframe.configure(width=0)

def forgot_password():
    sign_upframe.configure(width=0)
    loginframe.configure(width=0)
    forgotframe.configure(width=987)

def login():
    if usernameEntry.get()=='' or passwordEntry.get()== '':
        messagebox.showerror('Error', 'Enter your username and password')

bgcolor = 'white'
welcomeframe = Frame(mainframe, bg='#07531f', width=300, height=3000)
welcomeframe.pack(side=LEFT)
welcomeframe.pack_propagate(False)
welcomeframe.configure(width=2000, height=1300)
# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image4_path = os.path.join(base_path, 'images/logo.png')

# Load the image
img4 = PhotoImage(file=image4_path)
lbl = Label(welcomeframe, bg="#07531f", image=img4)
lbl.pack(pady=60)
userframe = Frame(welcomeframe,bg='#07531f', highlightbackground='white', highlightthickness=4)
userframe.pack(pady=10)
userframe.configure(width=987, height=500)
loginframe = Frame(userframe,bg='#07531f')
loginframe.pack(side=LEFT)
loginframe.configure(width=987, height=500)


heading = Label(loginframe, text="USERLOGIN", font=('Microsoft Yahei UI Light', 25, 'bold'), bg='#07531f',
                fg='white')
heading.place(x=400, y=25)

usernameEntry = Entry(loginframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="white",
                      bg='#07531f')
usernameEntry.place(x=250, y=130)
usernameEntry.insert('0', 'Username')

#usernameEntry.bind('<FocusIn>', user_enter)

frame1=Frame(loginframe, width=480, height=4, bg='white')
frame1.place(x=250, y=170)

passwordEntry = Entry(loginframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="white",
                      bg='#07531f')
passwordEntry.place(x=250, y=210)
passwordEntry.insert('0', 'Password')

#passwordEntry.bind('<FocusIn>', password_enter)
frame2=Frame(loginframe, width=480, height=4, bg='white')
frame2.place(x=250, y=247)


# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')

# Load the image
openeye = PhotoImage(file=image_path)
eyeButton=Button(loginframe, image=openeye, activebackground='#07531f',activeforeground='#07531f',bd=0, bg='#07531f',cursor='hand2')#, command=hide)
eyeButton.place(x=702, y=215)

forgotButton=Button(loginframe, text="Forgot password. Click here?", font=('Open Sans', 16, 'bold'), activebackground='#07531f',activeforeground='white',bd=0, bg='#07531f',cursor='hand2',fg='white',command=forgot_password)
forgotButton.place(x=250, y=290)

loginButton=Button(loginframe, text="Login", bg="white", width=15,bd=0, height=1, font=('Open Sans', 23, 'bold'), fg="#07531f", activebackground="white", activeforeground="#07531f", command=welcome)
loginButton.place(x=350, y=360)

registerLabel = Label(loginframe, text="Not registered?", font=('Microsoft Yahei UI Light', 16, 'bold'), bg='#07531f',
                fg='white')
registerLabel.place(x=250, y=450)
registerButton=Button(loginframe, text="Create an account", font=('Open Sans', 16, 'bold underline'), activebackground='#07531f',activeforeground='white',bd=0, bg='#07531f',cursor='hand2',fg='white',command= sign_up)
registerButton.place(x=420, y=450)


def authentication_page():
    sign_upframe.configure(width=0)
    loginframe.configure(width=987)
    forgotframe.configure(width=0)

sign_upframe = Frame(userframe,bg='#890a0a')
sign_upframe.pack(side=LEFT)
sign_upframe.configure(width=0, height=500)
heading = Label(sign_upframe, text="SIGN UP", font=('Microsoft Yahei UI Light', 25, 'bold'), bg='#890a0a',
                fg='white')
heading.place(x=400, y=25)

Label(sign_upframe, text='Email:', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#890a0a', fg='white').place(x=70, y=80)
EmailEntry = Entry(sign_upframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#07531f",
                      bg='white')
EmailEntry.place(x=250, y=80)


#usernameEntry.bind('<FocusIn>', user_enter)

Label(sign_upframe, text='Username:', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#890a0a', fg='white').place(x=70, y=150)
usernameEntry = Entry(sign_upframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#07531f",
                      bg='white')
usernameEntry.place(x=250, y=150)

Label(sign_upframe, text='Password:', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#890a0a', fg='white').place(x=70, y=220)
passwordEntry = Entry(sign_upframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#07531f",
                      bg='white')
passwordEntry.place(x=250, y=220)

#passwordEntry.bind('<FocusIn>', password_enter)

# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')

# Load the image
openeye1 = PhotoImage(file=image_path)
eyeButton=Button(sign_upframe, image=openeye1, activebackground='white',activeforeground='white',bd=0, bg='white',cursor='hand2')#, command=hide)
eyeButton.place(x=702, y=220)

Label(sign_upframe, text='Confirm:', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#890a0a', fg='white').place(x=70, y=290)
passwordEntry = Entry(sign_upframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#890a0a",
                      bg='white')
passwordEntry.place(x=250, y=290)

#passwordEntry.bind('<FocusIn>', password_enter)

# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')

# Load the image
openeye2 = PhotoImage(file=image_path)
eyeButton=Button(sign_upframe, image=openeye2, activebackground='white',activeforeground='white',bd=0, bg='white',cursor='hand2')#, command=hide)
eyeButton.place(x=702, y=290)

check=IntVar()
conCheck= Checkbutton(sign_upframe, font=('Open Sans', 16, 'bold'),
                      bg='#890a0a', fg='#890a0a', activebackground='#890a0a', activeforeground='white', cursor='hand2', variable=check)
conCheck.place(x=70, y=350)
checklabel= Label(sign_upframe, text="Please agree to our terms & conditions", font=('Open Sans', 16, 'bold'), bd=0, bg='#890a0a', fg='white', activebackground='#890a0a', activeforeground='white', cursor='hand2')
checklabel.place(x=100, y=355)


sign_upButton=Button(sign_upframe, text="Sign Up", bg="white", width=15,bd=0, height=1, font=('Open Sans', 18, 'bold'), fg="#890a0a", activebackground="white", activeforeground="#890a0a")
sign_upButton.place(x=340, y=385)

registerLabel = Label(sign_upframe, text="Already have an account?", font=('Microsoft Yahei UI Light', 16, 'bold'), bg='#890a0a',
                fg='white')
registerLabel.place(x=230, y=450)
loginButton2=Button(sign_upframe, text="Login", font=('Open Sans', 16, 'bold underline'), activebackground='#890a0a',activeforeground='white',bd=0, bg='#890a0a',cursor='hand2',fg='white',command= authentication_page)
loginButton2.place(x=500, y=450)



##################forgot password window################################
forgotframe = Frame(userframe,bg='#c7ab0d')
forgotframe.pack(side=LEFT)
forgotframe.configure(width=0, height=500)

heading = Label(forgotframe, text="RETRIEVE PASSWORD", font=('Microsoft Yahei UI Light', 25, 'bold'), bg='#c7ab0d',
                fg='white')
heading.place(x=320, y=25)

Label(forgotframe, text='Username', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#c7ab0d', fg='white').place(x=246, y=80)
fusernameEntry = Entry(forgotframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#c7ab0d",
                      bg='white')
fusernameEntry.place(x=250, y=120)


#usernameEntry.bind('<FocusIn>', user_enter)


Label(forgotframe, text='Password', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#c7ab0d', fg='white').place(x=246, y=170)
fpasswordEntry = Entry(forgotframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#c7ab0d",
                      bg='white')
fpasswordEntry.place(x=250, y=220)

#passwordEntry.bind('<FocusIn>', password_enter)

# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')

# Load the image
openeye3 = PhotoImage(file=image_path)
eyeButton=Button(forgotframe, image=openeye3, activebackground='white',activeforeground='white',bd=0, bg='white',cursor='hand2')#, command=hide)
eyeButton.place(x=702, y=220)

Label(forgotframe, text='Confirm Password', font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#c7ab0d', fg='white').place(x=246, y=270)
passwordEntry = Entry(forgotframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0, fg="#c7ab0d",
                      bg='white')
passwordEntry.place(x=250, y=320)

#passwordEntry.bind('<FocusIn>', password_enter)

# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')

# Load the image
openeye4 = PhotoImage(file=image_path)
eyeButton=Button(forgotframe, image=openeye4, activebackground='white',activeforeground='white',bd=0, bg='white',cursor='hand2')#, command=hide)
eyeButton.place(x=702, y=320)





changeButton=Button(forgotframe, text="Change password", bg="white", width=15,bd=0, height=1, font=('Open Sans', 18, 'bold'), fg="#c7ab0d", activebackground="white", activeforeground="#c7ab0d", command=authentication_page)
changeButton.place(x=340, y=385)









navigationFrame = Frame(mainframe, bd=2, bg='white')

navigationFrame.pack(side=LEFT)
navigationFrame.pack_propagate(False)
navigationFrame.configure(width=400, height=1150)

# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
logo_path = os.path.join(base_path, 'images/logo.png')

# Load the image
logoimage = PhotoImage(file=logo_path)
logo = Label(navigationFrame, bg="white", image=logoimage)
logo.place(x=70, y=40)

register_btn = Button(navigationFrame, width=20, height=2, text='REGISTER', font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(home_indicate, homepage))
register_btn.place(x=20, y=260)

home_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
home_indicate.place(x=0, y=260, width=20, height=98)

menu_btn = Button(navigationFrame, width=20, height=2, text='DELIVERY', font='arial 24 bold', fg='#07531f', bd=0, activebackground='#c3c3c3', bg='#c3c3c3', command=lambda : indicate(menu_indicate, add_page))
menu_btn.place(x=20, y=362)

menu_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
menu_indicate.place(x=0, y=362, width=20, height=98)

contact_btn = Button(navigationFrame, width=20, height=2, text="DELIVERY RECORDS", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(contact_indicate, members_page))
contact_btn.place(x=20, y=464)

contact_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
contact_indicate.place(x=0, y=464, width=20, height=98)

about_btn = Button(navigationFrame, width=20, height=2, text="MEMBER'S LIST", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(about_indicate, factory_page))
about_btn.place(x=20, y=566)

about_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
about_indicate.place(x=0, y=566, width=20, height=98)

cumulative_btn = Button(navigationFrame, width=20, height=2, text="CUMULATIVE", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(cumulative_indicate, cumulative_page))
cumulative_btn.place(x=20, y=668)

cumulative_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
cumulative_indicate.place(x=0, y=668, width=20, height=98)

analytics_btn = Button(navigationFrame, width=20, height=2, text="ANALYTICS", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(analytics_indicate, analytics_page))
analytics_btn.place(x=20, y=770)

analytics_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
analytics_indicate.place(x=0, y=770, width=20, height=98)


# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
lightmode_path = os.path.join(base_path, 'images/lightmode.png')

# Load the image
img2 = PhotoImage(file=lightmode_path)
themeButton = Button(navigationFrame, bd=0, bg="white", image=img2, activebackground='white', anchor='w', command=theme)
themeButton.pack(side=BOTTOM, fill=X)

workingFrame = Frame(mainframe, bg='#07531f')

workingFrame.pack(fill=BOTH, expand=TRUE)
workingFrame.pack_propagate(False)
workingFrame.configure(width=1600, height=1500)



hideButton = Button(mainframe,text='', bg='#07531f', fg='#07531f', font='arial 15 bold',bd=0, command=hidebutton)
hideButton.place(x=275, y=2)




mainframe.mainloop()