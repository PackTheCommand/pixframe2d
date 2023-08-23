"""



style = ttk.Style()
style.theme_use("azure")  # Use the "clam" theme for a dark-themed look
        style.configure("TScrollbar",
                        background='#333440',
                        troughcolor="#76818E",
                        gripcount=0,
                        darkcolor='#444654',
                        lightcolor='#444654',
                        bordercolor='#444654')

        style.configure("TNotebook", background="#2E2E2E")  # Dark gray background
        style.configure("TNotebook.Tab", background="#3E3E3E", foreground="white")  # Dark gray tab with white text
        style.map("TNotebook.Tab", background=[("selected", "#505050")])  # Selected tab color
        style.configure("TCheckbutton", background="#444654", foreground="white", highlightbackground="#444654",
                        highlightcolor="#444654", font=tkfont.Font(size=10))
        style.map("TCheckbutton",
                  background=[("active", "#444654"), ("!active", "#333")],
                  foreground=[("active", "white"), ("!active", "white")],
                  highlightbackground=[("active", "#333440"), ("!active", "#333")],
                  highlightcolor=[("active", "#333440"), ("!active", "#333")])"""