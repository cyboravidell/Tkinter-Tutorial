# import what you need from tkinter module
from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk    # Provides access to the Tk themed widgets.
import sqlite3



class Contacts:
    db_filename = 'contacts.db'
    def __init__(self,root):
        self.root = root
        self.create_gui()
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica', 10))
        ttk.style.configure("Treeview.Heading", font=('helvetica', 12,'bold'))

    def execute_db_query(self,query,parameter=()):
        with sqlite3.connect(self.db_filename)as conn:
            print(conn)
            print(' You have successfuly connected to the Database')
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameter)
            conn.commit()
        return query_result

    def create_gui(self):
        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_scrollbar()
        self.create_bottom_buttons()
        self.view_contacts()

    def create_left_icon(self):
        photo = PhotoImage(file='E:\Tkinter Tutorial\Contacts\icons\logo.png')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0,column=0)

    def create_label_frame(self):
        labelFrame = LabelFrame(self.root, text="Create new Contact", bg="sky blue", font="helvetica 10")
        labelFrame.grid(row=0,column=1, padx=8,pady=8, sticky="ew")
        Label(labelFrame, text="Name: ", bg='green', fg="white").grid(row=1, column=1, sticky=W,padx=15,pady=2)
        self.namefield = Entry(labelFrame)
        self.namefield.grid(row=1,column=2,sticky=W,padx=5,pady=2)
        Label(labelFrame, text="Email: ", bg="brown", fg="white").grid(row=2,column=1,sticky=W, padx=15, pady=2)
        self.emailfield = Entry(labelFrame)
        self.emailfield.grid(row=2,column=2, sticky=W, padx=5,pady=2)
        Label(labelFrame, text='Number: ', bg="black",fg="white").grid(row=3, column=1, sticky=W, padx=15, pady=2)
        self.numfield = Entry(labelFrame)
        self.numfield.grid(row=3,column=2, sticky=W, padx=5,pady=2)
        Button(labelFrame, text='Add Contact', command=self.on_add_contact_button_clicked, bg="blue",fg="white").grid(row=4, column=2, sticky=E, padx=5,pady=5)
 
    def create_message_area(self):
        self.message = Label(text='', fg="red")
        self.message.grid(row=3,column=1,sticky=W)
    
    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=("email","number"),style='Treeview')
        self.tree.grid(row=6,column=0,columnspan=3)
        self.tree.heading("#0",text=' Name',anchor=W)
        self.tree.heading("email",text='Email Address',anchor=W)
        self.tree.heading("number",text='Contact Number',anchor=W)

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical',command=self.tree.yview)
        self.scrollbar.grid(row=6,column=3,rowspan=10,sticky='sn')

    def create_bottom_buttons(self):
        Button(text='Delete Selected', command='',bg='red',fg="white").grid(row=8,column=0, sticky=W,padx=20,pady=10)
        Button(text="Modify Selected", command="", bg="purple", fg="white").grid(row=8,column=1,sticky=W)

    def on_add_contact_button_clicked(self):
        self.add_new_contact()

    def on_delete_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_contacts()

    def add_new_contact(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO contact_list VALUES(NULL,?, ?,?)'
            parameters = (self.namefield.get(),self.emailfield.get(), self.numfield.get())
            self.execute_db_query(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
            self.view_contacts()

        else:
            self.message['text'] = 'name,email and number cannot be blank'
        self.view_contacts()

    def new_contacts_validated(self):
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) != 0 and len(self.numfield.get()) != 0

    def view_contacts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM contact_list order by name desc'
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
            self.tree.insert('',0, text=row[1], values=(row[2],row[3]))

    def delete_contacts(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contact_list where name = ?'
        self.execute_db_query(query,(name,))
        self.message['text'] = f'Contacts for {name} deleted'
        self.view_contacts()

if __name__ == '__main__':
    root  = Tk()
    root.title('My Contacts List')
    application = Contacts(root)
    root.mainloop()
