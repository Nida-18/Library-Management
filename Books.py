# BOOK WINDOW
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as my
import tkinter.ttk as tk
import replicate as r
import tkcalendar
from tkinter import messagebox
import datetime as dt
from datetime import date as d


# ------------------Resize image function----------------------------#
def resize(event):
    new_width = event.width
    new_height = event.height
    copy_of_image = image1.copy()
    img = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(img)
    label1.config(image=photo)
    label1.image = photo


# -----------------------Update information--------------------------#
def update():
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur = my_con.cursor()

    tday = d.today()             # gets today's date
    query = 'select proposed_date_of_return, issue_id ' \
            ' from issue_books'
    cur.execute(query)
    data = cur.fetchall()
    for i in data:              # update no of days left
        left = (i[0]-tday).days
        id_ = i[1]
        query = 'update issue_books set no_of_days_left=%s where ' \
                'issue_id="%s" and status="Issued"' % (left, id_)
        cur.execute(query)
        my_con.commit()
    query = 'select no_of_days_left, issue_id from issue_books' \
            ' where status="Issued"'
    cur.execute(query)
    data = cur.fetchall()
    for i in data:            # update fine
        import math
        lef = i[0]
        if lef <= 0:
            id_ = i[1]
            fine = (math.fabs(lef))*3
            query = 'update issue_books set fine=%s where' \
                    ' issue_id="%s"' % (fine, id_)
            cur.execute(query)
            my_con.commit()
    my_con.close()


