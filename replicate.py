# REPETITIVE FUNCTIONS ACROSS PROGRAM
from tkinter import *
import mysql.connector as my
from tkinter import messagebox
from PIL import Image, ImageTk
from validate_email import validate_email
import time


# ----------------------Menu Bar-------------------------------------#
# Functions for respective windows------------------------------
def homepage(screen):
    import homepage as hp
    screen.destroy()
    hp.main_page(c)


def books(screen):
    import Books
    screen.destroy()
    Books.book(c)


def members(screen):
    import Members
    screen.destroy()
    Members.members(c)


def funds(screen):
    import Funds
    screen.destroy()
    Funds.funds(c)


def dev_info(screen):
    import Developers_info
    screen.destroy()
    Developers_info.info(c)


# Main menu bar-------------------------------------------------
def menubar(screen, screen_, treeview, b):
    global c
    c = b

    # ----------------------------------------------------------------
    # defining edit function
    def accounts():
        accounts_frame = Frame(screen, bg="black")
        accounts_frame.place(relx=0.79, rely=0.008, relheight=0.3,
                             relwidth=0.2)

        # ------------------------------------------------------------
        # defining editaccount function
        def editaccount():
            my_con = my.connect(host='sql11.freemysqlhosting.net',
                                user='sql11422143',
                                passwd='pq3EcPFj4e', db='sql11422143')
            cur = my_con.cursor()
            query = "select*from user_password"
            cur.execute(query)
            data = cur.fetchone()
            my_con.close()

            edit_account_frame = Frame(screen, bg='grey')
            edit_account_frame.place(relx=0.79, rely=0.008,
                                     relheight=0.3, relwidth=0.2)

            user_id_label = Label(edit_account_frame,
                                  text="Enter the username:",
                                  bg='black', fg='white')
            user_id_label.place(relx=0.1, rely=0.3)
            user_id_entry = Entry(edit_account_frame, width=23)
            user_id_entry.insert(0, data[0])
            user_id_entry.bind("<Return>",
                               lambda e: password_entry.focus)
            user_id_entry.place(relx=0.5, rely=0.3)

            password_label = Label(edit_account_frame,
                                   text="Enter the password:",
                                   bg='black', fg='white')
            password_label.place(relx=0.1, rely=0.5)
            password_entry = Entry(edit_account_frame, width=23)
            password_entry.insert(0, data[1])
            password_entry.bind("<Return>",
                                lambda e: email_id_entry.focus)
            password_entry.place(relx=0.5, rely=0.5)

            email_id_label = Label(edit_account_frame,
                                   text="Enter the Email ID:",
                                   bg='black', fg='white')
            email_id_label.place(relx=0.1, rely=0.7)
            email_id_entry = Entry(edit_account_frame, width=23)
            email_id_entry.insert(0, data[2])
            email_id_entry.place(relx=0.5, rely=0.7)

            # --------------------------------------------------------
            # defining submit function
            def submit():
                if messagebox.askyesno("?", "do you want to "
                                            "save changes? ") == TRUE:
                    query1 = 'update user_password set ' \
                             'user_name= "%s", password= "%s" , ' \
                             'email= "%s"'
                    # checking validity of email id
                    if validate_email(email_id_entry.get()) == TRUE:
                        entry_get((user_id_entry, password_entry,
                                   email_id_entry), query1)
                        edit_account_frame.destroy()
                    else:
                        messagebox.showerror("error", "Invalid email")
                else:
                    edit_account_frame.destroy()
            # --------------------------------------------------------

            submit_button = Button(edit_account_frame, text="submit",
                                   command=submit)
            submit_button.place(relx=0.1, rely=0.82)

            cancel_button = Button(edit_account_frame, text="Cancel",
                                   command=lambda:
                                   edit_account_frame.destroy())
            cancel_button.place(relx=0.75, rely=0.82)
        # -------------------------------------------------------------
        edit_account = Button(accounts_frame, text="Edit Account",
                              width=40, height=2, bg="white",
                              command=editaccount)
        edit_account.place(relx=0.04, rely=0.3)

        # -------------------------------------------------------------
        # defining sign out function
        def signout():
            sign_out_frame = Frame(screen, bg='white')
            sign_out_frame.place(x=0, y=0, relheight=1, relwidth=1)
            if messagebox.askyesno('?', "Sign out?") == TRUE:
                my_con = my.connect(host='sql11.freemysqlhosting.net',
                                    user='sql11422143',
                                    passwd='pq3EcPFj4e',
                                    db='sql11422143')
                cur = my_con.cursor()
                # update login status
                query = "update user_password set status='NO' "
                cur.execute(query)
                my_con.commit()
                my_con.close()
                screen.destroy()
                import sys
                sys.exit()
            else:
                sign_out_frame.destroy()
        # -------------------------------------------------------------
        sign_out = Button(accounts_frame, text="Sign out", width=15,
                          height=2, command=signout, bg='white')
        sign_out.place(relx=0.3, rely=0.5)

        close_button1 = Button(accounts_frame, text="Close",
                               command=lambda:
                               accounts_frame.destroy(),
                               width=7, height=1, bg='white')
        close_button1.place(relx=0.79, rely=0.9)

    # ----------------------------------------------------------------
    account_image = ImageTk.PhotoImage(Image.open("images/account "
                                                  "button image.png"))
    account_button = Button(screen, image=account_image, bg="black",
                            command=accounts)
    account_button.place(relx=0.93, rely=0.008)
    account_button.image = account_image

    # -----------------------------------------------------------------
    # defining printing function
    def printing():
        if messagebox.askyesno("?", "Do you want to print the "
                                    "treeview data? ") == TRUE:
            heading = []
            if treeview.get_children() == ():
                messagebox.showerror("!", "No data to print")
            else:
                for i in range(1, (len(treeview["columns"]))+1):
                    head = treeview.heading(i)["text"]
                    heading.append(head)            # list of headings

                import xlsxwriter                       # excel writer
                workbook = xlsxwriter.Workbook('printing.xlsx')
                worksheet = workbook.add_worksheet("library")
                row = 0
                column = 0
                for a in heading:
                    # placing the headings
                    worksheet.write(row, column, a)
                    # width of cell according to word
                    worksheet.set_column(column, column, len(a))
                    column += 1

                row_tup = ()
                len_list = []
                for i in treeview.get_children():
                    # creating list and tuple of treeview row data
                    row_tup += ((treeview.item(i)["values"]),)
                    len_list += (treeview.item(i)["values"])

                row = 1
                column = 0
                n = len(row_tup[0])        # number of columns
                for a in row_tup:
                    for i in a:
                        # inserting each row
                        worksheet.write(row, column, i)
                        column += 1
                    row += 1
                    column = 0

                for i in range(n):
                    col_len = ()
                    x = i
                    col_len += ((len(heading[i])),)
                    col_len += ((len(str(len_list[x]))),)
                    # finding length of all data in a column
                    while x < ((len(len_list))-n):
                        if type(len_list[x+n]) == int:
                            col_len += (5,)
                        else:
                            col_len += (len(str(len_list[x + n])),)
                        x += n

                    # finding the maximum length in a column
                    width = max(col_len)
                    # size of the column according to largest length
                    worksheet.set_column(i, i, width+2)
                workbook.close()
                import os
                # printing command
                os.startfile("printing.xlsx", "print")
                # give 20 secs for system to give print command
                time.sleep(20)
                os.remove("printing.xlsx")
        else:
            return

    print_image = ImageTk.PhotoImage(Image.open("images/print"
                                                " button image.png"))
    print_button = Button(screen, image=print_image, bg='black',
                          command=printing)
    if treeview != '':
        print_button.place(relx=0.83, rely=0.008)
    print_button.image = print_image

    # menu
    menu = Menu(screen, bg='black')
    screen.config(menu=menu)    # commands disabled if on that page

    if screen_ == 'screen':
        menu.add_command(label='Homepage',
                         command=lambda: homepage(screen),
                         state=DISABLED)
    else:
        menu.add_command(label='Homepage',
                         command=lambda: homepage(screen))

    if screen_ == 'bk_screen':
        menu.add_command(label='Books', state=DISABLED)
    else:
        menu.add_command(label='Books', command=lambda: books(screen))

    if screen_ == 'members_screen':
        menu.add_cascade(label='Members', state=DISABLED)
    else:
        menu.add_cascade(label='Members',
                         command=lambda: members(screen))

    if screen_ == 'funds_screen':
        menu.add_cascade(label='Funds', state=DISABLED)
    else:
        menu.add_cascade(label='Funds', command=lambda: funds(screen))

    if screen_ == 'info_screen':
        menu.add_cascade(label='Developers Info', state=DISABLED)
    else:
        menu.add_cascade(label='Developers Info', command=lambda: dev_info(screen))


