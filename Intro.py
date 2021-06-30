# Intro Page
from tkinter import *
from PIL import Image, ImageTk
import cv2


# ----------------------------Start Function--------------------------#
def start(event):
    label1.destroy()
    import log
    win.destroy()
    log.main()


# ------------------------Main Window---------------------------------#
def main_window():
    global win
    global label1
    win = Tk()
    win.title('Library Management System')
    win.iconbitmap("images/main_icon.ico")
    win.bind('<Key>', start)  # start function on pressing any key
    win.state('zoomed')

    # opens video
    cap = cv2.VideoCapture("images/vid.MP4")
    global n
    n = 0

    # -----------------------------------------------------------------
    # defining show function
    def show():
        global n  # frame count
        n = n+1
        if n <= 30:
            rest, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image).resize((1600, 850))
            imgtk = ImageTk.PhotoImage(image=img)
            label1.imgtk = imgtk
            label1.configure(image=imgtk)
            win.after(10, show)
        else:
            label1.destroy()
            frm = Frame(win, bg='black')
            frm.place(relx=0, rely=0, relwidth=1, relheight=1)
            label = Label(frm, text='Press any Key to continue',
                          bg='black', fg='white')
            label.place(relx=0.45, rely=0.5)
    # -----------------------------------------------------------------

    label1 = Label(win)
    label1.place(relx=0, rely=0, relheight=1, relwidth=1)

    show()
    win.mainloop()
    # -----------------------------------------------------------------


main_window()
