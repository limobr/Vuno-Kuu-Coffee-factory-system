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
import bcrypt
import matplotlib.dates as mdates
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import win32print
import win32api
from fpdf import FPDF


import pandas as pd


mainframe = Tk()
mainframe.geometry('1700x950+50+50')
mainframe.title('Vuno Kuu System')

conn = sqlite3.connect('member_data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
-- Create members table
CREATE TABLE IF NOT EXISTS members (
    reg_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    reg_date TEXT NOT NULL,
    national_id TEXT DEFAULT 'N/A',
    bank TEXT DEFAULT 'N/A',
    account_no TEXT DEFAULT 'N/A',
    phone TEXT NOT NULL
);
''')
cursor.execute('''
-- Create user_registry table
CREATE TABLE IF NOT EXISTS user_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- encrypted password
    usertype TEXT CHECK(usertype IN ('admin', 'clerk')) NOT NULL, -- 'admin' or 'clerk'
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    id_number TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    quitting_date TEXT, -- Optional
    date_added TEXT NOT NULL
);
''')
cursor.execute('''
-- Create transactions table with separate date and time fields
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_reg_no INTEGER NOT NULL,
    buyer_reg_no INTEGER NOT NULL,
    amount_kgs REAL NOT NULL,
    transaction_date TEXT NOT NULL,  -- Stores the date (YYYY-MM-DD format)
    transaction_time TEXT NOT NULL,  -- Stores the time (HH:MM:SS format)
    clerk TEXT NOT NULL,
    FOREIGN KEY (seller_reg_no) REFERENCES members (reg_no),
    FOREIGN KEY (buyer_reg_no) REFERENCES members (reg_no),
    FOREIGN KEY (clerk) REFERENCES user_registry (username)
);

''')
cursor.execute('''
-- Create member_records table
CREATE TABLE IF NOT EXISTS member_records (
    top_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_no INTEGER NOT NULL,
    name TEXT NOT NULL,
    topping_date TEXT NOT NULL,
    time TEXT NOT NULL,
    amount_kgs REAL NOT NULL,
    clerk TEXT NOT NULL, -- Automatically filled with logged-in clerk
    FOREIGN KEY (reg_no) REFERENCES members (reg_no),
    FOREIGN KEY (clerk) REFERENCES user_registry (username)
);

''')
cursor.execute('''
-- Create mbuni table
CREATE TABLE IF NOT EXISTS mbuni (
    top_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_no INTEGER NOT NULL,
    name TEXT NOT NULL,
    topping_date TEXT NOT NULL,
    time TEXT NOT NULL,
    amount_kgs REAL NOT NULL,
    clerk TEXT NOT NULL, -- Automatically filled with logged-in clerk
    FOREIGN KEY (reg_no) REFERENCES members (reg_no),
    FOREIGN KEY (clerk) REFERENCES user_registry (username)
);