# -------------Books Functions---------------------------------------#
# book entry----------------------
def delete(tup):
    for i in tup:
        i.delete(0, END)


def disable(tup):
    for i in tup:
        i.config(state=DISABLED)


def normal(tup):
    for i in tup:
        i.config(state=NORMAL)


def insert(tup, tup1):
    len_ = len(tup)
    for i in range(len_):
        tup[i].insert(0, str(tup1[i]))


# Getting Entry Function---------------------
def entry_get(entries, query, extra=()):
    # get the data from entries and execute the given query
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur = my_con.cursor()
    tup = ()
    for entry in entries:
        if entry.get() == '':
            messagebox.showerror('ERROR', 'Field Cant be Empty')
            break
        else:
            x = entry.get()
            tup = tup + (x,)
    else:
        if extra == ():
            tup = tup
        else:
            tup = tup + extra

        try:
            cur.execute(query % tup)
            my_con.commit()
        except my.Error as er:
            messagebox.showerror("Error", er.msg)
    my_con.close()


# Update treeview function----------------------------------------
def update(treeview, table, id_, extra='ASC'):
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur = my_con.cursor()
    query = 'Select * from %s order by %s %s' % (table, id_, extra)
    cur.execute(query)
    data = cur.fetchall()
    my_con.close()

    if not data:
        for row1 in treeview.get_children():
            treeview.delete(row1)
        no_record_label = Label(treeview, text="No Records",
                                font=("times new roman", 16),
                                bg="white", fg="grey")
        no_record_label.place(relx=0.45, rely=0.45)
    else:
        for row1 in treeview.get_children():
            treeview.delete(row1)
        for row in data:
            treeview.insert('', 'end', values=row)


