import tkinter as tk


def create_window(food_database):
  window = tk.Tk()
  window.title("Nutrition Tracker")
  window.geometry("700x500")

  header_frame = tk.Frame(window, bg="light gray", width=200, height= 300, bd=3, relief=tk.RIDGE)
  header_frame.pack( fill='x', side='top')

  label = tk.Label(header_frame, text="Nutrition Tracker", fg='white', font=("Arial", 20, "bold"), bg='lightblue')
  label.pack()

  container_frame = tk.Frame(window, bg="green", width=200, height=300, bd=3, relief=tk.RIDGE)
  container_frame.pack(fill='both', expand=True)

  food_name_label = tk.Label(container_frame, text="Food Name")
  food_name = tk.Entry(container_frame) 

  food_name_label.pack()
  food_name.pack()

  def add_food():
    food = food_database.get_food(food_name.get())
    if food is None:
      status_label.config(text="Food not found") 
      return False
    
    status_label.config(text='Food found')
    food_name.delete(0, tk.END)
    return True

  status_label =tk.Label(container_frame, text="")
  status_label.pack()
    

  add_food_btn =tk.Button(container_frame, text="Add Food", command=add_food)
  add_food_btn.pack()





  summary_frame = tk.Frame(window, bg="blue", width=200, height=300, bd=3, relief=tk.RIDGE)
  summary_frame.pack(fill='x', side='bottom')
    

  window.mainloop()