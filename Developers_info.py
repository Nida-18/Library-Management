# DEVELOPERS WINDOW
from tkinter import *
from PIL import Image, ImageTk
import replicate as r


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
def info(a):
    global image1  # globalising variables to be used outside function
    global label1
    global b

    b = a
    info_screen = Tk()
    info_screen.title('Developers Info')
    info_screen.state('zoomed')
    info_screen.resizable(0, 0)
    info_screen.iconbitmap("images/info.ico")
    image1 = Image.open("images"
                        "/DeveloperInfo.PNG")
    bg = ImageTk.PhotoImage(image1)
    label1 = Label(info_screen, image=bg)
    label1.bind('<Configure>', resize)
    label1.place(relx=0.0, rely=0.0, relheight=1, relwidth=1.0)

    r.menubar(info_screen, 'info_screen', " ", b)

    info_screen.mainloop()
