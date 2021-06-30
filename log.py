# LogIN PAGE
from tkinter import *
from PIL import ImageTk, Image
from random import randint
import mysql.connector as my
import smtplib
from email.message import EmailMessage
from tkinter import messagebox
import homepage


# ------------Design functions for different windows-----------------#
def design(page, text):
    title = Label(page, text=text, font=('bold', 15, 'underline'),
                  fg='#d56429', bg='black')
    title.grid(row=0, column=0, columnspan=3)
    # place the icon of the page
    page.iconbitmap("images/main_icon.ico")
    # configure the screen
    page.configure(bg='black')
    # disable modifying screen size
    page.resizable(0, 0)
    # transparent window of 0.9 transparency
    page.wm_attributes('-alpha', 0.9)


# --------------------Main login function----------------------------#
def login():
    root = Tk()                       # creating the main window
    root.title('LOGIN')               # placing the title for window
    # calling the design function
    design(page=root, text='Login to your account')
    # placing the window on center of the screen
    root.geometry("300x200+525+300")

    # Images ----------------------------------------------
    user_icon = ImageTk.PhotoImage(Image.open("images/"
                                              "username icon1.png"))
    user_icon_label = Label(root, image=user_icon)     # placing image
    user_icon_label.grid(row=1, column=1)
    pass_icon = ImageTk.PhotoImage(Image.open("images/"
                                              "password_icon1.png"))
    pass_label = Label(root, image=pass_icon)
    pass_label.grid(row=2, column=1)

    # Labels and entries-----------------------------------
    username = Label(root, text='Username:', font=15,
                     bg='black', fg='#d56429')
    username.grid(row=1, column=0, padx=5, pady=20)

    user = Entry(root)
    user.grid(row=1, column=2, ipady=5, ipadx=20, padx=5)
    # cursor focuses of next entry on pressing enter
    user.bind('<Return>', lambda e: password_entry.focus_set())
    user.focus()                     # user entry has initial focus

    password = Label(root, text='Password:', font=15,
                     bg='black', fg='#d56429')
    password.grid(row=2, column=0, padx=5, pady=20)

    password_entry = Entry(root, show='*')  # *instead of password
    password_entry.bind('<Return>', lambda e: clicked())
    password_entry.grid(row=2, column=2, ipady=5, ipadx=20)

    # ----------------------------------------------------------------
    # Submit button function
    def clicked():
        usr = user.get()
        psd = str(password_entry.get())
        my_con0 = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
        cur0 = my_con0.cursor()
        cur0.execute('select * from user_password')
        data0 = cur0.fetchall()
        for row in data0:
            if row[0] == usr:                   # finding username
                if row[1] == psd:               # match the password
                    # update status
                    query0 = 'update user_password set status="YES"' \
                             ' where user_name= "%s" ' % (usr,)
                    cur0.execute(query0)
                    my_con0.commit()
                    root.destroy()
                    a = 0
                    homepage.main_page(a)        # opening homepage

                else:
                    messagebox.showerror('ERROR', 'WRONG PASSWORD')
                break
        else:
            messagebox.showerror('ERROR', 'INVALID USERNAME')

        my_con0.close()
    submit = Button(root, text='Submit', command=clicked, width=10)
    submit.grid(row=3, column=2, pady=7, padx=2, columnspan=2)

    # ----------------------------------------------------------------
    # forgot password button function
    def forgot():
        forgot_password = Tk()                    # New window
        root.withdraw()                           # Main window hidden
        forgot_password.title('Account Modification')
        forgot_password.geometry("400x200+525+300")
        # calling the design function
        design(page=forgot_password, text='Enter The Details')

        # username entry
        username_label = Label(forgot_password,
                               text="Enter the username",
                               bg='black', fg='#d56429', height=2)
        username_label.grid(row=1, column=0, padx=5, pady=20)
        username_entry = Entry(forgot_password)
        username_entry.grid(row=1, column=1, padx=5, pady=20, ipady=3)

        # ------------------------------------------------------------
        # send code button function
        def sent():
            send.config(state=DISABLED)
            usr = username_entry.get()
            code_label = Label(forgot_password,
                               text="Enter the verification code "
                                    "sent to the registered EmailID",
                               bg='black', fg='#d56429')
            code_label.grid(row=2, column=0, columnspan=3,
                            padx=5, pady=5)

            code = Entry(forgot_password)
            code.grid(row=3, column=0, columnspan=2,
                      padx=5, pady=5, ipady=3)

            # send code to registered email address
            my_con1 = my.connect(host='sql11.freemysqlhosting.net',
                                 user='sql11422143',
                                 passwd='pq3EcPFj4e',
                                 db='sql11422143')
            cur1 = my_con1.cursor()
            cur1.execute('select * from user_password')
            data1 = cur1.fetchall()
            email = ''
            for row in data1:
                if row[0] == usr:
                    email = row[2]         # finding the email id
                    break
            else:        # if username not found display error message
                forgot_password.destroy()
                messagebox.showerror('ERROR', 'INVALID USERNAME')
                root.deiconify()

            receivers_email = email
            # administers emailid
            sender_email = "python.testing.tk@gmail.com"
            email_password = "testpython1"     # administers password
            num = randint(1000, 10000)
            str_num = str(num)

            msg = EmailMessage()
            msg.set_content("THE VERIFICATION CODE FOR YOUR ACCOUNT "
                            "IS %s" % str_num)
            msg['Subject'] = "Authentication"
            msg["From"] = sender_email
            msg["To"] = receivers_email

            # email connection server 587
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(msg)

            # --------------------------------------------------------
            # password change button function
            def password_change():
                password_new = Tk()                      # New window
                password_new.geometry("300x200+525+300")
                v_code = code.get()
                if v_code == str_num:            # validating the code
                    design(page=password_new, text='Password Change')
                    forgot_password.withdraw()
                    password_new.title("New password")

                    new_password_label = Label(password_new,
                                               text="Enter new"
                                                    " password",
                                               bg='black',
                                               fg='#d56429')
                    new_password_label.grid(row=1, column=0,
                                            padx=5, pady=20)

                    new_password = Entry(password_new, show='*')
                    new_password.grid(row=1, column=1, pady=5)

                    confirm_password_label = Label(password_new,
                                                   text="Confirm new "
                                                        "password",
                                                   bg='black',
                                                   fg='#d56429')
                    confirm_password_label.grid(row=2, column=0,
                                                padx=5, pady=20)

                    confirm_password = Entry(password_new, show='*')
                    confirm_password.grid(row=2, column=1, pady=5)

                    # ------------------------------------------------
                    # change password function
                    def home():
                        passw1 = new_password.get()
                        conpassw = confirm_password.get()

                        # confirm new password and change it
                        if passw1 == conpassw:
                            mycon = my.connect(host='sql11.freemysq'
                                                    'lhosting.net',
                                               user='sql11422143',
                                               passwd='pq3EcPFj4e',
                                               db='sql11422143')
                            curs = mycon.cursor()

                            str1 = 'update user_password set' \
                                   ' Password="%s" where' \
                                   ' User_name="%s"' % (passw1, usr)
                            curs.execute(str1)
                            mycon.commit()
                            mycon.close()

                            password_new.destroy()
                            root.deiconify()   # main window to login
                        else:   # passwords don't match  error message
                            messagebox.showerror("ERROR",
                                                 "Password "
                                                 "doesnt match")

                    done = Button(password_new, text="Submit",
                                  command=lambda: home())
                    done.grid(row=3, column=0, pady=7)
                else:           # if code incorrect show error message
                    messagebox.showerror('ERROR', 'Wrong Input')
                    # ------------------------------------------------
            sub = Button(forgot_password, text='Submit',
                         command=lambda: password_change(), width=10)
            sub.grid(row=3, column=2, ipady=2, padx=5, pady=5)
            # --------------------------------------------------------

        send = Button(forgot_password, text="Send Code", command=sent)
        send.grid(row=1, column=2, padx=5)
        # ------------------------------------------------------------
    forgotpsd = Button(root, text='Forgot password?', command=forgot)
    forgotpsd.grid(row=3, column=0, columnspan=2, padx=10)
    # ----------------------------------------------------------------
    root.mainloop()


def main():
    # check the login status, if not logged out then no login needed
    my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur = my_con.cursor()
    query = 'select status from user_password'
    cur.execute(query)
    data = cur.fetchone()
    if data[0] == "NO":
        login()
    else:
        a = 0
        homepage.main_page(a)
