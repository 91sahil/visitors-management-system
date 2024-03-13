from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import re

def admin_login():
    admin_password = admin_password_entry.get()

    if admin_password == "admin123":  #"admin123" admin password
        admin_login_window.withdraw()
        vw.deiconify()
    else:
        showerror("Login Failed", "Incorrect admin password")

def view_entries():
    con = MongoClient("localhost", 27017)
    db = con["sah16oct23"]
    coll = db["employee"]
    entries = coll.find()

    vw_st_data.delete(1.0, END)

    for entry in entries:
        office = entry['office']
        name = entry['name']
        phone = entry['phone']
        in_time = entry['in_time']
        date = entry['date']
        visitee = entry['visitee']

        entry_text = f"Office: {office}\nName: {name}\nPhone: {phone}\nIn Time: {in_time}\nDate: {date}\nVisitee: {visitee}\n\n"

        vw_st_data.insert(INSERT, entry_text)
def delete_entry_by_phone(phone_number):
    con = MongoClient("localhost", 27017)
    db = con["sah16oct23"]
    coll = db["employee"]

    # Delete the entry by phone number
    result = coll.delete_many({"phone": phone_number})

    con.close()

    return result.deleted_count


def delete_selected_entry():
    phone_number = phone_number_entry.get()
    
    if not phone_number:
        showinfo("Phone Number Required", "Please enter a phone number to delete an entry.")
        return
    
    deleted_count = delete_entry_by_phone(phone_number)

    if deleted_count > 0:
        showinfo("Delete Entry", "Entry deleted successfully")
        view_entries()
        phone_number_entry.delete(0, END)  # Clear the phone number entry field
    else:
        showinfo("Delete Entry", "Entry not found")

admin_login_window = Tk()
admin_login_window.title("Admin Login")
admin_login_window.geometry("1000x750+30+30")
f = ("Times New Roman", 15, "bold")

admin_login_label = Label(admin_login_window, text="FOR ADMIN LOGIN:-", font=f)
admin_login_label.place(x=700,y=500)

admin_password_label = Label(admin_login_window, text="Admin Password:", font=f)
admin_password_label.place(x=720,y=530)

admin_password_entry = Entry(admin_login_window, show="*", font=f)
admin_password_entry.place(x=700,y=560)

admin_login_button = Button(admin_login_window, text="Login", font=f, command=admin_login)
admin_login_button.place(x=760,y=600)

vw = Tk()
vw.title("Entry")
vw.geometry("1000x750+30+30")
f = ("Times New Roman", 20, "bold")

header_label = Label(vw, text="VISITOR'S DETAILS", font=f)
header_label.pack(pady=20)

def back():
	vw.withdraw()
	admin_login_window.deiconify()
	admin_password_entry.delete(0,END)

back_mv_button = Button(vw, text="BACK", command=back , width="30", height=2, fg="white", bg="grey", font=("Times New Roman", 10, "bold"))
back_mv_button.place(x=450,y=680)

header_label = Label(admin_login_window, text="VISITOR'S MANAGEMENT", font= ("Times New Roman", 30, "bold"))
header_label.pack(pady=20)

enter_details_label = Label(admin_login_window, text="Enter Your Details :-", font= ("Times New Roman", 25, "bold"))
enter_details_label.place(x=50,y=90)

office_label = Label(admin_login_window, text="Office Number", font=f)
office_label.place(x=50,y=150)

r = IntVar()
r.set(1)
rb_1 = Radiobutton(admin_login_window, text="office 1", font=f, variable=r, value=1)
rb_2 = Radiobutton(admin_login_window, text="office 2", font=f, variable=r, value=2)
rb_3 = Radiobutton(admin_login_window, text="office 3", font=f, variable=r, value=3)
rb_4 = Radiobutton(admin_login_window, text="office 4", font=f, variable=r, value=4)
rb_5 = Radiobutton(admin_login_window, text="office 5", font=f, variable=r, value=5)
rb_1.place(x=80,y=200)
rb_2.place(x=80,y=250)
rb_3.place(x=80,y=300)
rb_4.place(x=250,y=200)
rb_5.place(x=250,y=250)

name_label = Label(admin_login_window, text="Name  = ", font=f)
name_label.place(x=50,y=400)
name_entry = Entry(admin_login_window, font=f)
name_entry.place(x=220,y=400)

