from tkinter import *

window = Tk()
window.title("MALAM Credentials")
window.geometry("300x150")


def submit_btn(event=None):
    user_id = user_id_input.get()
    password = password_in.get()
    window.quit()


window.bind('<Return>', submit_btn)

Label(window, text="User ID :").place(width=85, x=1, y=15)
user_id_input = Entry(window)
user_id_input.place(width=135, x=101, y=17)

Label(window, text="Password :").place(width=100, x=1, y=50)
password_in = Entry(window, show='*')
password_in.place(width=135, x=101, y=52)

Button(window, text="submit", command=submit_btn).place(width=100, x=95, y=100)

window.mainloop()
