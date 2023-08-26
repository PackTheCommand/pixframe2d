import json

import tkinter as  tk
from tkinter import ttk
class nbt_directEdit:
    def __init__(self,object):

         self.object = object
         self.nbt_plain=json.dumps(self.object["nbt"],indent=1)
         self.r=tk.Tk()
         root=self.r
         root.tk.call("source", "ttk_theme/azure.tcl")
         root.tk.call("set_theme", "dark")

         self.r.title("nbt_directEdit")

         self.text=tk.Text(self.r)
         self.text.pack()
         self.text.insert(tk.END,self.nbt_plain)
         self.text.tag_configure("error",foreground="red")


         b=ttk.Button(self.r,text="save",command=self.save)
         b.pack()
    def save(self):
     try:
          self.object["nbt"]=json.loads(self.text.get("1.0",tk.END))
          self.r.destroy()
          return self.object
     except:
          self.text.tag_add("error","1.0","end")
