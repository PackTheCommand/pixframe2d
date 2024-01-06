import json

import tkinter as tk
from tkinter import ttk


class nbt_directEdit:
     def __init__(self, object):

          self.object = object
          self.nbt_plain = json.dumps(self.object["nbt"], indent=1)
          self.r = tk.Tk()
          self.closed=False
          root = self.r
          root.tk.call("source", "ttk_theme/azure.tcl")
          root.tk.call("set_theme", "dark")

          self.r.title("nbt_directEdit")

          self.text = tk.Text(self.r)
          self.text.pack()
          self.text.insert(tk.END, self.nbt_plain)
          self.text.tag_configure("error", foreground="red")

          b = ttk.Button(self.r, text="save", command=self.save)
          b.pack()
          self.b=b
          self.liveControlNbt()

     def liveControlNbt(self):
          try:
               json.loads(self.text.get("1.0", tk.END))
               self.text.tag_remove("error", "1.0", "end-1c")
               #self.b["state"] = "normal"
          except Exception:
               self.text.tag_add("error", "1.0", "end")
               #self.b["state"] = "disabled"
          if not self.closed:
               self.r.after(100, self.liveControlNbt)





     def save(self):
         try:
             self.object["nbt"] = json.loads(self.text.get("1.0", tk.END))
             self.r.destroy()
             self.closed =True
             return self.object
         except:
             self.text.tag_add("error", "1.0", "end")
