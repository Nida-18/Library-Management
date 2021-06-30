# FUNDS WINDOW
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as my
import tkinter.ttk as tk
import replicate as r
from tkinter import messagebox


# --------------------Resize image function--------------------------#
def resize(event):
    new_width = event.width
    new_height = event.height
    copy_of_image = image1.copy()
    img = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(img)
    label1.config(image=photo)
    label1.image = photo


# ----------------------Main function--------------------------------#
def funds(a):
    global image1   # globalising variables to be used outside function
    global label1
    global b

    b = a
    funds_screen = Tk()
    funds_screen.title('Funds')
    funds_screen.state('zoomed')
    funds_screen.resizable(0, 0)
    funds_screen.iconbitmap("images/"
                            "funds icon.ico")
    image1 = Image.open("images"
                        "/book1.jpeg")
    bg = ImageTk.PhotoImage(image1)
    label1 = Label(funds_screen, image=bg)
    label1.bind('<Configure>', resize)
    label1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1.0)
    col = '#96978f'

    # ----------------------------------------------------------------
    # defining members details
    def funds_details():
        # Creating Frame and inserting labels, entries and button-----
        funds_frame = LabelFrame(funds_screen, text='Funds', bd=15,
                                 bg=col, relief=RIDGE,
                                 font=('times new roman', 10, "bold"))
        funds_frame.place(x=100, y=180, height=550,
                          width=1320)

        search_label = Label(funds_frame, text='Search', bg='black',
                             fg='white')
        search_label.place(relx=0.13, rely=0.01, height=30)
        search_entry = Entry(funds_frame, width=117, relief=GROOVE)
        search_entry.place(relx=0.175, rely=0.01, height=30)

        id_label = Label(funds_frame, text='Fund ID', width=13, bd=2,
                         bg='black', fg='white')
        id_label.place(relx=0.03, rely=0.62)
        id_entry = Entry(funds_frame, width=60)
        id_entry.bind('<Return>', lambda e: name_entry.focus_set())
        id_entry.place(relx=0.13, rely=0.62)

        name_label = Label(funds_frame, text='Name', width=13, bd=2,
                           bg='black', fg='white')
        name_label.place(relx=0.47, rely=0.62)
        name_entry = Entry(funds_frame, width=60)
        name_entry.bind('<Return>', lambda e: amount_entry.focus_set()
                        )
        name_entry.place(relx=0.55, rely=0.62)

        amount_label = Label(funds_frame, text="Amount", width=13,
                             bd=2, bg='black', fg='white')
        amount_label.place(relx=0.03, rely=0.734)
        amount_entry = Entry(funds_frame, width=60)
        amount_entry.bind('<Return>', lambda e: cause_entry.focus_set(
        ))
        amount_entry.place(relx=0.13, rely=0.734)

        cause_label = Label(funds_frame, text='Charity/Fine',
                            width=13, bd=2,  bg='black', fg='white')
        cause_label.place(relx=0.47, rely=0.734)
        cause_entry = tk.Combobox(funds_frame, width=57)
        cause_entry['values'] = ('Fine', 'Charity')
        cause_entry.place(relx=0.55, rely=0.734)

        entry_tup = (id_entry, name_entry, amount_entry, cause_entry)
        r.delete(entry_tup)
        r.disable(entry_tup)  # Disabling entries
        # Search Option--------------------------------------
        query1 = 'select*from funds where funds_id like ("%s") ' \
                 'or name like ("%s") ' \
                 'or amount like ("%s") or cause like ("%s")'

        search_img = ImageTk.PhotoImage(Image.open("images/search "
                                                   "image.jpg"))

        ent = (search_entry.get()*4)
        search_entry.bind('<Return>', lambda e: r.search((
            search_entry.get(), search_entry.get(),
            search_entry.get(), search_entry.get()),
                                                         fund_tree,
                                                         query1,
                                                         search_entry)
                          )  # enabling enter key
        search_button = Button(funds_frame,
                               command=lambda: r.search((
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get()),
                                                        fund_tree,
                                                        query1,
                                                        search_entry),
                               text='search', image=search_img)
        search_button.place(relx=0.84, rely=0.01, height=30, width=40)
        search_button.image = search_img

        # ------------------------------------------------------------
        # defining selection of each row
        def select(event):
            cur_item = fund_tree.focus()
            row_info = fund_tree.item(cur_item)
            row_list = row_info['values']

            r.normal(entry_tup)
            r.delete(entry_tup)
            r.insert(entry_tup, row_list)
            cause_entry.config(state='readonly')
            org_id = id_entry.get()
            r.disable(entry_tup)

            # --------------------------------------------------------
            # defining delete button
            def delete():
                if messagebox.askyesno('?', 'Delete Record?') \
                        == FALSE:
                    funds_details()
                else:
                    my_con3 = my.connect(host='sql11.freemysqlho'
                                              'sting.net',
                                         user='sql11422143',
                                         passwd='pq3EcPFj4e',
                                         db='sql11422143')
                    cur3 = my_con3.cursor()

                    query3 = "delete from funds where funds_id='%s'"\
                             % (org_id,)
                    cur3.execute(query3)
                    my_con3.commit()
                    r.update(fund_tree, 'funds', 'funds_id')
                    my_con3.close()

                    r.delete(entry_tup)
                    r.disable(entry_tup)

                    funds_details()

                # ----------------------------------------------------
            delete_button.config(state=NORMAL, command=delete)
            # --------------------------------------------------------
        delete_button = Button(funds_frame, text='Delete the record',
                               width=15, height=2, state=DISABLED)
        delete_button.place(relx=0.82, rely=0.26)

        # ------------------------------------------------------------
        # defining add button
        def add():
            name_entry.focus()
            fund_tree.config(selectmode=NONE)
            add_button.destroy()
            r.normal(entry_tup)
            r.delete(entry_tup)
            cause_entry.config(state='readonly')

            # entering funds_id
            my_con2 = my.connect(host='sql11.freemysqlhosting.net',
                                 user='sql11422143',
                                 passwd='pq3EcPFj4e',
                                 db='sql11422143')
            cur2 = my_con2.cursor()
            query2 = "select funds_id from funds"
            cur2.execute(query2)
            data2 = cur2.fetchall()
            my_con2.close()

            if not data2:
                y = 1
            else:
                id_ = ()
                for row2 in data2:
                    y = int("".join(filter(str.isdigit, row2[0])))
                    id_ += (y,)
                y = max(id_) + 1
            if y < 100:
                f_id = "FN00" + str(y)
            elif 100 <= y <= 1000:
                f_id = "FN0" + str(y)
            else:
                f_id = "FN" + str(y)

            id_entry.insert(0, f_id)
            id_entry.config(state=DISABLED)

            # --------------------------------------------------------
            # defining submit button
            def submit():
                query4 = 'insert into funds values("%s","%s",' \
                         '"%s","%s")'
                r.entry_get(entry_tup, query4)
                r.update(fund_tree, 'funds', 'funds_id')

                r.delete(entry_tup)
                funds_details()

            # --------------------------------------------------------
            submit_button = Button(funds_frame, text='Submit',
                                   width=15, height=2, command=submit)
            submit_button.place(relx=0.82, rely=0.105)

            # --------------------------------------------------------
            # defining cancel button
            def cancel():
                funds_details()

            # --------------------------------------------------------
            cancel_button = Button(funds_frame, text='Cancel',
                                   width=15, height=2, command=cancel)
            cancel_button.place(relx=0.82, rely=0.26)

        # ------------------------------------------------------------
        add_button = Button(funds_frame, text='Add Record', width=15,
                            height=2, command=add)
        add_button.place(relx=0.82, rely=0.105)

        # creating the treeview
        fund_tree = tk.Treeview(funds_frame, column=(1, 2, 3, 4),
                                show='headings')
        fund_tree.heading(1, text='Fund ID')
        fund_tree.column(1, minwidth=0, width=100, stretch=NO)
        fund_tree.heading(2, text='Name')
        fund_tree.column(2, minwidth=0, width=350, stretch=NO)
        fund_tree.heading(3, text='Amount')
        fund_tree.column(3, minwidth=0, width=155, stretch=NO)
        fund_tree.heading(4, text='Charity/Fine')
        fund_tree.column(4, minwidth=50, width=200)

        fund_tree.bind('<<TreeviewSelect>>', select)
        r.update(fund_tree, 'funds', 'funds_id')
        fund_tree.place(relx=0.13, rely=0.105)
        r.menubar(funds_screen, 'funds_screen', fund_tree, b)

        # creating scrollbar
        scroll = Scrollbar(funds_frame, orient=VERTICAL,
                           command=fund_tree.yview)
        scroll.place(relx=0.76, rely=0.105, height=225)
        fund_tree.configure(yscrollcommand=scroll.set)

        # displaying total fund
        my_con0 = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
        cur0 = my_con0.cursor()

        query0 = "select amount from funds"
        cur0.execute(query0)
        data0 = cur0.fetchall()
        amount = 0
        for i in data0:
            for j in i:
                amount += j
        amount_label = Label(funds_frame, text='Total fund = "%s"$'
                                               % (amount,))
        amount_label.place(relx=0.66, rely=0.53)

    funds_details()
    # ----------------------------------------------------------------

    funds_screen.mainloop()
