import Tkinter as tk
import time
import thread
import Queue as qu

def friend(aQ, kill):
	while not kill[0]:
		time.sleep(.5)
		aQ.put("Hey man, what's up?")

class message1:
    def __init__(self, master, killer, bQ):
        self.master = master
	self.killer = killer
        self.bQ = bQ
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

        self.text_display.update()
        master.after(100,self.check_queue)

    def send_text(self, event):
        newText = self.text_input.get()
        self.recent_message = newText
        if newText == '\\quit':
            self.killer[0] = True
            self.master.destroy()
        self.text_input.delete(0, tk.END)
        self.show_text()

    def show_text(self):
        self.text_display.insert(tk.END, self.recent_message+'\n')
        self.text_display.see(tk.END)
        self.text_display.update()
        self.num_messages += 1

    def check_queue(self):
        while not self.bQ.empty():
            try:
                mes = self.bQ.get(timeout=0.01)
                self.bQ.task_done()
            except:
                break
            self.recent_message = mes
            self.show_text()
        self.master.after(100, self.check_queue)

q = qu.Queue()
fKill = [False,]
myFriend = thread.start_new_thread(friend,(q,fKill))

root = tk.Tk()
my_gui = message1(root, fKill, q)
root.mainloop()
