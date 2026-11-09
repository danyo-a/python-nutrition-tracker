import tkinter as tk


def change_message():
  message.set(f'Hello {user_name.get()}')

window = tk.Tk()
window.title("My First GUI")
window.geometry("400x300")
user_name = tk.StringVar()
 
entry = tk.Entry(window, textvariable=user_name)
entry.pack()

message = tk.StringVar()
label = tk.Label(window, textvariable=message)
label.pack(pady=20)
submit = tk.Button(window, text="Click Me",command=change_message)
submit.pack()
window.mainloop()