phone_label = Label(admin_login_window, text="Phone No  = ", font=f)
phone_label.place(x=50,y=450)
phone_entry = Entry(admin_login_window, font=f)
phone_entry.place(x=220,y=450)

in_time_label = Label(admin_login_window, text="in_time  = ", font=f)
in_time_label.place(x=50,y=500)
in_time_entry = Entry(admin_login_window, font=f)
in_time_entry.place(x=220,y=500)

date_label = Label(admin_login_window, text="Date  = ", font=f)
date_label.place(x=50,y=550)
date_entry = Entry(admin_login_window, font=f)
date_entry.place(x=220,y=550)

visitee_label = Label(admin_login_window, text="visitee  = ", font=f)
visitee_label.place(x=50,y=600)
visitee_entry = Entry(admin_login_window, font=f)
visitee_entry.place(x=220,y=600)

def validate_name(name):
	if len(name) < 2 or len(name) > 50:
		return False
	if not re.match("^[A-Za-z\s]*$", name):
		return False
	return True

def validate_phone(phone):
	if len(phone) < 10 or len(phone) > 15:
		return False
	if not re.match("^[0-9]*$", phone):
		return False
	return True

def validate_time_format(time_str):
	time_pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9] (AM|PM)$'
	return bool(re.match(time_pattern, time_str))

def validate_date_format(date_str):
	date_pattern = r'^\d{4}-\d{2}-\d{2}$'
	return bool(re.match(date_pattern, date_str))

# Save visitor entry function
def save():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["sah16oct23"]
		coll = db["employee"]

		selected_office = r.get()
		name = name_entry.get()
		phone = phone_entry.get()
		in_time = in_time_entry.get()
		date = date_entry.get()
		visitee = visitee_entry.get()
 
		if not validate_name(name):
			showinfo("Invalid Input", "Please enter a valid name.")
			return

		if not validate_phone(phone):
			showinfo("Invalid Input", "Please enter a valid phone number.")
			return

		if not validate_time_format(in_time):
			showinfo("Invalid Input", "Please enter a valid time format (e.g., hh:mm AM/PM).")
			return

		if not validate_date_format(date):
			showinfo("Invalid Input", "Please enter a valid date format (e.g., YYYY-MM-DD).")
			return


		if coll.find_one({"phone": phone}):
			showinfo("Duplicate Entry", "Phone number already exists")
			phone_entry.delete(0, END)
		else:
			data = {"office": selected_office, "name": name, "phone": phone, "in_time": in_time, "date": date, "visitee": visitee}
			coll.insert_one(data)
			showinfo("Success", "Visitor entry saved successfully")

		name_entry.delete(0, END)
		phone_entry.delete(0, END)
		in_time_entry.delete(0, END)
		date_entry.delete(0, END)
		visitee_entry.delete(0, END)
	except Exception as e:
		showinfo("Issue", e)
	finally:
		if con is not None:
			con.close()

submit_button = Button(admin_login_window, text="Submit", width="30", height=2, fg="white", bg="grey", command=save, font=("Times New Roman", 10, "bold"))
submit_button.place(x=150,y=680)

def clear_all():
	name_entry.delete(0, END)
	phone_entry.delete(0, END)
	in_time_entry.delete(0, END)
	date_entry.delete(0, END)
	visitee_entry.delete(0, END)

clear_button = Button(admin_login_window, text="Clear", width="30", height=2, fg="white", bg="blue", font=("Times New Roman", 10, "bold"), command=clear_all)
clear_button.place(x=450,y=680)

vw_st_data = ScrolledText(vw, width=30, height=13, font=f)
vw_st_data.place(x=100,y=100)

entry_label = Label(vw, text="", font=f)
entry_label.pack()

delete_entry_button = Button(vw, text="Delete Entry", command=delete_selected_entry, width="30", height=2, fg="white", bg="grey", font=("Times New Roman", 10, "bold"))
delete_entry_button.place(x=653,y=480)

to_number_label = Label(vw, text="TO DELETE ENTRY", font=f)
to_number_label.place(x=620,y=350)

phone_number_label = Label(vw, text="Phone Number:", font=f)
phone_number_label.place(x=653,y=390)
phone_number_entry = Entry(vw, font=f)
phone_number_entry.place(x=617,y=430)


view_entries_button = Button(vw, text="View Entries",  width="30", height=2, fg="white", bg="grey", command=view_entries, font=("Times New Roman", 10, "bold"))
view_entries_button.place(x=200,y=550)

vw.withdraw()

admin_login_window.mainloop()