''')

# Commit changes and close the connection
conn.commit()


def welcome():
    welcomeframe.destroy()
    navigationFrame.configure(width=400)
    hideButton.config(text='HIDE MENU', bg='#07531f', fg='white')
    hideButton.place(x=275, y=2)
    hideButton.config(command=hidebutton)

def clerkpage():

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)

    homeframe= Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com",font='arial 12 italic', width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="CLERK REGISTRATION", width=10, height=2, bg="#07531f", fg='#fff', font='arial 25 bold underline').pack(
        side=TOP, fill=X, pady=60, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    inputframe = Frame(workingFrame, bg='#07531f')
    inputframe.pack(pady=10)
    inputframe.configure(width=990, height=1000)

    # First Name Input
    first_name_label = Label(inputframe, text="First Name", font=('Arial', 14), bg='#07531f', fg='white')
    first_name_label.grid(row=0, column=0, pady=10, padx=10)
    first_name_entry = Entry(inputframe, width=30, font=('Arial', 14))
    first_name_entry.grid(row=0, column=1, pady=10, padx=10)

    # Last Name Input
    last_name_label = Label(inputframe, text="Last Name", font=('Arial', 14), bg='#07531f', fg='white')
    last_name_label.grid(row=1, column=0, pady=10, padx=10)
    last_name_entry = Entry(inputframe, width=30, font=('Arial', 14))
    last_name_entry.grid(row=1, column=1, pady=10, padx=10)

    # Username Input
    username_label = Label(inputframe, text="Username", font=('Arial', 14), bg='#07531f', fg='white')
    username_label.grid(row=2, column=0, pady=10, padx=10)
    username_entry = Entry(inputframe, width=30, font=('Arial', 14))
    username_entry.grid(row=2, column=1, pady=10, padx=10)

    # Password Input
    password_label = Label(inputframe, text="Password", font=('Arial', 14), bg='#07531f', fg='white')
    password_label.grid(row=3, column=0, pady=10, padx=10)
    password_entry = Entry(inputframe, width=30, font=('Arial', 14), show='*')
    password_entry.grid(row=3, column=1, pady=10, padx=10)

    # ID Number Input
    id_number_label = Label(inputframe, text="ID Number", font=('Arial', 14), bg='#07531f', fg='white')
    id_number_label.grid(row=4, column=0, pady=10, padx=10)
    id_number_entry = Entry(inputframe, width=30, font=('Arial', 14))
    id_number_entry.grid(row=4, column=1, pady=10, padx=10)

    # Phone Number Input
    phone_number_label = Label(inputframe, text="Phone Number", font=('Arial', 14), bg='#07531f', fg='white')
    phone_number_label.grid(row=5, column=0, pady=10, padx=10)
    phone_number_entry = Entry(inputframe, width=30, font=('Arial', 14))
    phone_number_entry.grid(row=5, column=1, pady=10, padx=10)

    # Add Clerk Button
    add_clerk_btn = Button(inputframe, text="Add Clerk", font=('Arial', 20, 'bold'), bg='white', fg='#07531f', 
                        width=20, command=lambda: add_clerk(
                            first_name_entry.get(),
                            last_name_entry.get(),
                            username_entry.get(),
                            password_entry.get(),
                            id_number_entry.get(),
                            phone_number_entry.get()
                        ))
    add_clerk_btn.grid(row=7, column=0, columnspan=2, pady=20)

    # Function to handle adding the clerk to the database
    def add_clerk(first_name, last_name, username, password, id_number, phone_number):
        conn = sqlite3.connect('member_data.db')
        cursor = conn.cursor()

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute("""
                INSERT INTO user_registry (username, password, usertype, id_number, phone_number, date_added, first_name, last_name)
                VALUES (?, ?, ?, ?, ?, date('now'), ?, ?)
            """, (username, hashed_password, 'clerk', id_number, phone_number, first_name, last_name))
            
            conn.commit()
            
            # Display success message using messagebox
            messagebox.showinfo("Success", f"Clerk {first_name} has been added successfully!")
            
            # Clear the input fields after successful addition
            first_name_entry.delete(0, 'end')
            last_name_entry.delete(0, 'end')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            id_number_entry.delete(0, 'end')
            phone_number_entry.delete(0, 'end')

        except sqlite3.IntegrityError:
            # Show error message if the username already exists
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
        finally:
            conn.close()

    







    homeframe.pack(pady=20)
    homeframe.configure(width=1600, height=1150)

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

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)


    homeframe= Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com",font='arial 12 italic', width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER REGISTRATION", width=10, height=2, bg="#07531f", fg='#fff', font='arial 25 bold underline').pack(
        side=TOP, fill=X, pady=60, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

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


def viewclerks():

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)
    add_frame = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S DELIVERY", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(
        side=TOP, fill=X, pady=60, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    inputframe = Frame(workingFrame, bg='#07531f')
    inputframe.pack(pady=10)
    inputframe.configure(width=990, height=1000)
    # Clear input frame first
    for widget in inputframe.winfo_children():
        widget.destroy()

    # Create treeview to display clerks
    columns = ('first_name', 'last_name', 'username', 'phone_number', 'date_added', 'quitting_date')
    tree = ttk.Treeview(inputframe, columns=columns, show='headings', height=10)
    
    # Define column headings
    tree.heading('first_name', text='First Name')
    tree.heading('last_name', text='Last Name')
    tree.heading('username', text='Username')
    tree.heading('phone_number', text='Phone Number')
    tree.heading('date_added', text='Date Added')
    tree.heading('quitting_date', text='Quitting Date')

    # Define column widths
    tree.column('first_name', width=100)
    tree.column('last_name', width=100)
    tree.column('username', width=100)
    tree.column('phone_number', width=120)
    tree.column('date_added', width=100)
    tree.column('quitting_date', width=120)

    # Fetch clerks from database
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, username, phone_number, date_added, quitting_date FROM user_registry WHERE usertype = 'clerk'")
    clerks = cursor.fetchall()
    conn.close()

    # Insert data into treeview
    for clerk in clerks:
        tree.insert('', 'end', values=clerk)

    tree.pack(pady=20)

    # Label to show selection
    selected_label = Label(inputframe, text="Select a clerk to quit", font=('Arial', 12))
    selected_label.pack(pady=10)

    # Quit Clerk button (disabled by default)
    quit_btn = Button(inputframe, text="Quit Clerk", state=DISABLED, command=lambda: quit_clerk(tree))
    quit_btn.pack(pady=10)

    # Function to enable the Quit button when a row is selected
    def on_row_select(event):
        selected_item = tree.selection()
        if selected_item:
            quit_btn.config(state=NORMAL)

    # Bind row selection event
    tree.bind('<<TreeviewSelect>>', on_row_select)

def quit_clerk(tree):
    # Get selected row
    selected_item = tree.selection()[0]
    selected_values = tree.item(selected_item, 'values')

    username = selected_values[2]  # Username from selected row

    # Update quitting_date in database
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user_registry SET quitting_date = date('now') WHERE username = ?", (username,))
    conn.commit()
    conn.close()

    # Update quitting_date in the treeview
    tree.set(selected_item, column='quitting_date', value='Today')

    # Disable the button after quitting
    quit_btn.config(state=DISABLED)

    messagebox.showinfo('Success', f"Clerk {username} has been quitted successfully.")

    
    add_frame.pack(pady=20)
    add_frame.configure(width=1600, height=1150)


def add_page(logged_in_clerk):

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()

    def Top_ID():
        cursor.execute('SELECT MAX(top_id) FROM member_records')
        max_row_value = cursor.fetchone()[0]
        Topping_ID.set(max_row_value + 1 if max_row_value is not None else 1)

    def Clear():
        search.set('')
        Name.set('')
        addition.set('')
        Reg_No.set('')
        Total.set('')
        transfer.set('')
        Recipient_Name.set('')
        recipient_search.set('')
        Recipient_Reg_No.set('')
        transfer.set('')
        seller_search.set('')
        Seller_Reg_No.set('')
        Seller_Name.set('')
        Total_Seller.set('')
        M_search.set('')
        M_Topping_ID.set('')
        M_Reg_No.set('')
        M_Name.set('')
        M_addition.set('')
        total_members.set('')


    def search3():
        text = search.get()

        if text == '':
            messagebox.showerror('Search', 'Enter the member number')
        else:
            # Search for member's details
            cursor.execute('SELECT reg_no, name FROM members WHERE reg_no = ?', (text,))
            result = cursor.fetchone()

            if result:
                Reg_No.set(result[0])
                Name.set(result[1])

                query = '''
                    SELECT 
                        (COALESCE(SUM(r.amount_kgs), 0) - 
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.seller_reg_no = m.reg_no), 0) +
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.buyer_reg_no = m.reg_no), 0)
                        ) AS total_kilos
                    FROM members m
                    LEFT JOIN member_records r ON m.reg_no = r.reg_no
                    WHERE m.reg_no = ?
                    GROUP BY m.reg_no
                '''
                
                # Execute the query
                cursor.execute(query, (text,))
                total_result = cursor.fetchone()

                if total_result:
                    total_members.set(total_result[0])
                else:
                    total_members.set(0)
                
                # Calculate the total kilos delivered by this member
                cursor.execute('SELECT SUM(amount_kgs) FROM member_records WHERE reg_no = ?', (text,))
                total_kgs_result = cursor.fetchone()[0]
                total_kgs = total_kgs_result if total_kgs_result is not None else 0
                
                # Update the total kilos field (convert float to string)
                Total.set(str(total_kgs))
            else:
                Clear()
                messagebox.showerror('Invalid', 'Registration number not found')




    def print_receipt(reg_no, name, delivery_kgs, clerk, date, time):
        # Query to calculate total kilos for the member
        query = '''
            SELECT 
                (COALESCE(SUM(r.amount_kgs), 0) - 
                COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.seller_reg_no = m.reg_no), 0) +
                COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.buyer_reg_no = m.reg_no), 0)
                ) AS total_kilos
            FROM members m
            LEFT JOIN member_records r ON m.reg_no = r.reg_no
            WHERE m.reg_no = ?
            GROUP BY m.reg_no
        '''
        
        # Execute the query
        cursor.execute(query, (reg_no,))
        result = cursor.fetchone()
        total_kilos = result[0] if result else 0  # Default to 0 if no record found

        # Fetch the latest top_id from the member_records table
        cursor.execute("SELECT top_id FROM member_records ORDER BY top_id DESC LIMIT 1")
        latest_top_id_record = cursor.fetchone()

        # Check if the fetched record is not None
        if latest_top_id_record:
            latest_top_id = latest_top_id_record[0]
        else:
            latest_top_id = "N/A"  # Handle the case when no record exists
        
        # Close the database connection
        conn.close()

        # Ensure the date is formatted correctly (replace '/' with '-')
        formatted_date = date.replace("/", "-")

        # Parse the month from the formatted date (assuming 'YYYY-MM-DD' format)
        month = formatted_date.split('-')[1]  # Extracts the month as a string, e.g., '10'
        month_folder = f"m{int(month)}"  # Converts it to 'm1', 'm2', etc.

        # Define the directory path
        base_dir = "cherry"
        month_dir = os.path.join(base_dir, month_folder)
        
        # Create directories if they don't exist
        os.makedirs(month_dir, exist_ok=True)

        # Convert time to 12-hour format (handle cases where seconds are included)
        try:
            formatted_time = datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

        
        # Set up the filename using the actual values, ensuring all parts are strings
        receipt_file = f"receipt_{latest_top_id}_{reg_no}_{formatted_date}.pdf"
        receipt_path = os.path.join(month_dir, receipt_file)

        c = canvas.Canvas(receipt_path, pagesize=letter)

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, 740, "VUNO KUU COFFEE FACTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 720, "P.O BOX 209, KERICHO")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 700, "CHERRY RECEIPT")
        
        # Create space for the receipt details
        c.drawString(50, 690, "")  # Create space
        c.setFont("Helvetica-Bold", 10)
        
        # Receipt Details
        receipt_details = [
            f"REG ID: {reg_no}      NAME: {name}      DATE: {formatted_date} {formatted_time}",
            "-" * 100,
            f"TOP ID: {'-' * 71} {latest_top_id}",
            f"AMOUNT KGS: {'-' * 60} {delivery_kgs}kgs",
            f"TOTAL KGS: {'-' * 63} {total_kilos}kgs",
            f"SERVED BY: {'-' * 62} {clerk}",
            "-" * 100,
        ]


        y_position = 680  # Starting position for receipt details

        for detail in receipt_details:
            c.drawString(50, y_position, detail)
            y_position -= 20  # Move down for next line

        # Save and close PDF
        c.showPage()
        c.save()

        # Automatically open the PDF for printing (platform-dependent)
        if os.name == 'nt':  # For Windows
            os.startfile(receipt_file, "print")
        elif os.name == 'posix':  # For Linux or Mac
            os.system(f"lp {receipt_file}")

        messagebox.showinfo("Info", f"Receipt for {name} generated and sent to printer.")


    def save_delivery():
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
            INSERT INTO member_records (reg_no, name, topping_date, time, amount_kgs, clerk)
            VALUES (?, ?, ?, ?, ?, ?)''', (R1, N1, TD, TT, A1, logged_in_clerk))
            conn.commit()
            messagebox.showinfo("Info", "Record saved successfully!")
            Clear()
            Top_ID()

            # Call the print_receipt function to generate and print the receipt
            print_receipt(R1, N1, A1, logged_in_clerk, TD, TT)

    def search_member(search_entry, reg_no_var, name_var):
        reg_no = search_entry.get()
        if reg_no:
            cursor.execute("SELECT * FROM members WHERE Reg_No = ?", (reg_no,))
            member = cursor.fetchone()
            if member:
                reg_no_var.set(member[0])  # Set the registration number
                name_var.set(member[1])    # Set the name
                
                # Only calculate total kilos if this is for the seller
                if reg_no_var == Seller_Reg_No:
                    # Fetch total kilos delivered by the member
                    cursor.execute("SELECT SUM(amount_kgs) FROM member_records WHERE reg_no = ?", (reg_no,))
                    delivered_kilos = cursor.fetchone()[0] or 0
                    
                    # Fetch total kilos transferred by the member
                    cursor.execute("SELECT SUM(amount_kgs) FROM transactions WHERE seller_reg_no = ?", (reg_no,))
                    transferred_kilos = cursor.fetchone()[0] or 0

                    # Fetch total kilos received by the member
                    cursor.execute("SELECT SUM(amount_kgs) FROM transactions WHERE buyer_reg_no = ?", (reg_no,))
                    received_kilos = cursor.fetchone()[0] or 0

                    # Calculate the total kilos
                    total_kgs = delivered_kilos - transferred_kilos + received_kilos

                    # Debug print statements
                    print(f"Delivered Kilos for Member {reg_no}: {delivered_kilos}")
                    print(f"Transferred Kilos for Member {reg_no}: {transferred_kilos}")
                    print(f"Received Kilos for Member {reg_no}: {received_kilos}")
                    print(f"Total Kilos for Member {reg_no}: {total_kgs}")

                    # Set the total for the seller
                    Total_Seller.set(total_kgs)

            else:
                messagebox.showerror("Error", "Member not found")
        else:
            messagebox.showerror("Error", "Please enter a registration number")


    def print_transfer_receipt(seller_reg_no, seller_name, seller_total_kilos, transfer_amount, buyer_reg_no, buyer_name, clerk, date, time):
        # Fetch the latest transaction ID
        cursor.execute("SELECT transaction_id FROM transactions ORDER BY transaction_id DESC LIMIT 1")
        latest_transaction_record = cursor.fetchone()
        
        # Check if the fetched record is not None
        if latest_transaction_record:
            latest_transaction_id = latest_transaction_record[0]
        else:
            latest_transaction_id = "N/A"  # Handle the case when no record exists

        # Format the date and time
        formatted_date = date.replace("/", "-")

        try:
            formatted_time = datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

        # Define the directory path
        base_dir = "transactions"
        month_folder = f"m{int(formatted_date.split('-')[1])}"  # Extract and convert month to 'm1', 'm2', etc.
        month_dir = os.path.join(base_dir, month_folder)
        os.makedirs(month_dir, exist_ok=True)

        # Set up the filename using the transaction details
        receipt_file = f"transfer_receipt_{latest_transaction_id}_{seller_reg_no}_{formatted_date}.pdf"
        receipt_path = os.path.join(month_dir, receipt_file)
        try:
            # Get the default printer
            printer_name = win32print.GetDefaultPrinter()
            if not printer_name:
                raise Exception("No printer found")

            # Send the PDF directly to the default printer
            win32api.ShellExecute(
                0,
                "print",
                receipt_path,
                None,
                ".",
                0
            )
        except Exception as e:
            # Handle cases where no printer is available or any other error occurs
            messagebox.showerror("Print Error", str(e))

        # Generate the PDF
        c = canvas.Canvas(receipt_path, pagesize=letter)

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, 740, "VUNO KUU COFFEE FACTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 720, "P.O BOX 209, KERICHO")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 700, "TRANSACTION RECEIPT")

        # Create space for the receipt details
        c.drawString(50, 690, "")  

        c.setFont("Helvetica-Bold", 10)

        # Receipt Details
        receipt_details = [
            f"SELLER REG ID: {seller_reg_no}      NAME: {seller_name}      DATE: {formatted_date} {formatted_time}",
            "-" * 113,
            f"TRANSACTION ID: {'-' * 60} {latest_transaction_id}",
            f"TRANSFER AMOUNT: {'-' * 56} {transfer_amount}kgs",
            f"NEW TOTAL KGS: {'-' * 56} {seller_total_kilos}kgs",
            f"RECIPIENT REG ID: {'-' * 59} {buyer_reg_no}",
            f"NAME: {'-' * 75} {buyer_name}",
            f"SERVED BY: {'-' * 69} {clerk}",
            "-" * 113,
        ]


        y_position = 680  # Starting position for receipt details
        for detail in receipt_details:
            c.drawString(50, y_position, detail)
            y_position -= 20

        # Save and close PDF
        c.showPage()
        c.save()

        # Automatically open the PDF for printing (platform-dependent)
        if os.name == 'nt':  # For Windows
            os.startfile(receipt_path, "print")
        elif os.name == 'posix':  # For Linux or Mac
            os.system(f"lp {receipt_path}")

        messagebox.showinfo("Info", f"Transfer receipt for {seller_name} generated and sent to printer.")

    def handle_transfer():
        transfer_amount = transfer.get()
        if not transfer_amount or float(transfer_amount) <= 0:
            messagebox.showerror("Transfer Error", "Please enter a valid transfer amount")
            return

        current_total = float(Total_Seller.get())
        if float(transfer_amount) > current_total:
            messagebox.showerror("Transfer Error", "Transfer amount exceeds available total")
            return

        buyer_reg_no = Recipient_Reg_No.get()
        if buyer_reg_no == '':
            messagebox.showerror("Recipient Error", "Please enter recipient details")
            return

        # Check if the seller is the same as the recipient
        if Seller_Reg_No.get() == buyer_reg_no:
            messagebox.showerror("Transfer Error", "Seller and recipient cannot be the same")
            return

        # Save transaction record
        today = date.today()
        Date = today.strftime("%d/%m/%Y")
        transfer_time = datetime.now().strftime("%H:%M:%S")

        cursor.execute('''
        INSERT INTO transactions (seller_reg_no, buyer_reg_no, amount_kgs, transaction_date, transaction_time, clerk)
        VALUES (?, ?, ?, ?, ?, ?)''', (Seller_Reg_No.get(), buyer_reg_no, transfer_amount, Date, transfer_time, logged_in_clerk))

        conn.commit()
        messagebox.showinfo("Success", "Transfer completed successfully")
        # Fetch the seller's reg no from the StringVar correctly
        seller_reg_no = Seller_Reg_No.get()

        # Query to calculate total kilos for the seller
        query = '''
            SELECT 
                (COALESCE(SUM(r.amount_kgs), 0) - 
                COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.seller_reg_no = m.reg_no), 0) +
                COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.buyer_reg_no = m.reg_no), 0)
                ) AS total_kilos
            FROM members m
            LEFT JOIN member_records r ON m.reg_no = r.reg_no
            WHERE m.reg_no = ?
            GROUP BY m.reg_no
        '''

        # Execute the query with the correct parameter
        cursor.execute(query, (seller_reg_no,))
        result = cursor.fetchone()
        total_kilos = result[0] if result else 0  # Default to 0 if no record found

        # Fetch seller and recipient details
        seller_name = Seller_Name.get()
        buyer_name = Recipient_Name.get()

        # Call the print_transfer_receipt function to generate and print the transfer receipt
        print_transfer_receipt(seller_reg_no, seller_name, total_kilos, transfer_amount, buyer_reg_no, buyer_name, logged_in_clerk, Date, transfer_time)
        Clear()


    def search_mbuni():
        text = M_search.get()

        if text == '':
            messagebox.showerror('Search', 'Enter the member number')
        else:
            # Search for member's details
            cursor.execute('SELECT reg_no, name FROM members WHERE reg_no = ?', (text,))
            result = cursor.fetchone()

            if result:
                M_Reg_No.set(result[0])
                M_Name.set(result[1])

                query = '''
                    SELECT reg_no, name, MAX(topping_date) AS last_date, 
                            SUM(amount_kgs) AS total_kilos
                        FROM mbuni
                        WHERE reg_no LIKE ?
                        GROUP BY reg_no
                '''
                
                # Execute the query
                cursor.execute(query, (text,))
                m_total_result = cursor.fetchone()
                print(m_total_result)


                if m_total_result:
                    mbuni_members_total.set(m_total_result[3])
                    
                else:
                    mbuni_members_total.set(0)
                
                
            else:
                messagebox.showerror('Invalid', 'Registration number not found')
        
    def print_receipt_mbuni(reg_no, name, delivery_kgs, clerk, date, time):
        # Query to calculate total kilos for the member
        query = '''
            SELECT reg_no, name, MAX(topping_date) AS last_date, 
                    SUM(amount_kgs) AS total_kilos
                FROM mbuni
                WHERE reg_no LIKE ?
                GROUP BY reg_no
        '''
        
        # Execute the query
        cursor.execute(query, (reg_no,))
        result = cursor.fetchone()
        total_kilos = result[3] if result else 0  # Accessing the correct index for total kilos

        # Fetch the latest top_id from the mbuni table
        cursor.execute("SELECT top_id FROM mbuni ORDER BY top_id DESC LIMIT 1")
        latest_top_id_record = cursor.fetchone()

        # Check if the fetched record is not None
        if latest_top_id_record:
            latest_top_id = latest_top_id_record[0]
        else:
            latest_top_id = "N/A"  # Handle the case when no record exists
        
        # Ensure the date is formatted correctly (replace '/' with '-')
        formatted_date = date.replace("/", "-")

        # Parse the month from the formatted date (assuming 'DD-MM-YYYY' format)
        month = formatted_date.split('-')[1]  # Extracts the month as a string, e.g., '10'
        month_folder = f"m{int(month)}"  # Converts it to 'm1', 'm2', etc.

        # Define the directory path
        base_dir = "mbuni"
        month_dir = os.path.join(base_dir, month_folder)
        
        # Create directories if they don't exist
        os.makedirs(month_dir, exist_ok=True)

        # Convert time to 12-hour format (handle cases where seconds are included)
        try:
            formatted_time = datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

        # Set up the filename using the actual values, ensuring all parts are strings
        receipt_file = f"receipt_{latest_top_id}_{reg_no}_{formatted_date}.pdf"
        receipt_path = os.path.join(month_dir, receipt_file)

        c = canvas.Canvas(receipt_path, pagesize=letter)

        # Header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, 740, "VUNO KUU COFFEE FACTORY")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 720, "P.O BOX 209, KERICHO")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(230, 700, "MBUNI RECEIPT")

        # Create space for the receipt details
        c.drawString(50, 690, "")  # Create space
        
        # Create space for the receipt details
        c.setFont("Helvetica-Bold", 10)
        
        # Receipt Details
        receipt_details = [
            f"REG ID: {reg_no}      NAME: {name}      DATE: {formatted_date} {formatted_time}",
            "-" * 100,
            f"TOP ID: {'-' * 71} {latest_top_id}",
            f"AMOUNT KGS: {'-' * 60} {delivery_kgs}kgs",
            f"TOTAL KGS: {'-' * 63} {total_kilos}kgs",
            f"SERVED BY: {'-' * 62} {clerk}",
            "-" * 100,
        ]

        y_position = 680  # Starting position for receipt details

        for detail in receipt_details:
            c.drawString(50, y_position, detail)
            y_position -= 20  # Move down for next line

        # Save and close PDF
        c.showPage()
        c.save()

        # Automatically open the PDF for printing (platform-dependent)
        if os.name == 'nt':  # For Windows
            os.startfile(receipt_path, "print")
        elif os.name == 'posix':  # For Linux or Mac
            os.system(f"lp {receipt_path}")

        messagebox.showinfo("Info", f"Receipt for {name} generated and sent to printer.")

    def save_mbuni_Delivery():
        today = date.today()
        Date = today.strftime("%d/%m/%Y")
        top_time = datetime.now().strftime("%H:%M:%S")

        T1 = M_Topping_ID.get()
        R1 = M_Reg_No.get()
        N1 = M_Name.get()
        TD = Date
        TT = top_time
        A1 = M_addition.get()

        if A1 == '' or R1 == '' or N1 == '':
            messagebox.showerror('Error', 'Cannot leave blank fields')
        else:
            cursor.execute('''
            INSERT INTO mbuni (reg_no, name, topping_date, time, amount_kgs, clerk)
            VALUES (?, ?, ?, ?, ?, ?)''', (R1, N1, TD, TT, A1, logged_in_clerk))
            conn.commit()
            messagebox.showinfo("Info", "Record saved successfully!")
            Clear()
            Top_ID()

        # Call the print_receipt function to generate and print the receipt
        print_receipt_mbuni(R1, N1, A1, logged_in_clerk, TD, TT)




    def shift_to_transfers():
        inputframe.place_forget()
        mbuni_frame.place_forget()
        transfersframe.place(x=20, y=0, width=1200, height=1500)

    def shift_to_delivery():
        transfersframe.place_forget()
        mbuni_frame.place_forget()
        inputframe.place(x=20, y=0, width=1200, height=1500)

    def shift_to_mbuni():
        transfersframe.place_forget()
        inputframe.place_forget()
        mbuni_frame.place(x=20, y=0, width=1200, height=1500)

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)


    add_frame = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by:Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S DELIVERY", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=60, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    ###inputframe = Frame(workingFrame, bg='#07531f')
    inputframe = Frame(add_frame, bg='#FF9999')
    inputframe.place(x=20, y=0, width=1200, height=1500)
    
    transfersframe = Frame(add_frame, bg='chocolate')
    transfersframe.place(x=20, y=0, width=0, height=1500)

    # Mbuni Frame
    mbuni_frame = Frame(add_frame, bg='grey')
    mbuni_frame.place(x=20, y=0, width=0, height=250)
    

    # Search input for Delivery
    search = IntVar()
    SearchEntry = Entry(inputframe, textvariable=search, width=12, bd=0, font='arial 30 bold', fg='#07531f').place(x=35, y=20)
    Srch = Button(inputframe, text="Search", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', command=search3).place(x=370, y=16)

    # Delivery Inputs
    Topping_ID = IntVar()
    Reg_No = StringVar()
    Name = StringVar()
    addition = StringVar()
    total_members = StringVar()
    Total = StringVar()

    Label(inputframe, text='Reg_No:', font='arial 20 bold', fg='white', bg='#FF9999').place(x=150, y=120)
    Entry(inputframe, textvariable=Reg_No, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=120)

    Label(inputframe, text='Name:', font='arial 20 bold', fg='white', bg='#FF9999').place(x=150, y=190)
    Entry(inputframe, textvariable=Name, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=190)

    Label(inputframe, text='Total (kgs):', font='arial 20 bold', fg='white', bg='#FF9999').place(x=150, y=260)
    Entry(inputframe, textvariable=total_members, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=260)

    Label(inputframe, text='Delivery (Kgs):', font='arial 20 bold', fg='white', bg='#FF9999').place(x=150, y=330)
    Entry(inputframe, textvariable=addition, width=20, bd=0, font='arial 23 bold', fg='#07531f').place(x=615, y=330)

    # Transfer Frame
    # Seller search inputs
    seller_search = IntVar()
    Entry(transfersframe, textvariable=seller_search, width=12, bd=0, font='arial 30 bold', fg='#07531f').place(x=35, y=20)
    Button(transfersframe, text="Search Seller", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', 
           command=lambda: search_member(seller_search, Seller_Reg_No, Seller_Name)).place(x=370, y=16)

    Seller_Reg_No = StringVar()
    Seller_Name = StringVar()
    Total_Seller = StringVar()

    Label(transfersframe, text='Seller Reg_No:', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=100)
    Entry(transfersframe, textvariable=Seller_Reg_No, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=100)
    Label(transfersframe, text='Seller Name:', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=170)
    Entry(transfersframe, textvariable=Seller_Name, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=170)
    Label(transfersframe, text='Total (Kgs):', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=240)
    Entry(transfersframe, textvariable=Total_Seller, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=240)

    # Additional inputs for transfer
    transfer = StringVar()
    Label(transfersframe, text='Transfer (Kgs):', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=310)
    Entry(transfersframe, textvariable=transfer, width=20, bd=0, font='arial 23 bold', fg='#07531f').place(x=615, y=310)

    recipient_search = IntVar()
    Entry(transfersframe, textvariable=recipient_search, width=12, bd=0, font='arial 30 bold', fg='#07531f').place(x=35, y=360)
    Button(transfersframe, text="Search Recipient", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', 
           command=lambda: search_member(recipient_search, Recipient_Reg_No, Recipient_Name)).place(x=370, y=360)
    Recipient_Reg_No = StringVar()
    Recipient_Name = StringVar()

    Label(transfersframe, text='Recipient Reg_No:', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=440)
    Entry(transfersframe, textvariable=Recipient_Reg_No, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=440)
    Label(transfersframe, text='Recipient Name:', font='arial 20 bold', fg='white', bg='chocolate').place(x=150, y=510)
    Entry(transfersframe, textvariable=Recipient_Name, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=510)

    # Search input for Mbuni Delivery
    M_search = IntVar()
    M_SearchEntry = Entry(mbuni_frame, textvariable=M_search, width=12, bd=0, font='arial 30 bold', fg='#07531f')
    M_SearchEntry.place(x=35, y=20)

    M_Srch = Button(mbuni_frame, text="Search", width=15, bd=0, bg='lightblue', fg='#07531f', font='arial 20 bold', command=search_mbuni)
    M_Srch.place(x=370, y=16)

    # Mbuni Delivery Inputs
    M_Topping_ID = IntVar()
    M_Reg_No = StringVar()
    M_Name = StringVar()
    M_addition = StringVar()
    M_Total = StringVar()
    mbuni_members_total = StringVar()

    Label(mbuni_frame, text='Reg_No:', font='arial 20 bold', fg='white', bg='grey').place(x=150, y=120)
    Entry(mbuni_frame, textvariable=M_Reg_No, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=120)

    Label(mbuni_frame, text='Name:', font='arial 20 bold', fg='white', bg='grey').place(x=150, y=190)
    Entry(mbuni_frame, textvariable=M_Name, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=190)
    
    Label(mbuni_frame, text='Total (kgs):', font='arial 20 bold', fg='white', bg='grey').place(x=150, y=260)
    Entry(mbuni_frame, textvariable=mbuni_members_total, width=20, bd=0, font='arial 23 bold', fg='#07531f', state='disabled').place(x=615, y=260)

    Label(mbuni_frame, text='Mbuni (Kgs):', font='arial 20 bold', fg='white', bg='grey').place(x=150, y=330)
    Entry(mbuni_frame, textvariable=M_addition, width=20, bd=0, font='arial 23 bold', fg='#07531f').place(x=615, y=330)


    # Buttons for switching and saving
    Button(inputframe, text='Save Delivery', width=17, bd=0, bg='#2b9348', fg='#ffffff', font='arial 20 bold', command=save_delivery).place(x=665, y=580)
    Button(inputframe, text='Switch to Mbuni', width=17, bd=0, bg='grey', fg='white', font='arial 20 bold', command=shift_to_mbuni).place(x=350, y=580)
    Button(inputframe, text='Switch to Transfers', width=17, bd=0, bg='orange', fg='white', font='arial 20 bold', command=shift_to_transfers).place(x=35, y=580)


    Button(transfersframe, text='Process Transfer', width=17, bd=0, bg='green', fg='white', font='arial 20 bold', command=handle_transfer).place(x=665, y=580)
    Button(transfersframe, text='Switch to Delivery', width=17, bd=0, bg='red', fg='white', font='arial 20 bold', command=shift_to_delivery).place(x=350, y=580)
    Button(transfersframe, text='Switch to mbuni', width=17, bd=0, bg='grey', fg='white', font='arial 20 bold', command=shift_to_mbuni).place(x=35, y=580)

    
    Button(mbuni_frame, text='Save Mbuni', width=17, bd=0, bg='#2b9348', fg='#ffffff', font='arial 20 bold', command=save_mbuni_Delivery).place(x=665, y=580)
    Button(mbuni_frame, text='Switch to Transfers', width=17, bd=0, bg='orange', fg='white', font='arial 20 bold', command=shift_to_transfers).place(x=350, y=580)
    Button(mbuni_frame, text='Switch to Delivery', width=17, bd=0, bg='red', fg='white', font='arial 20 bold', command=shift_to_delivery).place(x=35, y=580)
    # Initialize topping ID
    Top_ID()

    add_frame.pack(pady=20)
    add_frame.configure(width=1600, height=1150)











def records_page():
    membersdataframe = Frame(workingFrame, bg='#07531f')

    # # Initialize the active table (default to 'member_records')
    # active_table = StringVar(value='member_records')

    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()

    # Fetch transaction data with seller and buyer names
    cursor.execute('''
    SELECT 
        t.transaction_id, 
        m1.reg_no || '. ' || m1.name AS seller,  -- Concatenating reg_no and name for seller
        m2.reg_no || '. ' || m2.name AS buyer,   -- Concatenating reg_no and name for buyer
        t.transaction_date, 
        t.transaction_time, 
        t.amount_kgs, 
        t.clerk
    FROM 
        transactions t
    JOIN 
        members m1 ON t.seller_reg_no = m1.reg_no  -- Join to get seller details
    JOIN 
        members m2 ON t.buyer_reg_no = m2.reg_no   -- Join to get buyer details
    ''')

    # Now fetch the data and bind it to the UI table or frame.
    transactions_data = cursor.fetchall()

    

    # Fetch data from the specified SQLite table
    cursor.execute(f'SELECT * FROM member_records')
    cherry_data = cursor.fetchall()


    # Fetch data from the specified SQLite table
    cursor.execute(f'SELECT * FROM mbuni')
    mbuni_data = cursor.fetchall()

    def show_cherry_records():
        # Clear current columns and headings
        tv1["columns"] = ()
        
        # Reset any existing headings before configuring new ones
        for col in tv1["columns"]:
            tv1.heading(col, text="")
            tv1.column(col, width=0)
        
        # Define the new columns
        column_names = ['Top ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)', 'served by']  # Example column names

        # Configure Treeview columns and headings
        tv1['columns'] = column_names
        tv1['show'] = 'headings'
        for column in column_names:
            tv1.heading(column, text=column)
            tv1.column(column, width=150)

        # Clear previous rows
        for item in tv1.get_children():
            tv1.delete(item)
        
        # Display transaction data
        for row in cherry_data:
            tv1.insert('', 'end', values=row)
        cherry_button.config(bg='white', fg='#07531f')
        mbuni_button.config(bg='#07531f', fg='white')
        transactions_button.config(bg='#07531f', fg='white')
        
        record_label.config(text='CHERRY RECORDS')

    def show_mbuni_records():
        # Clear current columns and headings
        tv1["columns"] = ()
        
        # Reset any existing headings before configuring new ones
        for col in tv1["columns"]:
            tv1.heading(col, text="")
            tv1.column(col, width=0)
        
        # Define the new columns
        column_names = ['Mbuni ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)', 'served by']  # Example column names

        # Configure Treeview columns and headings
        tv1['columns'] = column_names
        tv1['show'] = 'headings'
        for column in column_names:
            tv1.heading(column, text=column)
            tv1.column(column, width=150)

        # Clear previous rows
        for item in tv1.get_children():
            tv1.delete(item)
        
        # Display transaction data
        for row in mbuni_data:
            tv1.insert('', 'end', values=row)
        cherry_button.config(bg='#07531f', fg='white')
        mbuni_button.config(bg='white', fg='#07531f')
        transactions_button.config(bg='#07531f', fg='white')
        
        record_label.config(text='MBUNI RECORDS')


    # # Load data based on the selected table
    # def load_data(table):
    #     global column_names
    #     # Connect to SQLite database
    #     conn = sqlite3.connect('member_data.db')
    #     cursor = conn.cursor()

    #     # Fetch data from the specified SQLite table
    #     cursor.execute(f'SELECT * FROM {table}')
    #     rows = cursor.fetchall()

    #     # Define column names based on the table
    #     if table == 'member_records':
    #         column_names = ['Top ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)', 'served by']
    #     elif table == 'mbuni':
    #         column_names = ['Mbuni ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)', 'served by']
    #     else:  # transactions table
    #         column_names = ['Transaction ID', 'Seller', 'Buyer', 'Date', 'Transaction Time', 'Amount (kgs)', 'served by']

    #     # Configure Treeview columns and headings
    #     tv1['columns'] = column_names
    #     tv1['show'] = 'headings'
    #     for column in column_names:
    #         tv1.heading(column, text=column)
    #         tv1.column(column, width=150)

    #     # Clear previous rows and insert new rows into the Treeview
    #     for item in tv1.get_children():
    #         tv1.delete(item)
    #     for row in rows:
    #         tv1.insert('', 'end', values=row)


    def show_transactions():
        # Clear current columns and headings
        tv1["columns"] = ()
        
        # Reset any existing headings before configuring new ones
        for col in tv1["columns"]:
            tv1.heading(col, text="")
            tv1.column(col, width=0)
        
        # Define the new columns
        column_names = ['Transaction ID', 'Seller', 'Buyer', 'Date', 'Transaction Time', 'Amount (kgs)', 'served by']  # Example column names

        # Configure Treeview columns and headings
        tv1['columns'] = column_names
        tv1['show'] = 'headings'
        for column in column_names:
            tv1.heading(column, text=column)
            tv1.column(column, width=150)

        # Clear previous rows
        for item in tv1.get_children():
            tv1.delete(item)
        
        # Display transaction data
        for row in transactions_data:
            tv1.insert('', 'end', values=row)
        cherry_button.config(bg='#07531f', fg='white')
        mbuni_button.config(bg='#07531f', fg='white')
        transactions_button.config(bg='white', fg='#07531f')
        
        record_label.config(text='TRANSACTION RECORDS')



    # def toggle_view():
    #     # Toggle between 'Mbuni' and 'Cherry'
    #     if toggle_button['text'] == 'Mbuni':
    #         load_data('mbuni')  # Load mbuni records
    #         toggle_button.config(text='Cherry')
    #     else:
    #         load_data('member_records')  # Load member records (cherry)
    #         toggle_button.config(text='Mbuni')

    def search_data():
        query = search.get().lower()  # Convert to lowercase for case-insensitive search
        results.clear()  # Clear previous results
        current_index[0] = 0  # Reset the current index

        # Clear previous selections
        for item in tv1.get_children():
            tv1.selection_remove(item)

        # Check if query is not empty
        if query:
            # Store matched items in results
            for item in tv1.get_children():
                values = tv1.item(item, 'values')
                # Check if Reg_No or Name matches the query
                if str(values[1]).lower() == query or str(values[2]).lower() == query:
                    results.append(item)
        
        # Display the results count only after search
        result_count_label.config(text=f"{len(results)} results found")
        
        # Show the next/previous buttons and navigation info if there are results
        if results:
            next_button.place(x=10, y=100)  # Show next button
            previous_button.place(x=10, y=250)  # Show previous button
            navigation_info_label.place(x=10, y=150)  # Show navigation info
            result_count_label.place(x=10, y=200)  # Show result count
            tv1.selection_add(results[current_index[0]])
            tv1.see(results[current_index[0]])
            update_navigation_info()
        else:
            next_button.place_forget()  # Hide next button if no results
            previous_button.place_forget()  # Hide previous button if no results
            navigation_info_label.place_forget()  # Hide navigation info if no results

    def update_navigation_info():
        # Update the navigation label for the current result
        current_result = current_index[0] + 1
        total_results = len(results)
        navigation_info_label.config(text=f"{current_result}/{total_results}")
        result_count_label.config(text=f"{total_results} results found.")

    def next_result():
        if results:
            # Remove current selection
            tv1.selection_remove(results[current_index[0]])
            current_index[0] = (current_index[0] + 1) % len(results)  # Cycle through results
            tv1.selection_add(results[current_index[0]])
            tv1.see(results[current_index[0]])
            update_navigation_info()

    def previous_result():
        if results:
            # Remove current selection
            tv1.selection_remove(results[current_index[0]])
            current_index[0] = (current_index[0] - 1) % len(results)  # Cycle backwards through results
            tv1.selection_add(results[current_index[0]])
            tv1.see(results[current_index[0]])
            update_navigation_info()

    def save_table_to_pdf():
        # Dialog window for all filter options
        dialog = Toplevel()
        dialog.title("Export to PDF")
        dialog.geometry("400x600")  # Increased to accommodate all fields

        # Table Selection
        Label(dialog, text="Choose Table:").grid(row=0, column=0, padx=5, pady=5)
        table_var = StringVar()
        table_combo = Combobox(dialog, textvariable=table_var, values=['member_records', 'mbuni'])
        table_combo.grid(row=0, column=1, padx=5, pady=5)
        table_combo.set('member_records')  # Default to Cherry

        

        # Define components for Start and End Date dropdowns
        Label(dialog, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        start_date_combo = Combobox(dialog)
        start_date_combo.grid(row=1, column=1, padx=5, pady=5)

        Label(dialog, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        end_date_combo = Combobox(dialog)
        end_date_combo.grid(row=2, column=1, padx=5, pady=5)

        # Minimum and Maximum Kilos Inputs for range
        Label(dialog, text="Min Kilos:").grid(row=3, column=0, padx=5, pady=5)
        min_kilos = Entry(dialog)
        min_kilos.grid(row=3, column=1, padx=5, pady=5)

        Label(dialog, text="Max Kilos:").grid(row=4, column=0, padx=5, pady=5)
        max_kilos = Entry(dialog)
        max_kilos.grid(row=4, column=1, padx=5, pady=5)

        # Clerk Selection with checkboxes directly in dialog
        clerk_vars = {}
        Label(dialog, text="Clerks:").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        clerk_frame = Frame(dialog)
        clerk_frame.grid(row=5, column=1, padx=5, pady=5)

        all_clerks_var = IntVar()
        
        # Clerk Checkbuttons
        clerk_vars = {}
        checkbuttons_list = []  # List to keep track of clerk checkbuttons

        # Function to load clerks based on table selection
        def load_clerks():
            nonlocal checkbuttons_list

            # Clear any existing checkbuttons
            for cb in checkbuttons_list:
                cb.destroy()
            checkbuttons_list.clear()

            # Retrieve and display clerks based on selected table
            selected_table = table_var.get()
            clerk_names = []  # Replace with database query to get clerks for `selected_table`

            for i, clerk in enumerate(clerk_names):
                clerk_var = IntVar()
                cb = Checkbutton(dialog, text=clerk, variable=clerk_var)
                cb.grid(row=5 + i, column=1, sticky=W, padx=5)
                checkbuttons_list.append(cb)  # Track the checkbutton for clearing later
                clerk_vars[clerk] = clerk_var

        # Set up a command to run whenever the table selection changes
        table_combo.bind("<<ComboboxSelected>>", lambda event: load_clerks())

        # Start by loading clerks for the initial table
        load_clerks()

        # Connect to the database to load initial filter options
        def load_filters():
            selected_table = table_var.get()
            conn = sqlite3.connect('member_data.db')
            cursor = conn.cursor()

            # Retrieve dates from the selected table
            cursor.execute(f"SELECT DISTINCT topping_date FROM {selected_table} ORDER BY topping_date")
            dates = [row[0] for row in cursor.fetchall()]

            # Populate date dropdowns
            start_date_combo['values'] = dates
            end_date_combo['values'] = dates
            if dates:
                start_date_combo.set(dates[0])
                end_date_combo.set(dates[-1])

            # Retrieve clerks
            cursor.execute(f"SELECT DISTINCT clerk FROM {selected_table}")
            clerks = [row[0] for row in cursor.fetchall()]
            conn.close()

            # Populate clerks with checkboxes in the main dialog
            Checkbutton(dialog, text="All Clerks", variable=all_clerks_var, command=lambda: select_all_clerks(clerks)).pack(anchor="w", in_=clerk_frame)
            
            clerk_vars.clear()
            for clerk in clerks:
                var = IntVar()
                Checkbutton(dialog, text=clerk, variable=var).pack(anchor="w", in_=clerk_frame)
                clerk_vars[clerk] = var

        # Select all clerks if "All Clerks" is checked
        def select_all_clerks(clerks):
            for var in clerk_vars.values():
                var.set(all_clerks_var.get())

        # Trigger load filters when table selection changes
        table_combo.bind("<<ComboboxSelected>>", lambda event: load_filters())
        load_filters()  # Initial load for default table

        # Confirm and Generate PDF
        def confirm_and_generate():
            # Get the current date and time
            now = datetime.now()

            # Format the date and time to include the abbreviated weekday name
            doc_formatted_time = now.strftime("%a, %Y-%m-%d %H:%M:%S")
            table = table_var.get()
            start = start_date_combo.get()
            end = end_date_combo.get()
            min_kg = min_kilos.get()
            max_kg = max_kilos.get()

            # Selected clerks based on checkboxes
            selected_clerks = [clerk for clerk, var in clerk_vars.items() if var.get() == 1]
            if all_clerks_var.get() == 1:
                selected_clerks = None  # No filter on clerks if "All Clerks" is selected

            # Build SQL Query with filters
            query = f"SELECT * FROM {table} WHERE 1=1"
            params = []

            if start and end:
                query += " AND topping_date BETWEEN ? AND ?"
                params.extend([start, end])
             # Apply kilo range filter if both min and max are provided
            if min_kg and max_kg:
                query += " AND amount_kgs BETWEEN ? AND ?"
                params.extend([float(min_kg), float(max_kg)])
            elif min_kg:  # Only minimum kilos
                query += " AND amount_kgs >= ?"
                params.append(float(min_kg))
            elif max_kg:  # Only maximum kilos
                query += " AND amount_kgs <= ?"
                params.append(float(max_kg))
            if selected_clerks:
                placeholders = ', '.join(['?'] * len(selected_clerks))
                query += f" AND clerk IN ({placeholders})"
                params.extend(selected_clerks)

            # Execute the query with filters
            conn = sqlite3.connect('member_data.db')
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            conn.close()

            # Check if data exists to export
            if not rows:
                messagebox.showinfo("No Data", "No records found with the specified filters.")
                return

            # Create PDF and save it
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 8)

            # Create the printed on text
            printed_on_text = f"Printed on: {doc_formatted_time}"

            pdf.set_font("Arial", "", 10)  # Smaller font size for the date
            pdf.cell(0, 10, printed_on_text, 0, 1, 'R')  # Align right

            # Add Main Heading (centered and bold)
            pdf.set_font("Arial", "B", 16)  # Larger font size for main heading
            pdf.cell(0, 10, "VUNO KUU COFFEE FACTORY", 0, 1, 'C')
            
            pdf.set_font("Arial", "B", 12)  # Subheading with a smaller font
            pdf.cell(0, 8, "P.O BOX 209, KERICHO", 0, 1, 'C')
            
            pdf.set_font("Arial", "I", 10)  # Italics for slogan
            pdf.cell(0, 8, "Sweetness all the way...", 0, 1, 'C')
            pdf.ln(5)  # Space below the main heading

            # Generate header based on filters
            def generate_header():
                if min_kg and selected_clerks:
                    return f"List of members with {min_kg} kilos and above who were served by {', '.join(selected_clerks)} from {start} to {end}"
                elif min_kg:
                    return f"List of members with {min_kg} kilos and above from {start} to {end}"
                elif selected_clerks:
                    return f"List of members served by {', '.join(selected_clerks)} from {start} to {end}"
                else:
                    return f"List of members' deliveries from {start} to {end}"
                

            # Add the header to PDF
            header_text = generate_header()
            pdf.set_font("Arial", "B", 8)
            pdf.cell(0, 10, header_text, 0, 1, 'C')


            # PDF headers with adjusted widths
            column_names = ['Top ID', 'Reg_No', 'Name', 'Topping_Date', 'Time', 'Amount (kgs)', 'Served By']
            column_widths = [15, 20, 30, 25, 25, 20, 30]

            for col, width in zip(column_names, column_widths):
                pdf.cell(width, 7, col, border=1, align="C")
            pdf.ln()

            # Add rows to PDF with adjusted cell width and height
            pdf.set_font("Arial", "", 8)
            for row in rows:
                for i, item in enumerate(row):
                    pdf.cell(column_widths[i], 6, str(item), border=1, align="C")
                pdf.ln()

            # Ensure generated_folders directory exists
            output_dir = 'generated_folders'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Modify file path to include all relevant criteria
            start_date_safe = start.replace('/', '-')
            end_date_safe = end.replace('/', '-')
            min_kg_str = f"_min{min_kg}" if min_kg else ""
            clerks_str = f"_clerks_{'_'.join(selected_clerks).replace(' ', '_')}" if selected_clerks else "_all_clerks"

            # Combine for a unique filename
            filename = f"{table}_filtered_{start_date_safe}_to_{end_date_safe}{min_kg_str}{clerks_str}.pdf"
            file_path = os.path.join(output_dir, filename)

            # Save PDF file with unique name
            pdf.output(file_path)

            messagebox.showinfo("PDF Generated", f"PDF successfully saved to {file_path}")
            dialog.destroy()  # Close the dialog after saving

        # Button to confirm and generate PDF
        Button(dialog, text="Generate PDF", command=confirm_and_generate).grid(row=8, column=1, padx=5, pady=10)

    # # Function to handle button clicks and load the respective table data
    # def handle_button_click(table_name):
    #     active_table.set(table_name)
    #     load_data(table_name)
    #     update_button_styles()

    # # Update the button styles to show the active button
    # def update_button_styles():
    #     cherry_button.config(relief="sunken" if active_table.get() == 'member_records' else "raised")
    #     mbuni_button.config(relief="sunken" if active_table.get() == 'mbuni' else "raised")
    #     transactions_button.config(relief="sunken" if active_table.get() == 'transactions' else "raised")

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)


    # Layout setup
    factoryframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    record_label = Label(workingFrame, text="MEMBER'S ADDITION", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline')
    record_label.pack(side=TOP, fill=X, pady=20, padx=30)

    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    inputframe = Frame(workingFrame, bg='grey')
    inputframe.pack(fill=BOTH, padx=10, expand=True)
    inputframe.configure(width=990, height=750)

    style = ttk.Style(inputframe)
    tv1 = ttk.Treeview(inputframe, height=20)
    style.configure('Treeview', background='#07531f', foreground='white', font='arial 13 bold', bordercolor='#07531f')
    style.configure('Treeview.Heading', font='arial 13 bold', foreground='#07531f')
    tv1.grid(row=0, column=0, sticky="nsew")  # Use grid layout

    treescrolly = ttk.Scrollbar(inputframe, orient='vertical', command=tv1.yview)
    tv1.configure(yscrollcommand=treescrolly.set)
    treescrolly.grid(row=0, column=1, sticky="ns")

    # Configure inputframe's grid layout
    inputframe.grid_columnconfigure(0, weight=4)  # Make the treeview expand
    inputframe.grid_columnconfigure(2, weight=1)  # Make the navigation frame remain on the right

    navigationFrame2 = Frame(inputframe, bg='grey')
    navigationFrame2.grid(row=0, column=2, sticky="ns")
    navigationFrame2.configure(width=250, height=750)

    search = StringVar()
    Entry(navigationFrame2, textvariable=search, bd=0, width=17, font='arial 17 bold', fg='#07531f', bg='white').place(x=10, y=10)

    Button(navigationFrame2, text='Search', bd=0, width=20, height=2, fg='white', bg='#07531f',
           activeforeground='white', activebackground='#07531f', command=search_data).place(x=10, y=50)

    # Initialize the next button and navigation labels as hidden
    next_button = Button(navigationFrame2, text='Next', bd=0, width=20, height=2, fg='#07531f', bg='white',
           activeforeground='#07531f', activebackground='white', command=next_result)
    navigation_info_label = Label(navigationFrame2, text="0/0", bg='#07531f', fg='white', font='arial 15')
    result_count_label = Label(navigationFrame2, text="0 results found", bg='#07531f', fg='white', font='arial 15')
    previous_button = Button(navigationFrame2, text='Previous', bd=0, width=20, height=2, fg='#07531f', bg='white',
           activeforeground='#07531f', activebackground='white', command=previous_result)

    # Initially hide next button and navigation info label
    next_button.place_forget()
    previous_button.place_forget()
    navigation_info_label.place_forget()
    result_count_label.place_forget()

    # toggle_button = Button(navigationFrame2, text='Mbuni', bd=0, width=20, height=2, fg='white', bg='#07531f',
    #                        activeforeground='white', activebackground='#07531f', command=toggle_view)
    # toggle_button.place(x=10, y=250)

    
    print_pdf_label = Label(navigationFrame2, text="---print pdf---", bg='grey', fg='white', font='arial 15')
    print_pdf_label.place(x=10, y=300)


    to_pdf_button = Button(navigationFrame2, text='GEN PDF', bd=0, width=20, height=2, fg='white', bg='#07531f',
                           activeforeground='white', activebackground='#07531f', command=save_table_to_pdf)
    to_pdf_button.place(x=10, y=330)

    
    viewsection_label = Label(navigationFrame2, text="------view------", bg='grey', fg='white', font='arial 15')
    viewsection_label.place(x=10, y=400)

    cherry_button = Button(navigationFrame2, text="Cherry", bd=0, width=20, height=2, fg='white', bg='#07531f',
                           activeforeground='white', activebackground='#07531f', command=show_cherry_records)
    cherry_button.place(x=10, y=450)

    mbuni_button = Button(navigationFrame2, text="Mbuni", bd=0, width=20, height=2, fg='white', bg='#07531f',
                           activeforeground='white', activebackground='#07531f', command=show_mbuni_records)
    mbuni_button.place(x=10, y=500)

    transactions_button = Button(navigationFrame2, text="Transactions", bd=0, width=20, height=2, fg='white', bg='#07531f',
                           activeforeground='white', activebackground='#07531f', command=show_transactions)
    transactions_button.place(x=10, y=550)

    # Update button styles initially
    show_cherry_records()

    membersdataframe.pack(pady=20)
    membersdataframe.configure(width=1600, height=100)

    results = []  # List to hold search results
    current_index = [0]  # Current index for pagination


    # Bind Enter key to the search_data function
    Entry(navigationFrame2, textvariable=search, bd=0, width=17, font='arial 17 bold', fg='#07531f', bg='white').bind('<Return>', lambda event: search_data())



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
        tv1['columns'] = column_names
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
        selected_columns = column_selection.get()
    

        results.clear()
        current_index[0] = 0

        # Clear previous highlights
        for item in tv1.get_children():
            tv1.item(item, tags='')

        if query and selected_columns:
            # Determine which columns to search
            columns_to_search = []
            if selected_columns == "All Columns":
                columns_to_search = [i for i in range(len(tv1['columns']))]
            else:
                columns_to_search = [tv1['columns'].index(col) for col in selected_columns.split(', ')]

            # Filter based on the dropdown option if selected
            for item in tv1.get_children():
                values = tv1.item(item, 'values')

                # Check if the query matches any of the selected column values
                if any(query in str(values[i]).lower() for i in columns_to_search):
                    results.append(item)
                    tv1.item(item, tags='match')  # Highlight matched item

            # Apply tags for matched items
            tv1.tag_configure('match', background='#87CEEB')  # Highlight color for matches
            update_navigation_info()

            # Update result count label
            result_count_label.config(text=f"{len(results)} results found")
            if results:
                next_button.place(x=10, y=270)
                navigation_info_label.place(x=10, y=240)
                show_current_result()  # Highlight the first result if any
            else:
                next_button.place_forget()
                navigation_info_label.place_forget()

    def show_current_result():
        # Remove highlight for the previous result
        if results:
            for item in results:
                tv1.item(item, tags='match')
            # Highlight the current result
            tv1.item(results[current_index[0]], tags='current_match')
            tv1.tag_configure('current_match', background='#Ff9999')  # Different color for current item
            tv1.see(results[current_index[0]])
            update_navigation_info()

    def next_result():
        if results:
            current_index[0] = (current_index[0] + 1) % len(results)  # Cycle through results
            show_current_result()

    def update_navigation_info():
        if results:
            current_result = current_index[0] + 1
            total_results = len(results)
            navigation_info_label.config(text=f"{current_result}/{total_results}")
    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)

    # GUI Setup
    factoryframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com",
          font='arial 12 italic', width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="MEMBER'S LIST", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    inputframe = Frame(workingFrame, bg='#07531f')
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

    load_data()

    navigationFrame2 = Frame(inputframe, bg='#07531f')
    navigationFrame2.pack(side=RIGHT)
    navigationFrame2.configure(width=250, height=1000)

    search = StringVar()
    SearchEntry = Entry(navigationFrame2, textvariable=search, bd=0, width=14, font='arial 20 bold', fg='#07531f', bg='white')
    SearchEntry.place(x=10, y=10)

    Button(navigationFrame2, text='Search', bd=0, width=10, height=1, fg='#07531f', bg='white', font='arial 17 bold',
           activeforeground='#07531f', activebackground='white', command=search_data).place(x=10, y=50)

    ###Sort by label
    sort_label = Label(navigationFrame2, text="Search by: ", bg='#07531f', fg='#FFF', font='arial 15').place(x=10, y=110)

    # Dropdown for column selection
    column_selection = StringVar()
    column_options = ["All Columns"] + [", ".join([col]) for col in tv1['columns']]
    column_menu = OptionMenu(navigationFrame2, column_selection, *column_options)
    column_menu.config(width=10, bg='white', fg='#07531f', font='arial 14 bold', bd=0)
    column_menu.place(x=10, y=140)
    column_selection.set("All Columns")


    # Navigation and result labels
    next_button = Button(navigationFrame2, text='Next', bd=0, width=10, height=1, fg='white', bg='#Ff9999', font='arial 14 bold',
                         activeforeground='white', activebackground='#Ff9999', command=next_result)

    navigation_info_label = Label(navigationFrame2, text="0/0", bg='#07531f', fg='#Ff9999', font='arial 15')
    result_count_label = Label(navigationFrame2, text="", bg='#07531f', fg='#Ff9999', font='arial 15')

    # Initially hide navigation and next button
    next_button.place_forget()
    navigation_info_label.place_forget()
    result_count_label.place(x=10, y=200)

    # Bind Enter key to the search_data function
    SearchEntry.bind('<Return>', lambda event: search_data())

    factoryframe.pack(pady=20)
    factoryframe.configure(width=1600, height=1150)

    results = []
    current_index = [0]


def cumulative_page():
    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)

    # Initialize the frame for the cumulative data
    cumulative_frame = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    
    cumulative_label = Label(workingFrame, text="CHERRY CUMULATIVE", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline')
    cumulative_label.pack(side=TOP, fill=X, pady=20, padx=30)
    cumulative_frame.pack(fill=BOTH, expand=True, padx=10)

    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    # Create a navigation frame positioned vertically on the right
    navigation_frame = Frame(cumulative_frame, bg='#07531f', width=15)
    navigation_frame.pack(side=RIGHT, fill=Y)

    

    # Function to load data based on the view
    def load_data(view):
        # Clear existing rows in the treeview
        tree.delete(*tree.get_children())
        
        if view == 'mbuni':
            # Query for Mbuni data
            query = '''
                SELECT m.reg_no, m.name, m.phone, MAX(r.topping_date) AS last_date, 
                       SUM(r.amount_kgs) AS total_kilos
                FROM members m
                LEFT JOIN mbuni r ON m.reg_no = r.reg_no
                GROUP BY m.reg_no
            '''
        else:
            # Query for Cherry data
            query = '''
                SELECT m.reg_no, m.name, m.phone, MAX(r.topping_date) AS last_date,
                       (COALESCE(SUM(r.amount_kgs), 0) - 
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.seller_reg_no = m.reg_no), 0) +
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.buyer_reg_no = m.reg_no), 0)
                       ) AS total_kilos
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

        

    # Function to toggle between Cherry and Mbuni data
    def toggle_view():
        if toggle_button['text'] == 'Mbuni':
            load_data('mbuni')  # Load Mbuni records
            toggle_button.config(text='Cherry', bg='red', fg='white')
            cumulative_label.config(text='MBUNI CUMULATIVE')
        else:
            load_data('member_records')  # Load Cherry records
            toggle_button.config(text='Mbuni', bg='grey', fg='white')
            cumulative_label.config(text='CHERRY CUMULATIVE')

    # Function to search for a name or registration ID
    def search():
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showerror('Search error', 'The search input is empty')
            return
        
        # Clear existing rows in the treeview
        tree.delete(*tree.get_children())
        
        # Determine current view for the search
        current_view = toggle_button['text']
        if current_view == 'Mbuni':
            query = '''
                SELECT m.reg_no, m.name, m.phone, MAX(r.topping_date) AS last_date,
                       (COALESCE(SUM(r.amount_kgs), 0) - 
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.seller_reg_no = m.reg_no), 0) +
                        COALESCE((SELECT SUM(t.amount_kgs) FROM transactions t WHERE t.buyer_reg_no = m.reg_no), 0)
                       ) AS total_kilos
                FROM members m
                LEFT JOIN member_records r ON m.reg_no = r.reg_no
                WHERE m.name LIKE ? OR m.reg_no LIKE ?
                GROUP BY m.reg_no
            '''
        else:
            query = '''
                SELECT m.reg_no, m.name, m.phone, MAX(r.topping_date) AS last_date, 
                       SUM(r.amount_kgs) AS total_kilos
                FROM members m
                LEFT JOIN mbuni r ON m.reg_no = r.reg_no
                GROUP BY m.reg_no
            '''

        cursor = conn.cursor()
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()

        # Insert data into the main Treeview
        for row in rows:
            tree.insert('', 'end', values=row)


    
    search_entry = Entry(navigation_frame, width=8, bd=0, fg='#07531f', bg='white', font='arial 20 bold')
    search_entry.pack(pady=10)
    
    search_button = Button(navigation_frame, text='Search', bd=0, width=10, height=1, bg="#fff", fg='#07531f',
          font='arial 17 bold',activeforeground='#07531f', activebackground='white', command=search)
    search_button.pack(pady=30)

    # Button for toggling between Mbuni and Cherry views
    toggle_button = Button(navigation_frame, text='Mbuni', bd=0, width=10, height=1, bg="grey", fg='white',
          font='arial 17 bold',activeforeground='white', activebackground='grey', command=toggle_view)
    toggle_button.pack(pady=40)

    # Create a Treeview widget to display the cumulative data
    style = ttk.Style(cumulative_frame)
    tree = ttk.Treeview(cumulative_frame, columns=('reg_no', 'name', 'phone', 'last_date', 'total_kilos'),
                        show='headings')
    style.configure('Treeview', background='#07531f', foreground='white', font='arial 13 bold', bordercolor='#07531f')
    style.configure('Treeview.Heading', font='arial 13 bold', foreground='#07531f')
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
    detail_tree = ttk.Treeview(cumulative_frame, columns=('top_id', 'topping_date', 'time', 'amount_kgs', 'category'),
                               show='headings')
    detail_tree.heading('top_id', text='Top ID')
    detail_tree.heading('topping_date', text='Topping Date')
    detail_tree.heading('time', text='Time')
    detail_tree.heading('amount_kgs', text='Amount (Kgs)')
    detail_tree.heading('category', text='Category')

    detail_tree.column('top_id', width=100)
    detail_tree.column('topping_date', width=150)
    detail_tree.column('time', width=100)
    detail_tree.column('amount_kgs', width=100)
    detail_tree.column('category', width=100)

    # Add scrollbar to detailed Treeview
    detail_scrollbar = Scrollbar(cumulative_frame, orient='vertical', command=detail_tree.yview)
    detail_tree.configure(yscrollcommand=detail_scrollbar.set)
    detail_scrollbar.pack(side=LEFT, fill=Y)

    # Pack the detailed Treeview
    detail_tree.pack(fill=BOTH, expand=TRUE)

    # Query the database and load default data (Mbuni initially)
    load_data('member records')

    # Function to display detailed deliveries for the selected member
    def show_detailed_deliveries(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            reg_no = item['values'][0]  # Get the reg_no of the selected member
            current_view = toggle_button['text']  # Get the current view (Mbuni or Cherry)

            # Clear the detailed Treeview
            detail_tree.delete(*detail_tree.get_children())

            # Determine which detailed query to run based on the current view
            if current_view == 'Cherry':
                # Query for detailed deliveries from member_records for Cherry
                detailed_query = '''
                    SELECT 'D-' || top_id AS top_id, topping_date, time, amount_kgs, 'Delivery' AS category
                    FROM mbuni
                    WHERE reg_no = ?
                    ORDER BY topping_date ASC
                '''
                cursor.execute(detailed_query, (reg_no,))
            else:
                # Query for detailed deliveries from mbuni for Mbuni view
                detailed_query = '''
                    SELECT 'D-' || top_id AS top_id, topping_date, time, amount_kgs, 'Delivery' AS category
                    FROM member_records
                    WHERE reg_no = ?
                    UNION ALL
                    SELECT 'T-' || transaction_id AS top_id, transaction_date, transaction_time, -amount_kgs, 'Sold'
                    FROM transactions
                    WHERE seller_reg_no = ?
                    UNION ALL
                    SELECT 'T-' || transaction_id AS top_id, transaction_date, transaction_time, +amount_kgs, 'Bought'
                    FROM transactions
                    WHERE buyer_reg_no = ?
                    ORDER BY topping_date ASC, transaction_date ASC
                '''
                cursor.execute(detailed_query, (reg_no, reg_no, reg_no))

            detailed_rows = cursor.fetchall()

            # Insert the detailed deliveries into the detailed Treeview
            for detailed_row in detailed_rows:
                detail_tree.insert('', 'end', values=(detailed_row[0], detailed_row[1], detailed_row[2], detailed_row[3], detailed_row[4]))

            # Calculate and display the total kilos at the bottom of the detailed Treeview
            total_kilos = sum(row[3] for row in detailed_rows)
            detail_tree.insert('', 'end', values=('Total', '', '', total_kilos, ''))

    # Bind the selection event to the Treeview
    tree.bind('<<TreeviewSelect>>', show_detailed_deliveries)



def analytics_page():

    def update_time():
        # Get the current time and date
        now = datetime.now()
        current_time = now.strftime("%a, %Y-%m-%d  %I:%M %p")
        # Update the label text with the current time
        time_label.config(text=current_time)
        # Schedule the label to update after 1000 milliseconds (1 second)
        time_label.after(1000, update_time)

    # Initialize window

    analyticsframe = Frame(workingFrame, bg='#07531f')
    Label(workingFrame, text="Developed by: Limo Brian             Email: limobrian48@gmail.com", font='arial 12 italic',
          width=10, height=3, bg="#b9462a", fg="#ffffff", anchor='e').pack(side=BOTTOM, fill=X)
    Label(workingFrame, text="ANALYTICS", width=10, height=2, bg="#07531f", fg='#fff',
          font='arial 25 bold underline').pack(side=TOP, fill=X, pady=20, padx=30)
    
    # Create a label to display the time
    time_label = Label(workingFrame, font=('Helvetica', 16), fg='white', bg='#07531f')
    time_label.place(x=10, y=50)

    # Start the time update loop
    update_time()

    analyticsframe.pack(fill=BOTH, expand=True, padx=10)

    # Create a frame for the plots
    plot_frame = ttk.Frame(analyticsframe)
    plot_frame.pack(fill=BOTH, expand=True)

    def plot_member_growth():
        conn = sqlite3.connect('member_data.db')
        df = pd.read_sql_query("SELECT COUNT(*) AS members, reg_date FROM members GROUP BY reg_date ORDER BY reg_date ASC", conn)
        conn.close()

        # Ensure reg_date is parsed as datetime, specifying dayfirst=True
        df['reg_date'] = pd.to_datetime(df['reg_date'], dayfirst=True)

        # Sort by the actual date (even though SQL orders it, it's good to ensure pandas also treats it as dates)
        df = df.sort_values(by='reg_date')

        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df['reg_date'], df['members'], marker='o', color='green')
        ax.set_title("Member Growth Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Members")

        # Format the x-axis for better date display
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        fig.autofmt_xdate()

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
            date_column = 'topping_date'
        elif period == 'monthly':
            query = "SELECT SUM(amount_kgs) AS total_kgs, strftime('%Y-%m', topping_date) AS month FROM member_records GROUP BY month"
            date_column = 'month'
        elif period == 'yearly':
            query = "SELECT SUM(amount_kgs) AS total_kgs, strftime('%Y', topping_date) AS year FROM member_records GROUP BY year"
            date_column = 'year'

        df = pd.read_sql_query(query, conn)
        conn.close()

        # Convert date column to datetime if period is daily
        if period == 'daily':
            df[date_column] = pd.to_datetime(df[date_column], dayfirst=True)

        # Sort the DataFrame by the date column
        df = df.sort_values(by=date_column)

        # Create figure and plot
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(df[date_column], df['total_kgs'], marker='o', color='blue')
        ax.set_title(f"Kilo Trends ({period.capitalize()})")
        ax.set_xlabel(period.capitalize())
        ax.set_ylabel("Total Kilos")

        # Format x-axis for dates if period is daily
        if period == 'daily':
            import matplotlib.dates as mdates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            fig.autofmt_xdate()  # Automatically format date labels

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
    register_indicate.config(bg='#c3c3c3')
    delivery_indicate.config(bg='#c3c3c3')
    records_indicate.config(bg='#c3c3c3')
    list_indicate.config(bg='#c3c3c3')
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
    delivery_btn.config(fg='black')
    records_btn.config(fg='black')
    list_btn.config(fg='black')
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
    delivery_btn.config(fg='#07531f')
    records_btn.config(fg='#07531f')
    list_btn.config(fg='#07531f')
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

#######################################################################LOGIN####################################

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin():
    password = '1234'
    username = 'limo'
    id_number = '40586847'
    phone_number = '0746120864'
    first_name = 'Limo'
    last_name = 'Brian'
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO user_registry (username, password, usertype, id_number, phone_number, date_added, first_name, last_name)
            VALUES (?, ?, ?, ?, ?, date('now'), ?, ?)
        """, (username, hashed_password, 'admin', id_number, phone_number, first_name, last_name))
        
        conn.commit()
        print(f"Clerk {first_name} {last_name} added successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different one.")
    finally:
        conn.close()

# Call the function to create an admin
create_admin()

def authenticate_user(username, password):
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT usertype FROM user_registry WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    conn.close()
    return user[0] if user else None

def redirect_to_dashboard(usertype):
    if usertype == 'admin':
        # Load admin dashboard
        print("Redirecting to Admin Dashboard")
        # Here, you would call the function to open the admin dashboard window
    elif usertype == 'clerk':
        # Load clerk dashboard
        print("Redirecting to Clerk Dashboard")
        # Here, you would call the function to open the clerk dashboard window
    else:
        messagebox.showerror("Login Error", "Invalid user type!")


# Global variable to store the currently logged-in clerk's username
current_logged_in_clerk = None

# Function to handle user login based on usertype
def login():
    global user_label, usertype, current_logged_in_clerk  # Include the new variable

    username = usernameEntry.get()
    password = passwordEntry.get()

    # Validate inputs
    if username == 'Username' or username == '' or password == 'Password' or password == '':
        messagebox.showerror('Login Error', 'Username or password cannot be blank')
        return

    print("Username entered:", username)
    print("Password entered:", password)

    # Connect to SQLite database
    conn = sqlite3.connect('member_data.db')
    cursor = conn.cursor()

    # Fetch the hashed password from the database
    cursor.execute("SELECT password, usertype FROM user_registry WHERE username=?", (username,))
    user = cursor.fetchone()
    print(f"Fetched user record: {user}")

    if user:
        stored_hashed_password = user[0]  # The hashed password
        usertype = user[1]  # Extract the usertype ('admin' or 'clerk')

        # Verify the entered password against the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            print(f"Usertype is: {usertype}")  # For verification
            # Set the currently logged-in clerk's username
            if usertype == "clerk":
                current_logged_in_clerk = username  # Store the clerk's username
            
            # Call toggle_buttons based on usertype
            toggle_buttons(usertype)

            # Set the user label
            user_label.config(text=f"Logged in as: {username} ({usertype})")
            if usertype == "admin":
                print("Redirecting to Admin Dashboard...")
                welcomeframe.config(width=0)
                hideButton.config(text='HIDE MENU')
            elif usertype == "clerk":
                print("Redirecting to Clerk Dashboard...")
                welcomeframe.config(width=0)
                hideButton.config(text='HIDE MENU')
            else:
                print("Invalid usertype!")  # Fallback for unexpected usertypes
        else:
            messagebox.showerror('Login Error', 'Invalid username or password')  # Handle invalid credentials
            user_label.config(text="Invalid login")
    else:
        messagebox.showerror('Login Error', 'Invalid username or password')  # Handle invalid credentials
        user_label.config(text="Invalid login")

    conn.close()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

    

# Sample functions to load dashboards (replace these with actual implementations)
def open_admin_dashboard():
    print("Admin Dashboard Opened")

def open_clerk_dashboard():
    print("Clerk Dashboard Opened")





# Example form fields in Tkinter:
welcomeframe = Frame(mainframe, bg='#07531f', width=300, height=3000)
userframe = Frame(welcomeframe,bg='#07531f', highlightbackground='red', highlightthickness=4)
usernameEntry = Entry(userframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0)
usernameEntry.place(x=250, y=130)

passwordEntry = Entry(userframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0)
passwordEntry.place(x=250, y=210)

idEntry = Entry(userframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0)
idEntry.place(x=250, y=290)

phoneEntry = Entry(userframe, width=30, font=('Microsoft Yahei UI Light', 20, 'bold'), bd=0)
phoneEntry.place(x=250, y=370)

# Button to submit the form
registerButton = Button(userframe, text="Register Clerk", bg="white", width=15, bd=0, height=1, 
                        font=('Open Sans', 23, 'bold'), fg="#07531f", 
                        activebackground="white", activeforeground="#07531f")
registerButton.place(x=350, y=450)

bgcolor = 'white'
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
userframe.pack(pady=10)
userframe.configure(width=987, height=500, bg='white')
loginframe = Frame(userframe,bg='#07531f')
loginframe.pack(side=LEFT)
loginframe.configure(width=987, height=500)

def hide():
    openeye.config(file=image_path2)
    passwordEntry.config(show='')
    eyeButton.config(command=show)

def show():
    openeye.config(file=image_path)
    passwordEntry.config(show='*')
    eyeButton.config(command=hide)

# Function to toggle the buttons based on usertype
def toggle_buttons(usertype):
    if usertype == 'clerk':
        register_btn.place(x=20, y=260)  # Show register button for clerks
        delivery_btn.place(x=20, y=362)
        clerks_btn.place_forget()  # Hide clerks button for clerks
        viewclerks_btn.place_forget()
    elif usertype == 'admin':
        clerks_btn.place(x=20, y=260)  # Show clerks button for admin
        viewclerks_btn.place(x=20, y=362)
        delivery_btn.place_forget()  # Hide register button for admin
        register_btn.place_forget()

    else:
        # Hide both buttons if usertype is invalid or undefined
        register_btn.place_forget()
        clerks_btn.place_forget()
    # Inside toggle_buttons function
    print(f"Usertype is: {usertype}")




def user_enter(event):
    if usernameEntry.get() == "Username":
        usernameEntry.delete(0, END)
def password_enter(event):
    if passwordEntry.get() == "Password":
        passwordEntry.delete(0, END)
        passwordEntry.config(show='*')

heading = Label(loginframe, text="USERLOGIN", font=('arial 25 bold'), bg='#07531f',
                fg='white')
heading.place(x=400, y=25)

# Username Entry
usernameEntry = Entry(loginframe, width=30, font=('arial 25 bold'), bd=0, fg="white",
                      bg='#07531f')
usernameEntry.place(x=250, y=130)
usernameEntry.insert('0', 'Username')

usernameEntry.bind('<Return>',focus_next_widget)
usernameEntry.bind('<FocusIn>', user_enter, focus_next_widget)


frame1 = Frame(loginframe, width=480, height=4, bg='white')
frame1.place(x=250, y=170)

# Password Entry
passwordEntry = Entry(loginframe, width=30, font=('arial 25 bold'), bd=0, fg="white",
                      bg='#07531f')
passwordEntry.place(x=250, y=210)
passwordEntry.insert('0', 'Password')

passwordEntry.bind('<Return>', lambda event:login())
passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(loginframe, width=480, height=4, bg='white')
frame2.place(x=250, y=247)


# Determine the base path depending on whether we're running as a script or as a bundled executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the image
image_path = os.path.join(base_path, 'images/close.png')
image_path2 = os.path.join(base_path,'images/open.png')

# Load the image
openeye = PhotoImage(file=image_path2)
closeeye = PhotoImage(file=image_path, width=30)
eyeButton=Button(loginframe, image=openeye, activebackground='#07531f',activeforeground='#07531f',bd=0, bg='#07531f',cursor='hand2', command=hide)
eyeButton.place(x=702, y=215)


# Login Button
loginButton = Button(loginframe, text="Login", bg="white", width=15, bd=0, height=1, 
                     font=('Open Sans', 23, 'bold'), fg="#07531f", 
                     activebackground="white", activeforeground="#07531f", command=login)
loginButton.place(x=350, y=360)






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

register_btn = Button(navigationFrame, width=20, height=2, text='REGISTER', font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(register_indicate, homepage))
register_btn.place(x=20, y=260)

clerks_btn = Button(navigationFrame, width=20, height=2, text='CLERKS', font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda: indicate(register_indicate, clerkpage))  # Adjust the command as necessary
clerks_btn.place(x=20, y=260)

register_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
register_indicate.place(x=0, y=260, width=20, height=98)

delivery_btn = Button(navigationFrame, width=20, height=2, text='DELIVERY', 
                      font='arial 24 bold', fg='#07531f', bd=0, 
                      activebackground='#c3c3c3', bg='#c3c3c3', 
                      command=lambda: indicate(delivery_indicate, lambda: add_page(current_logged_in_clerk)))

viewclerks_btn = Button(navigationFrame, width=20, height=2, text='VIEW CLERKS', font='arial 24 bold', fg='#07531f', bd=0, activebackground='#c3c3c3', bg='#c3c3c3', command=lambda : indicate(delivery_indicate, viewclerks))
viewclerks_btn.place(x=20, y=362)

delivery_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
delivery_indicate.place(x=0, y=362, width=20, height=98)

records_btn = Button(navigationFrame, width=20, height=2, text="RECORDS", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(records_indicate, records_page))
records_btn.place(x=20, y=464)

records_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
records_indicate.place(x=0, y=464, width=20, height=98)

list_btn = Button(navigationFrame, width=20, height=2, text="MEMBER'S LIST", font='arial 24 bold', fg='#07531f', bd=0, bg='#c3c3c3', activebackground='#c3c3c3', command=lambda : indicate(list_indicate, factory_page))
list_btn.place(x=20, y=566)

list_indicate= Label(navigationFrame, text='', bg='#c3c3c3')
list_indicate.place(x=0, y=566, width=20, height=98)

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

user_label = Label(navigationFrame, text="", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='#07531f')
user_label.pack(side=TOP, anchor='w')



workingFrame = Frame(mainframe, bg='#07531f')

workingFrame.pack(fill=BOTH, expand=TRUE)
workingFrame.pack_propagate(False)
workingFrame.configure(width=1600, height=1500)



hideButton = Button(mainframe,text='', bg='#07531f', fg='white', font='arial 15 bold',bd=0, command=hidebutton)
hideButton.place(x=275, y=2)




mainframe.mainloop()
