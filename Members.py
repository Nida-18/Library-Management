# MEMBERS WINDOW
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as my
import tkinter.ttk as tk
import replicate as r
import tkcalendar
from datetime import date as d
from tkinter import messagebox


# -----------------------Resize image function-----------------------#
def resize(event):
    new_width = event.width
    new_height = event.height
    copy_of_image = image1.copy()
    img = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(img)
    label1.config(image=photo)
    label1.image = photo


# ---------------------------Main function---------------------------#
def members(a):
    global image1   # globalising variables to be used outside function
    global label1
    global b

    b = a
    members_screen = Tk()
    members_screen.title('Members')
    members_screen.state('zoomed')
    members_screen.resizable(0, 0)
    members_screen.iconbitmap("images/"
                              "Members icon.ico")
    image1 = Image.open("images"
                        "/book1.jpeg")
    bg = ImageTk.PhotoImage(image1)
    label1 = Label(members_screen, image=bg)
    label1.bind('<Configure>', resize)
    label1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1.0)
    col = '#96978f'

    # ----------------------------------------------------------------
    # defining members details
    def members_details():
        # Creating Frame and inserting labels, entries and button-----
        members_frame = LabelFrame(members_screen,
                                   text='Members Details', bd=15,
                                   bg=col, relief=RIDGE,
                                   font=('times new roman', 10,
                                          "bold"))
        members_frame.place(x=200, y=180, height=550,
                            width=1115)
        search_label = Label(members_frame, text='Search',
                             bg='black', fg='white')
        search_label.place(relx=0.12, rely=0.01, height=30)
        search_entry = Entry(members_frame, width=90, relief=GROOVE)
        search_entry.place(relx=0.174, rely=0.01, height=30)

        id_label = Label(members_frame, text='Member ID', width=13,
                         bd=2, bg='black', fg='white')
        id_label.place(relx=0.03, rely=0.61)
        id_entry = Entry(members_frame, width=60)
        id_entry.bind('<Return>', lambda e: name_entry.focus_set())
        id_entry.place(relx=0.125, rely=0.61)

        name_label = Label(members_frame, text='Member Name',
                           width=13, bd=2, bg='black', fg='white')
        name_label.place(relx=0.03, rely=0.794)
        name_entry = Entry(members_frame, width=60)
        name_entry.bind('<Return>', lambda e: date_entry.focus())
        name_entry.place(relx=0.125, rely=0.794)

        date_label = Label(members_frame, text="Date of joining",
                           width=13, bd=2, bg='black', fg='white')
        date_label.place(relx=0.52, rely=0.61)
        date_entry = tkcalendar.DateEntry(members_frame, width=57)
        date_entry.bind('<Return>',
                        lambda e: contact_no_entry.focus_set())
        date_entry.place(relx=0.61, rely=0.61)
        date_entry.config(maxdate=d.today())

        contact_no_label = Label(members_frame, text='Contact Number',
                                 width=13, bd=2,  bg='black',
                                 fg='white')
        contact_no_label.place(relx=0.52, rely=0.794)
        contact_no_entry = Entry(members_frame, width=60)
        contact_no_entry.place(relx=0.61, rely=0.794)

        entry_tup = (id_entry, name_entry, date_entry,
                     contact_no_entry)
        r.delete(entry_tup)
        r.disable(entry_tup)  # Disabling entries

        # Search Option--------------------------------------
        query1 = 'select*from members where members_id like ("%s") ' \
                 'or members_name like ("%s") ' \
                 'or date_of_joining like ("%s") or ' \
                 'contact_number like ("%s")'

        search_img = ImageTk.PhotoImage(Image.open("images/search"
                                                   " image.jpg"))

        search_entry.bind('<Return>', lambda e: r.search((
            search_entry.get(), search_entry.get(),
            search_entry.get(), search_entry.get()),
                                                         mem_tree,
                                                         query1,
                                                         search_entry)
                          )  # enabling enter key
        search_button = Button(members_frame,
                               command=lambda: r.search((
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get()),
                                                        mem_tree,
                                                        query1,
                                                        search_entry),

                               text='search', image=search_img)
        search_button.place(relx=0.83, rely=0.01, height=30, width=40)
        search_button.image = search_img

        # ------------------------------------------------------------
        # defining selection of each row
        def select(event):
            cur_item = mem_tree.focus()
            row_info = mem_tree.item(cur_item)
            row_list = row_info['values']

            r.normal(entry_tup)
            r.delete(entry_tup)
            r.insert(entry_tup, row_list)
            org_id = id_entry.get()
            r.disable(entry_tup)

            # --------------------------------------------------------
            # defining view button function
            def view():
                edit_button.config(state=DISABLED)
                add_button.config(state=DISABLED)
                my_con2 = my.connect(host='sql11.freemysql'
                                          'hosting.net',
                                     user='sql11422143',
                                     passwd='pq3EcPFj4e',
                                     db='sql11422143')
                cur2 = my_con2.cursor()

                query2 = 'select book_reg, book_name, ' \
                         'date_of_issue, proposed_date_of_return,' \
                         ' status from issue_books where ' \
                         'members_id="%s" order by status' % (org_id,)
                cur2.execute(query2)
                data3 = cur2.fetchall()
                num = len(data3)
                my_con2.close()

                view_frame = LabelFrame(members_frame, text='View',
                                        bg=col,
                                        relief=RIDGE,
                                        font=('times new roman', 10,
                                              "bold"))
                view_frame.place(relx=0.237, rely=0.1, relheight=0.5,
                                 relwidth=0.6)

                id_text_label = Label(view_frame, text='Members ID: '
                                                       '"%s"' %
                                                       (org_id,),
                                      bg=col, fg='black',
                                      font=('times new roman', 10,
                                            "bold"))
                id_text_label.place(relx=0.03, rely=0.05)

                no_text_label = Label(view_frame, text='No Of Books '
                                                       'Borrowed: '
                                                       '"%s"' % num,
                                      bg=col, fg='black',
                                      font=('times new roman', 10,
                                            "bold"))
                no_text_label.place(relx=0.37, rely=0.05)

                view_tree = tk.Treeview(view_frame, column=(1, 2, 3,
                                                            4, 5),
                                        show='headings')
                view_tree.heading(1, text="Book's ID")
                view_tree.column(1, minwidth=50, width=80)
                view_tree.heading(2, text="Book's Name")
                view_tree.column(2, minwidth=50, width=125)
                view_tree.heading(3, text="Date Of Issue")
                view_tree.column(3, minwidth=50, width=80)
                view_tree.heading(4, text="Proposed Date Of Return")
                view_tree.column(4, minwidth=50, width=150)
                view_tree.heading(5, text='Status')
                view_tree.column(5, minwidth=50, width=60)
                view_tree.place(relx=0.05, rely=0.2, relheight=0.4)

                scroll_view = Scrollbar(view_frame, orient=VERTICAL,
                                        command=view_tree.yview)
                scroll_view.place(relx=0.93, rely=0.2, relheight=0.4)
                view_tree.configure(yscrollcommand=scroll_view.set)

                for row1 in view_tree.get_children():
                    view_tree.delete(row1)
                for row1 in data3:
                    view_tree.insert('', 'end', value=row1)

                # ----------------------------------------------------
                # defining close button function
                def close():
                    members_details()

                # ----------------------------------------------------
                close_button = Button(view_frame, text='Close',
                                      command=close, width=15)
                close_button.place(relx=0.4, rely=0.85)

            # --------------------------------------------------------
            view_button = Button(members_frame, text="View", width=15,
                                 height=2, command=view)
            view_button.place(relx=0.80, rely=0.26)

            # --------------------------------------------------------
            # defining edit button
            def edit():
                mem_tree.config(selectmode=NONE)
                edit_button.config(state=DISABLED)
                r.normal(entry_tup)
                date_entry.config(state="readonly")
                id_entry.config(state=DISABLED)
                add_button.destroy()

                # ----------------------------------------------------
                # defining change button
                def changes():
                    mem_tree.config(selectmode=BROWSE)
                    entries = name_entry, contact_no_entry

                    query2 = 'update members '\
                             ' set members_name="%s", ' \
                             'contact_number="%s",' \
                             'date_of_joining="%s"' \
                             ' where members_id="%s"'
                    r.entry_get(entries, query2,
                                extra=(date_entry.get_date(), org_id,)
                                )  # changing values
                    r.update(mem_tree, 'members',
                             'members_id')     # showing updated data

                    r.disable(entry_tup)
                    members_details()

                # ----------------------------------------------------
                changes_button = Button(members_frame,
                                        text='Save Changes', width=15,
                                        height=2, command=changes)
                changes_button.place(relx=0.80, rely=0.109)

                # ----------------------------------------------------
                # defining delete button
                def delete():
                    if messagebox.askyesno("?", "Do youwant to "
                                                "Delete?") == TRUE:
                        my_con3 = my.connect(host='sql11.freemys'
                                                  'qlhosting.net',
                                             user='sql11422143',
                                             passwd='pq3EcPFj4e',
                                             db='sql11422143')
                        cur3 = my_con3.cursor()

                        query3 = "delete from members where " \
                                 "members_id='%s'" % (org_id,)
                        cur3.execute(query3)
                        my_con3.commit()
                        r.update(mem_tree, 'members', 'members_id')
                        my_con3.close()

                        r.delete(entry_tup)
                        r.disable(entry_tup)

                        members_details()
                    else:
                        members_details()

                # ----------------------------------------------------
                delete_button = Button(members_frame,
                                       text='Delete the record',
                                       width=15, height=2,
                                       command=delete)
                delete_button.place(relx=0.80, rely=0.262)

                # ----------------------------------------------------
                # defining cancel button
                def cancel():
                    members_details()

                # ----------------------------------------------------
                cancel_button1 = Button(members_frame, text='Cancel',
                                        width=15, height=2,
                                        command=cancel)
                cancel_button1.place(relx=0.80, rely=0.42)

            # --------------------------------------------------------
            edit_button.config(state=NORMAL, command=edit)

        # ------------------------------------------------------------
        edit_button = Button(members_frame, text="Edit", width=15,
                             height=2, state=DISABLED)
        edit_button.place(relx=0.80, rely=0.107)

        # ------------------------------------------------------------
        # defining add button
        def add():
            mem_tree.config(selectmode=NONE)
            edit_button.destroy()
            add_button.destroy()
            r.normal(entry_tup)
            date_entry.config(state="readonly")
            r.delete(entry_tup)

            # --------------------------------------------------------
            # defining submit button
            def submit():
                query4 = 'insert into members(Members_Id,' \
                         ' Members_Name, Contact_number,' \
                         ' date_of_joining)' \
                         ' values("%s","%s","%s","%s")'
                r.entry_get(entry_tup[:2] + (entry_tup[3],), query4,
                            extra=(date_entry.get_date(),))
                r.update(mem_tree, "members", 'members_id')

                r.delete(entry_tup)
                members_details()

            # --------------------------------------------------------
            submit_button = Button(members_frame, text='Submit',
                                   width=15, height=2, command=submit)
            submit_button.place(relx=0.80, rely=0.107)

            # --------------------------------------------------------
            # defining cancel button
            def cancel():
                members_details()

            # --------------------------------------------------------
            cancel_button = Button(members_frame, text='Cancel',
                                   width=15, height=2, command=cancel)
            cancel_button.place(relx=0.80, rely=0.262)

        # ------------------------------------------------------------
        add_button = Button(members_frame, text='Add Record',
                            width=15, height=2, command=add)
        add_button.place(relx=0.80, rely=0.42)

        # creating the treeview
        mem_tree = tk.Treeview(members_frame, column=(1, 2, 3, 4),
                               show='headings')
        mem_tree.heading(1, text='Members ID')
        mem_tree.column(1, minwidth=0, width=125, stretch=NO)
        mem_tree.heading(2, text='Members Name')
        mem_tree.column(2, minwidth=0, width=250, stretch=NO)
        mem_tree.heading(3, text='Date of Joining')
        mem_tree.column(3, minwidth=0, width=125, stretch=NO)
        mem_tree.heading(4, text="Contact Number")
        mem_tree.column(4, minwidth=0, width=125, stretch=NO)

        mem_tree.bind('<<TreeviewSelect>>', select)
        r.update(mem_tree, 'members', 'members_id')
        mem_tree.place(relx=0.12, rely=0.105)
        r.menubar(members_screen, 'members_screen', mem_tree, b)

        # creating scrollbar
        scroll = Scrollbar(members_frame, orient=VERTICAL,
                           command=mem_tree.yview)
        scroll.place(relx=0.75, rely=0.105, height=225)
        mem_tree.configure(yscrollcommand=scroll.set)

    members_details()
    # ----------------------------------------------------------------

    members_screen.mainloop()
