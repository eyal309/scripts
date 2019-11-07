import json
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from tkinter import *
from random import *

window = Tk()
window.iconbitmap('icon.ico')
window.title('malam login')
window.geometry('300x150')

send_form = BooleanVar()
send_form.set(False)

remember_me = BooleanVar()
remember_me.set(False)

random_fill = BooleanVar()
random_fill.set(False)

try:
    with open('cred.json', 'r+') as ini:
        cred = json.load(ini)
        if cred['user']:
            remember_me.set(True)
except FileNotFoundError:
    with open('cred.json', 'w+') as ini:
        cred = {'user': '', 'password': ''}
        json.dump(cred, ini)

user_form = StringVar(window, value=cred['user'])
pass_form = StringVar(window, value=cred['password'])


def clear_btn():
    user_id_input.delete(0, 'end')
    password_in.delete(0, 'end')
    send_form.set(False)
    remember_me.set(False)
    random_fill.set(False)

    with open('cred.json', 'w') as file:
        json.dump({'user': '', 'password': ''}, file)


def exit_btn():
    window.destroy()


def submit_btn(event=None):
    id_num = user_id_input.get()
    password = password_in.get()
    send = send_form.get()
    random = random_fill.get()
    remember = remember_me.get()
    window.destroy()

    if remember:
        with open('cred.json', 'w') as file:
            json.dump({'user': id_num, 'password': password}, file)


    driver = webdriver.Chrome()

    url = <malam url> # add url here

    driver.get(url)

    company_num = 4300
    company_field = driver.find_element_by_name('indexNumInput')
    company_field.send_keys(company_num)

    id_field = driver.find_element_by_name('useridInput')
    id_field.send_keys(id_num)

    pass_field = driver.find_element_by_name('it2')
    pass_field.send_keys(password)

    login_btn = driver.find_element_by_id('loginButton')
    login_btn.click()
    sleep(0.5)

    # table = driver.find_element_by_id('pt1:j_id7')
    table = driver.find_element_by_xpath("//div[@id='pt1:j_id7']/div/table/tbody/tr/td[3]")
    table.click()
    sleep(0.5)

    # time_sheet = driver.find_element_by_id('pt1:timesheet__31410110')
    time_sheet = driver.find_element_by_xpath("//tr[@id='pt1:timesheet__31410110']/td[2]")
    time_sheet.click()
    sleep(1)

    days = driver.find_elements_by_class_name('xzy')

    minutes = [15, 15]

    if random:
        minutes = [randint(10, 20) for _ in days]

    i = 0
    for _ in days:
        shuffle(minutes)
        time_in = driver.find_element_by_name(f'pt1:dataTable:{i}:clockInTime')
        time_out = driver.find_element_by_name(f'pt1:dataTable:{i}:clockOutTime')
        if not driver.find_element_by_xpath(
                f"//div[@id='pt1:dataTable::db']/table/tbody/tr[{i + 1}]/td[2]/nobr/span").text:
            time_in.send_keys(f'08:{minutes[0]}')
            time_out.send_keys(f'17:{minutes[1]}')
        time_out.send_keys(Keys.DOWN)
        sleep(0.5)
        i += 1

    if send:
        btn_send = driver.find_element_by_id('pt1:saveButton')
        btn_send.click()

    sleep(20)
    driver.quit()


window.bind('<Return>', submit_btn)

Label(window, text="User ID :").place(width=85, x=1, y=15)
user_id_input = Entry(window, textvariable=user_form)
user_id_input.place(width=135, x=101, y=17)

Label(window, text="Password :").place(width=100, x=1, y=42)
password_in = Entry(window, show='*', textvariable=pass_form)
password_in.place(width=135, x=101, y=44)

Checkbutton(window, text="Send form", variable=send_form).place(width=90, x=100, y=70)
Checkbutton(window, text="Remember", variable=remember_me).place(width=90, x=10, y=70)
Checkbutton(window, text="Random fill", variable=random_fill).place(width=90, x=200, y=70)


Button(window, text="login", command=submit_btn).place(width=70, x=30, y=110)
Button(window, text="clear", command=clear_btn).place(width=70, x=110, y=110)
Button(window, text="cancel", command=exit_btn).place(width=70, x=190, y=110)

window.mainloop()
