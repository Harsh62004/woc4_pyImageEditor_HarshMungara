from tkinter import *

root = Tk()

mylabel = Label(root, text="Hello World!")
mylabel2= Label(root,text="We are just learning grid").grid(row=4,column=5)

mylabel.grid(row=0,column=1)

'''mylabel.pack()'''

root.mainloop()