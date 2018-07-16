#!/usr/bin/python3

import tkinter as tk
import time
import socket
import _thread as th
import queue as qu
import sys

class message1:
    def __init__(self, master, bQ, aC, name):
        self.master = master
        self.exit_request = False
        self.bQ = bQ
        self.server = aC
        self.name = name
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

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        self.quit_button = tk.Button(self.button_frame, text="Quit", fg="red", command=self.quit)
        self.quit_button.pack()

        self.text_display.update()
        master.after(100,self.check_queue)

        self.serverThread = th.start_new_thread(self.serverListen,tuple())

    def serverListen(self):
        while not self.exit_request:
            inbound = self.server.recv(1024).decode()
            if len(inbound) > 0:
                command = inbound.rstrip().split(' ')
                print("Got Here inbound:  ",command)
                if command[1] == '\\ping':
                    data = self.name+': '+'\\pong'+' '+command[2]
                    print("Got Here Ping:  "+data)
                    self.server.send(data.encode())
                if command[1] == '\\pong':
                    print("Got Here Pong:  "+inbound)
                    pingtime = float(command[2])
                    inbound = inbound+' '+str(time.time())+' '+str(time.time()-pingtime)
                self.bQ.put(inbound)
        self.server.close()

    def quit(self):
        self.exit_request = True
        data = self.name+" has left the chat."
        self.server.send(data.encode())
        self.master.destroy()

    def send_text(self, event):
        newText = self.text_input.get()
        if newText == '\\quit':
            self.quit()
        else:
            if newText == '\\ping':
                newText = newText+' '+str(time.time())
            data = self.name+": "+newText
            self.server.send(data.encode())
            self.text_input.delete(0, tk.END)

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

configDict = {}
try:
    with open('./scopeChat.config', 'rt') as configFile:
        for line in configFile:
            if line.lstrip()[0] != '#':
                configKey, configValue = line.split('=')
                configDict[configKey] = configValue.rstrip()
except IOError:
    print("There was an error opening the config file!")
    print("Creating a default config file...")
    with open('./scopeChat.config', 'wt') as newFile:
        newFile.write("name=anon\n")
        newFile.write("server=localhost\n")
        newFile.write("port=5406")
    print("...and exiting...")
    sys.exit()

try:
    myName = configDict['name']
except KeyError:
    myName = 'anon'
    print("Default: Setting name to \'"+myName+"\'")

try:
    serverIP = configDict['server']
except KeyError:
    print("Must specify server IP address in scopeChat.config!")
    sys.exit()

try:
    myPort = configDict['port']
except KeyError:
    myPort = '5406'
    print("Default: Setting port to \'"+myPort+"\'")

q = qu.Queue()
serverconnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverconnect.connect((serverIP, 5406))

root = tk.Tk()
my_gui = message1(root, q, serverconnect, myName)
root.mainloop()