# --------------------------Main function----------------------------#
def book(a):
    global image1  # globalising variables to be used outside function
    global label1
    global b

    b = a
    bk_screen = Tk()
    bk_screen.title('Books')
    bk_screen.state('zoomed')
    bk_screen.resizable(0, 0)
    bk_screen.iconbitmap("images/Book icon.ico")
    image1 = Image.open("images/book1.jpeg")
    bg = ImageTk.PhotoImage(image1)
    label1 = Label(bk_screen, image=bg)
    label1.bind('<Configure>', resize)
    label1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1.0)
    col = '#96978f'   # grey

    # ----------------------------------------------------------------
    # defining book details button
    def bk_detail():
        update()

        # Creating Frame and inserting labels, entries and button-----
        dt_frame = LabelFrame(bk_screen, text='BOOK DETAILS', bd=15,
                              bg=col,
                              relief=RIDGE, font=('times new roman',
                                                  10, "bold"))
        dt_frame.place(x=50, y=150, height=550,
                       width=1355)

        search_label = Label(dt_frame, text='Search', bg='black',
                             fg='white')
        search_label.place(relx=0.03, rely=0.01, height=30)
        search_entry = Entry(dt_frame, width=155, relief=GROOVE)
        search_entry.place(relx=0.075, rely=0.01, height=30)

        id_label = Label(dt_frame, text='Book ID', width=13, bd=2,
                         bg='black', fg='white')
        id_label.place(relx=0.03, rely=0.55)
        id_entry = Entry(dt_frame, width=58)
        id_entry.bind('<Return>', lambda e: genre_entry.focus())
        id_entry.place(relx=0.13, rely=0.55)

        name_label = Label(dt_frame, text='Book Name', width=13, bd=2,
                           bg='black', fg='white')
        name_label.place(relx=0.48, rely=0.55)
        name_entry = Entry(dt_frame, width=58)
        name_entry.bind('<Return>', lambda e: author_entry.focus())
        name_entry.place(relx=0.58, rely=0.55)

        genre_label = Label(dt_frame, text="Genre", width=13,  bd=2,
                            bg='black', fg='white')
        genre_label.place(relx=0.03, rely=0.664)
        genre_entry = Entry(dt_frame, width=58)
        genre_entry.bind('<Return>', lambda e: pub_entry.focus())
        genre_entry.place(relx=0.13, rely=0.664)

        author_label = Label(dt_frame, text='Author', width=13,  bd=2,
                             bg='black', fg='white')
        author_label.place(relx=0.48, rely=0.664)
        author_entry = Entry(dt_frame, width=58)
        author_entry.bind('<Return>',
                          lambda e: year_of_pub_entry.focus())
        author_entry.place(relx=0.58, rely=0.664)

        pub_label = Label(dt_frame, text='Publication', width=13,
                          bd=2, bg='black', fg='white')
        pub_label.place(relx=0.03, rely=0.778)
        pub_entry = Entry(dt_frame, width=58)
        pub_entry.bind('<Return>', lambda e: num_entry.focus())
        pub_entry.place(relx=0.13, rely=0.778)

        year_now = d.today().year
        year_of_pub_label = Label(dt_frame, text='Publication Year',
                                  width=13,  bd=2, bg='black',
                                  fg='white')
        year_of_pub_label.place(relx=0.48, rely=0.778)
        year_of_pub_entry = Spinbox(dt_frame, from_=year_now-100,
                                    to=year_now, width=57)
        year_of_pub_entry.bind('<Return>', lambda e: id_entry.focus())
        year_of_pub_entry.delete(0, END)
        year_of_pub_entry.place(relx=0.58, rely=0.778)

        num_label = Label(dt_frame, text='Number Of Books', width=13,
                          bd=2, bg='black', fg='white')
        num_label.place(relx=0.03, rely=0.892)
        num_entry = Entry(dt_frame,  width=58)
        num_entry.bind('<Return>', lambda e: name_entry.focus())
        num_entry.place(relx=0.13, rely=0.892)

        entry_tup = (id_entry, name_entry, author_entry, genre_entry,
                     pub_entry, year_of_pub_entry, num_entry)
        r.disable(entry_tup)  # Disabling entries

        # Search Option--------------------------------------
        query1 = 'select*from books where book_name like ("%s") ' \
                 'or book_reg like ("%s") ' \
                 'or author like ("%s") or genre like ("%s") ' \
                 'or publication like ("%s") or year_of_publication' \
                 ' like ("%s") or no_books like ("%s")'

        # enabling enter key
        search_entry.bind('<Return>', lambda e: r.search((
            search_entry.get(), search_entry.get(),
            search_entry.get(), search_entry.get(),
            search_entry.get(), search_entry.get(),
            search_entry.get()), detail, query1, search_entry))

        search_img = ImageTk.PhotoImage(Image.open("images/search"
                                                   " image.jpg"))
        search_button = Button(dt_frame,
                               command=lambda: r.search((
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get()),
                                   detail, query1, search_entry),
                               text='search', image=search_img)
        search_button.place(relx=0.915, rely=0.01, height=30,
                            width=40)
        search_button.image = search_img

        # ------------------------------------------------------------
        # defining selection of each row
        def select(event):
            cur_item = detail.focus() # index for treeview
            row_info = detail.item(cur_item) # dict
            # gives list of data in selected row of treeview
            row_list = row_info['values'] # values

            r.normal(entry_tup)
            r.delete(entry_tup)
            r.insert(entry_tup, row_list)   # replicate-file to insert
            org_id = id_entry.get()           # get the book id
            r.disable(entry_tup)

            # --------------------------------------------------------
            # defining view button function
            def view():  # readonly window display  book's issue info
                edit_button.config(state=DISABLED)
                add_button.config(state=DISABLED)
                my_con2 = my.connect(host='sql11.freemysqlhosting'
                                          '.net',
                                     user='sql11422143',
                                     passwd='pq3EcPFj4e',
                                     db='sql11422143')
                cur2 = my_con2.cursor()
                query2 = 'select No_books from books where' \
                         ' book_reg="%s"' % (org_id,)
                cur2.execute(query2)
                data2 = cur2.fetchone()

                query2 = 'select members_id, members_name,' \
                         ' date_of_issue, proposed_date_of_return' \
                         ' from issue_books where book_reg="%s" ' \
                         'and status="Issued"' % (org_id,)
                cur2.execute(query2)
                data3 = cur2.fetchall()
                num = len(data3)
                my_con2.close()

                view_frame = LabelFrame(dt_frame, text='View', bg=col,
                                        relief=RIDGE, font=('times'
                                                            ' new'
                                                            ' roman',
                                                            10, "bold"
                                                            ))
                view_frame.place(relx=0.35, rely=0.1, relheight=0.5,
                                 relwidth=0.4)

                id_text_label = Label(view_frame, text='Book ID: "%s"'
                                                       % (org_id,),
                                      bg=col, fg='black',
                                      font=('times new roman',
                                            10, "bold"))
                id_text_label.place(relx=0.03, rely=0.05)

                no_text_label = Label(view_frame, text='Total No Of '
                                                       'Books: "%s"'
                                                       % data2,
                                      bg=col, fg='black',
                                      font=('times new roman',
                                            10, "bold"))
                no_text_label.place(relx=0.37, rely=0.05)

                issue_no_label = Label(view_frame, text='No of Books'
                                                        ' Issued:"%s"'
                                                        % (num,),
                                       bg=col, fg='black',
                                       font=('times new roman', 10,
                                             "bold"))
                issue_no_label.place(relx=0.72, rely=0.05)

                view_tree = tk.Treeview(view_frame, column=(1, 2, 3, 4
                                                            ),
                                        show='headings')
                view_tree.heading(1, text="Member's ID")
                view_tree.column(1, minwidth=50, width=80)
                view_tree.heading(2, text="Member's Name")
                view_tree.column(2, minwidth=50, width=100)
                view_tree.heading(3, text="Date Of Issue")
                view_tree.column(3, minwidth=50, width=85)
                view_tree.heading(4, text="Proposed Date Of Return")
                view_tree.column(4, minwidth=50, width=140)
                view_tree.place(relx=0.05, rely=0.2, relheight=0.4)

                for row1 in view_tree.get_children():
                    view_tree.delete(row1)
                for row1 in data3:
                    view_tree.insert('', 'end', value=row1)

                scroll_view = Scrollbar(view_frame, orient=VERTICAL,
                                        command=view_tree.yview)
                scroll_view.place(relx=0.9, rely=0.2, relheight=0.4)
                view_tree.configure(yscrollcommand=scroll_view.set)

                # ----------------------------------------------------
                # defining close button function
                def close():
                    bk_detail()
                # ----------------------------------------------------
                close_button = Button(view_frame, text='Close',
                                      command=close, width=15)
                close_button.place(relx=0.4, rely=0.85)
            # --------------------------------------------------------
            view_button = Button(dt_frame, text="View", width=15,
                                 height=2, command=view)
            view_button.place(relx=0.9, rely=0.26)

            # --------------------------------------------------------
            # defining edit button
            def edit():
                genre_entry.focus_set()
                detail.config(selectmode=NONE)  # disabling selection
                edit_button.destroy()
                add_button.destroy()
                r.normal(entry_tup)  # replicate file to change state
                year_of_pub_entry.config(state='readonly')
                id_entry.config(state=DISABLED)

                # ----------------------------------------------------
                # defining change button
                def changes():
                    detail.config(selectmode=BROWSE)
                    if messagebox.askyesno('?', 'Do You Want To Save '
                                                'the Changes?') ==\
                            FALSE:
                        bk_detail()
                    else:  # not allowing negative and zero
                        if int(num_entry.get()) <= 0:
                            messagebox.showerror('Number', 'Negative'
                                                           ' or zero '
                                                           'books not'
                                                           ' allowed')
                        else:
                            entries = name_entry, author_entry, \
                                      genre_entry, pub_entry, \
                                      year_of_pub_entry, num_entry

                            query2 = 'update books ' \
                                     'set book_name="%s", ' \
                                     'author="%s", genre="%s", ' \
                                     'publication="%s", year_of_' \
                                     'publication="%s",' \
                                     'no_books=%s where book_reg="%s"'
                            r.entry_get(entries, query2, extra=(
                                org_id,))
                            r.update(detail, 'books', 'book_reg')
                            r.disable(entry_tup)  # disabling entries
                            bk_detail()
                            update()

                # ----------------------------------------------------
                changes_button = Button(dt_frame, text='Save Changes',
                                        width=15, height=2,
                                        command=changes)
                changes_button.place(relx=0.9, rely=0.105)

                # ----------------------------------------------------
                # defining delete button
                def delete():
                    if messagebox.askyesno('?', 'Do You Want to '
                                                'Delete the Record?')\
                            == FALSE:
                        bk_detail()
                    else:
                        my_con3 = my.connect(host='sql11.freemysqlh'
                                                  'osting.net',
                                             user='sql11422143',
                                             passwd='pq3EcPFj4e',
                                             db='sql11422143')
                        cur3 = my_con3.cursor()

                        query3 = "delete from books where " \
                                 "book_reg='%s'" % (org_id,)
                        cur3.execute(query3)
                        my_con3.commit()
                        r.update(detail, 'books', 'book_reg')
                        my_con3.close()

                        r.delete(entry_tup)
                        r.disable(entry_tup)

                        bk_detail()
                        update()

                # ----------------------------------------------------
                delete_button = Button(dt_frame, text='Delete the '
                                                      'record',
                                       width=15, height=2,
                                       command=delete)
                delete_button.place(relx=0.9, rely=0.26)

                # ----------------------------------------------------
                # defining cancel button
                def cancel():
                    bk_detail()

                # ----------------------------------------------------
                cancel_button1 = Button(dt_frame, text='Cancel',
                                        width=15, height=2,
                                        command=cancel)
                cancel_button1.place(relx=0.9, rely=0.4)

            # --------------------------------------------------------
            edit_button.config(state=NORMAL, command=edit)

        # ------------------------------------------------------------
        edit_button = Button(dt_frame, text="Edit", width=15,
                             height=2, state=DISABLED)
        edit_button.place(relx=0.9, rely=0.105)

        # ------------------------------------------------------------
        # defining add button
        def add():
            detail.config(selectmode=NONE)
            id_entry.focus_set()
            edit_button.destroy()
            add_button.destroy()

            r.normal(entry_tup)
            r.delete(entry_tup)
            year_of_pub_entry.config(state='readonly')

            # --------------------------------------------------------
            # defining submit button
            def submit():
                if int(num_entry.get()) <= 0:
                    messagebox.showerror('Number', 'Negative or zero'
                                                   ' books not '
                                                   'allowed')
                else:
                    query4 = 'insert into books values("%s", "%s",' \
                             '"%s","%s","%s","%s",%s)'
                    r.entry_get(entry_tup, query4)
                    r.update(detail, 'books', 'book_reg')

                    r.delete(entry_tup)
                    bk_detail()
                    update()

            # --------------------------------------------------------
            submit_button = Button(dt_frame, text='Submit', width=15,
                                   height=2, command=submit)
            submit_button.place(relx=0.9, rely=0.105)

            # --------------------------------------------------------
            # defining cancel button
            def cancel():
                bk_detail()

            # --------------------------------------------------------
            cancel_button = Button(dt_frame, text='Cancel', width=15,
                                   height=2, command=cancel)
            cancel_button.place(relx=0.9, rely=0.26)

        # ------------------------------------------------------------
        add_button = Button(dt_frame, text='Add Record', width=15,
                            height=2, command=add)
        add_button.place(relx=0.9, rely=0.4)

        # creating the treeview
        detail = tk.Treeview(dt_frame, column=(1, 2, 3, 4, 5, 6, 7),
                             show='headings')
        detail.heading(1, text='Book ID')
        detail.column(1, minwidth=0, width=55, stretch=NO)
        detail.heading(2, text='Book Name')
        detail.column(2, minwidth=0, width=260, stretch=NO)
        detail.heading(3, text='Author')
        detail.column(3, minwidth=0, width=155, stretch=NO)
        detail.heading(4, text='Genre')
        detail.column(4, minwidth=0, width=200, stretch=NO)
        detail.heading(5, text='Publication')
        detail.column(5, minwidth=0, width=150, stretch=NO)
        detail.heading(6, text='Year of publication')
        detail.column(6, minwidth=0, width=110, stretch=NO)
        detail.heading(7, text='No of Books')
        detail.column(7, minwidth=0, width=100, stretch=NO)
        detail.bind('<<TreeviewSelect>>', select)

        r.update(detail, 'books', 'book_reg')
        detail.place(relx=0.03, rely=0.105)
        r.menubar(bk_screen, 'bk_screen', detail, b)

        # creating scrollbar
        scroll = Scrollbar(dt_frame, orient=VERTICAL,
                           command=detail.yview)
        scroll.place(relx=0.83, rely=0.105, height=225)
        detail.configure(yscrollcommand=scroll.set)

    bk_detail_button = Button(bk_screen, text='Book Details',
                              width=20, height=2, command=bk_detail,
                              bg=col,
                              activebackground=col, font=('times new '
                                                          'roman', 15,
                                                          "bold"))
    bk_detail_button.place(relx=0.05, rely=0.05)

    # ----------------------------------------------------------------
    # Defining issue book button
    def issue():
        # creating frame and placing label, entries and button--------
        issue_frame = LabelFrame(bk_screen, text='BOOKS ISSUED',
                                 bd=15, bg=col,
                                 relief=RIDGE, font=('times new '
                                                     'roman', 10,
                                                     "bold"))
        issue_frame.place(x=50, y=150, height=550,
                          width=1355)

        search_label = Label(issue_frame, text='Search', bg='black',
                             fg='white')
        search_label.place(relx=0.03, rely=0.01, height=30)
        search_entry = Entry(issue_frame, width=155, relief=GROOVE)
        search_entry.place(relx=0.075, rely=0.01, height=30)

        id_label = Label(issue_frame, text='Issue ID',  width=20,
                         bg='black', fg='white')
        id_label.place(relx=0.03, rely=0.55)
        id_entry = Entry(issue_frame, width=55)
        id_entry.place(relx=0.15, rely=0.55)

        book_id_label = Label(issue_frame, text='Book ID',  width=20,
                              bg='black', fg='white')
        book_id_label.place(relx=0.03, rely=0.664)
        book_id_entry = Entry(issue_frame, width=55)
        book_id_entry.bind('<Return>',
                           lambda e: book_name_entry.focus())
        book_id_entry.place(relx=0.15, rely=0.664)

        book_name_label = Label(issue_frame, text='Book Name',
                                width=20, bg='black', fg='white')
        book_name_label.place(relx=0.48, rely=0.664)
        book_name_entry = Entry(issue_frame, width=55)
        book_name_entry.bind('<Return>',
                             lambda e: members_id_entry.focus())
        book_name_entry.place(relx=0.60, rely=0.664)

        members_id_label = Label(issue_frame, text="Members Id",
                                 width=20, bg='black', fg='white')
        members_id_label.place(relx=0.03, rely=0.778)
        members_id_entry = Entry(issue_frame, width=55)
        members_id_entry.bind('<Return>',
                              lambda e: members_name_entry.focus())
        members_id_entry.place(relx=0.15, rely=0.778)

        members_name_label = Label(issue_frame, text='Members Name',
                                   width=20, bg='black', fg='white')
        members_name_label.place(relx=0.48, rely=0.778)
        members_name_entry = Entry(issue_frame, width=55)
        members_name_entry.bind('Return',
                    lambda e: proposed_date_of_return_entry.focus())
        members_name_entry.place(relx=0.60, rely=0.778)

        date_of_issue_label = Label(issue_frame, text='Date of Issue',
                                    width=20, bg='black', fg='white')
        date_of_issue_label.place(relx=0.03, rely=0.892)
        date_of_issue_entry = tkcalendar.DateEntry(issue_frame,
                                                   width=52)
        date_of_issue_entry.place(relx=0.15, rely=0.892)

        proposed_date_of_return_label = Label(issue_frame,
                                              text='Proposed Date of'
                                                   ' Return',
                                              width=20, bg='black',
                                              fg='white')
        proposed_date_of_return_label.place(relx=0.48, rely=0.55)
        proposed_date_of_return_entry = tkcalendar.DateEntry(
            issue_frame, width=52)
        proposed_date_of_return_entry.place(relx=0.60, rely=0.55)

        # search option
        query1 = 'select*from issue_books where issue_id like ' \
                 '("%s") or book_reg like ("%s") ' \
                 'or book_name like ("%s") or members_id like ' \
                 '("%s") or members_name like ("%s") ' \
                 'or date_of_issue  like ("%s") or ' \
                 'proposed_date_of_return like ("%s") ' \
                 'or no_of_days_left like ("%s")  or fine like ("%s")'

        search_entry.bind('<Return>', lambda e: r.search((
            search_entry.get(), search_entry.get(),
            search_entry.get(),
            search_entry.get(), search_entry.get(),
            search_entry.get(),
            search_entry.get(), search_entry.get),
                                                         issue_tree,
                                                         query1,
                                                         search_entry)
                          )

        search_img = ImageTk.PhotoImage(Image.open("images/search"
                                                   " image.jpg"))
        search_button = Button(issue_frame,
                               command=lambda: r.search((
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get(),
                                   search_entry.get),
                                                        issue_tree,
                                                        query1,
                                                        search_entry),
                               text='search', image=search_img)
        search_button.place(relx=0.915, rely=0.01, height=30,
                            width=40)
        search_button.image = search_img

        entry_tup = (id_entry, book_id_entry, book_name_entry,
                     members_id_entry, members_name_entry,
                     date_of_issue_entry,
                     proposed_date_of_return_entry)

        # ------------------------------------------------------------
        # defining add button ------------------
        def add():
            issue_tree.config(selectmode=NONE)
            add_button.destroy()
            edit_button.destroy()

            book_id_entry.focus()
            r.normal(entry_tup)
            r.delete(entry_tup)

            # entering current date in issue_date
            today = d.today()
            date_of_issue_entry.insert(0, today)

            # restricting dates in calendar
            max_ = today + dt.timedelta(days=30)
            proposed_date_of_return_entry.config(mindate=today,
                                                 maxdate=max_,
                                                 state='readonly')

            # entering issue_id
            my_con2 = my.connect(host='sql11.freemysqlhosting.net',
                                 user='sql11422143',
                                 passwd='pq3EcPFj4e',
                                 db='sql11422143')
            cur2 = my_con2.cursor()
            query2 = "select issue_id from issue_books"
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
                i_id = "IS00" + str(y)
            elif 100 <= y <= 1000:
                i_id = "IS0" + str(y)
            else:
                i_id = "IS" + str(y)

            id_entry.insert(0, i_id)
            r.disable((date_of_issue_entry, id_entry,
                       members_name_entry))

            members_id_entry.bind('<FocusIn>',
                                  lambda e: members_name_entry.config
                                  (state=NORMAL))

            book_name_entry.bind('<FocusIn>',
                                 lambda e: (r.insert_name(
                                     book_id_entry, book_name_entry,
                                     'book_reg', 'book_name',
                                     members_id_entry)))

            members_name_entry.bind('<FocusIn>',
                                    lambda e: (r.insert_name(
                                        members_id_entry,
                                        members_name_entry,
                                        'members_id', 'members_name',
                                        proposed_date_of_return_entry,
                                        'members')))

            # --------------------------------------------------------
            # defining submit button
            def submit():
                left = (proposed_date_of_return_entry.get_date()
                        - today).days
                my_con6 = my.connect(host='sql11.freemysqlhosti'
                                          'ng.net',
                                     user='sql11422143',
                                     passwd='pq3EcPFj4e',
                                     db='sql11422143')
                cur6 = my_con6.cursor()
                query6 = 'Select no_books from books where' \
                         ' book_reg="%s"' % (book_id_entry.get(),)
                cur6.execute(query6)
                total_num = cur6.fetchall()[0][0]
                query6 = 'Select * from issue_books where ' \
                         'book_reg="%s" and status="Issued"' % \
                         (book_id_entry.get(),)
                cur6.execute(query6)
                data6 = cur6.fetchall()
                number_issued = len(data6)
                if number_issued >= total_num:  # no book in stock
                    messagebox.showerror('ERROR', 'No books in stock')
                else:
                    query6 = 'Select * from issue_books where' \
                             ' members_id="%s" and status="Issued"' %\
                             (members_id_entry.get(),)
                    cur6.execute(query6)
                    data6 = cur6.fetchall()
                    number_issued = len(data6)
                    if number_issued > 5:
                        messagebox.showerror("!", 'This member has'
                                                  ' reached maximum '
                                                  'limit of books')
                    else:
                        query6 = 'insert into issue_books (issue_id,'\
                                 'book_reg, book_name, members_id,' \
                                 ' members_name, date_of_issue, ' \
                                 'proposed_date_of_return,' \
                                 ' no_of_days_left, fine) ' \
                                 'values ("%s","%s","%s","%s","%s",' \
                                 '"%s","%s","%s","%s")'
                        tup1 = entry_tup[:6]
                        r.entry_get(tup1, query6, extra=(
                          proposed_date_of_return_entry.get_date(),
                          left, '0'))
                        r.update(issue_tree, 'issue_books', 'issue_id'
                                 )
                my_con6.close()

                issue()
                update()

            # --------------------------------------------------------
            submit_button = Button(issue_frame, text='Submit',
                                   width=15, height=2, command=submit)
            submit_button.place(relx=0.9, rely=0.105)

            # --------------------------------------------------------
            # defining cancel button
            def cancel():
                issue()

            # --------------------------------------------------------
            cancel_button = Button(issue_frame, text='Cancel',
                                   width=15, height=2, command=cancel)
            cancel_button.place(relx=0.9, rely=0.26)

        # ------------------------------------------------------------
        add_button = Button(issue_frame, text='Issue Book', width=15,
                            height=2, command=add)
        add_button.place(relx=0.9, rely=0.4)

        # ------------------------------------------------------------
        # defining selection of each row
        def select(event):
            cur_item = issue_tree.focus()
            row_info = issue_tree.item(cur_item)
            row_list = row_info['values']

            r.normal(entry_tup)
            r.delete(entry_tup)
            r.insert(entry_tup, row_list)
            id_e = id_entry.get()
            mem_name = members_name_entry.get()
            r.disable(entry_tup)

            def returned():
                my_con7 = my.connect(host='sql11.freemysq'
                                          'lhosting.net',
                                     user='sql11422143',
                                     passwd='pq3EcPFj4e',
                                     db='sql11422143')
                cur7 = my_con7.cursor()
                query7 = 'select fine from issue_books where ' \
                         'issue_id="%s"' % (id_e,)
                cur7.execute(query7)
                fine = cur7.fetchone()
                if fine[0] is not None:
                    if fine[0] > 0:
                        if messagebox.askyesno('?', 'Fine Paid?') == \
                                TRUE:

                            my_con2 = my.connect(host='sql11.freemys'
                                                      'qlhosting.net',
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
                                    y = int("".join(filter(
                                        str.isdigit, row2[0])))
                                    id_ += (y,)
                                y = max(id_) + 1
                            if y < 100:
                                f_id = "FN00" + str(y)
                            elif 100 <= y <= 1000:
                                f_id = "FN0" + str(y)
                            else:
                                f_id = "FN" + str(y)

                            query7 = 'insert into funds (funds_id,' \
                                     ' name, amount, cause) values' \
                                     '("%s", "%s", %s, "Fine")'\
                                     % (f_id, mem_name, fine[0])
                            cur7.execute(query7)
                            my_con7.commit()
                            r.update(issue_tree, 'issue_books',
                                     'issue_id')
                            issue()
                        else:
                            issue()
                    else:
                        if messagebox.askyesno('?', ' Returned Book?'
                                               ) == FALSE:
                            issue()

                    query7 = 'Update issue_books Set' \
                             ' status="Returned", ' \
                             'no_of_days_left=NULL, fine=NULL ' \
                             'where issue_id="%s"' % (id_e,)
                    cur7.execute(query7)
                    my_con7.commit()
                    r.update(issue_tree, 'issue_books', 'issue_id')
                    my_con7.close()
                    issue()
                    update()

            returned_button = Button(issue_frame, text='Return',
                                     width=15, height=2,
                                     command=returned)
            returned_button.place(relx=0.9, rely=0.26)

            # --------------------------------------------------------
            # defining edit button
            def edit():
                issue_tree.config(selectmode=NONE)
                edit_button.config(state=DISABLED)
                book_id_entry.focus()

                r.normal((book_id_entry, members_id_entry,
                          proposed_date_of_return_entry))

                today = d.today()
                date_of_issue_entry.insert(0, today)

                max_ = today + dt.timedelta(days=30)
                proposed_date_of_return_entry.config(mindate=today,
                                                     maxdate=max_,
                                                     state='readonly')

                add_button.destroy()

                book_name_entry.bind('<FocusIn>',
                                     lambda e: (r.insert_name(
                                         book_id_entry,
                                         book_name_entry, 'book_reg',
                                         'book_name',
                                         members_id_entry)))

                members_name_entry.bind('<FocusIn>',
                                        lambda e: r.insert_name(
                                            members_id_entry,
                                            members_name_entry,
                                            'members_id',
                                            'members_name',
                                        proposed_date_of_return_entry,
                                            'members'))

                # ----------------------------------------------------
                # defining save changes button
                def changes():
                    if messagebox.askyesno('?', 'Save Changes?') \
                            == FALSE:
                        issue()
                    else:
                        issue_tree.config(selectmode=BROWSE)
                        my_con7 = my.connect(host='sql11.freemysql'
                                                  'hosting.net',
                                             user='sql11422143',
                                             passwd='pq3EcPFj4e',
                                             db='sql11422143')
                        cur7 = my_con7.cursor()

                        new_book_id = book_id_entry.get()
                        new_members_id = members_id_entry.get()
                        new_book_name = book_name_entry.get()
                        new_members_name = members_name_entry.get()
                        new_date = \
                            proposed_date_of_return_entry.get_date()
                        new_days_left = new_date - today

                        tup = (new_book_id, new_book_name,
                               new_members_id, new_members_name,
                               new_date, new_days_left, id_e)

                        query7 = 'update issue_books ' \
                                 'set book_reg ="%s", ' \
                                 'book_name="%s",' \
                                 'members_id="%s",' \
                                 'Members_name="%s", ' \
                                 'proposed_date_of_return="%s"' \
                                 'no_of_days_left = "%s" where ' \
                                 'issue_id="%s"' % tup

                        cur7.execute(query7)
                        my_con7.commit()
                        r.update(issue_tree, 'issue_books', 'issue_id'
                                 )
                        my_con7.close()

                        r.disable(entry_tup)
                        r.delete(entry_tup)
                        issue()
                        update()

                # ----------------------------------------------------
                changes_button = Button(issue_frame,
                                        text='Save Changes', width=15,
                                        height=2, command=changes)
                changes_button.place(relx=0.9, rely=0.105)

                # ----------------------------------------------------
                # defining cancel button
                def cancel():
                    issue()

                # ----------------------------------------------------
                cancel_button = Button(issue_frame, text='Cancel',
                                       width=15, height=2,
                                       command=cancel)
                cancel_button.place(relx=0.9, rely=0.26)

                # ----------------------------------------------------
                # defining delete button
                def delete():
                    if messagebox.askyesno('?', 'Do you want to '
                                                'delete the record?'
                                           ) == FALSE:
                        issue()
                    else:
                        my_con8 = my.connect(host='sql11.freemysq'
                                                  'lhosting.net',
                                             user='sql11422143',
                                             passwd='pq3EcPFj4e',
                                             db='sql11422143')
                        cur8 = my_con8.cursor()
                        query8 = 'delete from issue_books where ' \
                                 'issue_id="%s"' % (id_e,)
                        cur8.execute(query8)
                        my_con8.commit()
                        my_con8.close()
                        issue()
                        update()

                # ----------------------------------------------------
                del_button = Button(issue_frame, text='Delete Record',
                                    width=15, height=2, command=delete
                                    )
                del_button.place(relx=0.9, rely=0.4)

            # --------------------------------------------------------
            edit_button.config(state=NORMAL, command=edit)

        # ------------------------------------------------------------
        edit_button = Button(issue_frame, text="Edit", width=15,
                             height=2, state=DISABLED)
        edit_button.place(relx=0.9, rely=0.105)

        # creating treeview
        issue_tree = tk.Treeview(issue_frame, column=(1, 2, 3, 4, 5,
                                                      6, 7, 8, 9, 10),
                                 show='headings')
        issue_tree.heading(1, text='Issue ID')
        issue_tree.column(1, minwidth=0, width=51, stretch=NO)
        issue_tree.heading(2, text='Book ID')
        issue_tree.column(2, minwidth=0, width=51, stretch=NO)
        issue_tree.heading(3, text='Book Name')
        issue_tree.column(3, minwidth=0, width=240, stretch=NO)
        issue_tree.heading(4, text='Members ID')
        issue_tree.column(4, minwidth=0, width=73, stretch=NO)
        issue_tree.heading(5, text='Members Name')
        issue_tree.column(5, minwidth=0, width=145, stretch=NO)
        issue_tree.heading(6, text='Date Of Issue')
        issue_tree.column(6, minwidth=0, width=100, stretch=NO)
        issue_tree.heading(7, text='Proposed Date Of Return')
        issue_tree.column(7, minwidth=0, width=150, stretch=NO)
        issue_tree.heading(8, text='No of Days Left')
        issue_tree.column(8, minwidth=0, width=105, stretch=NO)
        issue_tree.heading(9, text='Fine')
        issue_tree.column(9, minwidth=0, width=52, stretch=NO)
        issue_tree.heading(10, text='Status')
        issue_tree.column(10, minwidth=40, width=62)
        issue_tree.bind('<<TreeviewSelect>>', select)
        issue_tree.place(relx=0.03, rely=0.105)
        r.update(issue_tree, 'issue_books', 'status')

        # creating scrollbar
        scroll = Scrollbar(issue_frame, orient=VERTICAL,
                           command=issue_tree.yview)
        scroll.place(relx=0.83, rely=0.105, height=225)
        issue_tree.configure(yscrollcommand=scroll.set)
        r.menubar(bk_screen, 'bk_screen', issue_tree, b)

        r.delete(entry_tup)
        r.disable(entry_tup)

    # ----------------------------------------------------------------
    button_issue = Button(bk_screen, text='Books Issued',
                          command=issue, width=20, height=2,  bg=col,
                          activebackground=col, font=('times new'
                                                      ' roman', 15,
                                                      "bold"))
    button_issue.place(relx=0.25, rely=0.05)

    bk_detail()
    bk_screen.mainloop()
