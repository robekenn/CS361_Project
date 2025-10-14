import tkinter as tk
root = tk.Tk()
root.title("By Bible App") # Set window title
root.geometry("400x300") # Set window size

label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20) # Pack the label with padding

button = tk.Button(root, text="Click Me", command=lambda: print("Button Clicked!"))
button.pack()

root.mainloop()