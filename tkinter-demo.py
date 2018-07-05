import Tkinter as tk
import time

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = tk.Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

class message1:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Chat Window")
        self.recent_message = ''
	self.num_messages = 0
	self.h = 10
        self.w = 90

        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack( side = tk.RIGHT, fill='y')

        self.text_display = tk.Text(self.master, wrap=tk.WORD, height=self.h, width=self.w, yscrollcommand=self.scrollbar.set)
        self.text_display.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text_display.yview)

        self.text_input = tk.Entry(self.master)
        self.text_input.bind("<Return>", self.send_text)
        self.text_input.focus()
        self.text_input.pack(fill='x', expand=True)

    def send_text(self, event):
        newText = self.text_input.get()
        self.recent_message = newText
        if newText == '\\quit':
            self.master.destroy()
        self.text_input.delete(0, tk.END)
        self.show_text()

    def show_text(self):
        self.text_display.insert(tk.END, self.recent_message+'\n')
        self.text_display.see(tk.END)
        self.num_messages += 1
      #  while self.num_messages > self.h:
      #      deleted = ''
      #      while deleted != '\n':
      #          deleted = self.text_display.get('0.0')
      #          self.text_display.delete('0.0')
      #      self.num_messages -= 1
        

root = tk.Tk()
#my_gui = MyFirstGUI(root)
my_gui = message1(root)
root.mainloop()