# Generate Name using ID----------------------------------------------
def insert_name(entry, name_entry, id_column, name_column, focus_,
                table='books'):
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur = my_con.cursor()
    _id = entry.get()
    query = 'select %s from %s where %s="%s" ' % (name_column, table,
                                                  id_column, _id)
    cur.execute(query)
    data = cur.fetchall()
    if data:
        name_entry.config(state=NORMAL)
        name_entry.delete(0, END)
        name_entry.insert(0, (data[0])[0])
        name_entry.config(state=DISABLED)
        focus_.focus()
        if name_column == 'members_name':
            focus_.drop_down()
    else:
        focus_.focus_set()
        messagebox.showerror("ERROR", "ID not found!")
        entry.delete(0, END)
        name_entry.config(state=DISABLED)
        entry.focus()
    my_con.close()


# Search function----------------------------------------------------
def search(tup, tree, query, entry):
    from tkinter import messagebox
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    tup1 = ()
    for i in tup:
        tup1 = tup1 + (("%" + i + "%"),)
    cur = my_con.cursor()
    cur.execute(query % tup1)
    data = cur.fetchall()

    if not data:
        if messagebox.askretrycancel('No record', 'No Records Found')\
                == FALSE:
            entry.delete(0, END)

    else:
        for row1 in tree.get_children():
            tree.delete(row1)
        for row1 in data:
            tree.insert('', 'end', value=row1)
