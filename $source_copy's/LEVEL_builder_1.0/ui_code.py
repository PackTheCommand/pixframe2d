from tkinter import Frame, Label


class Collor:
    selector_none="#000000"
    highlight="#000000"
    bg="#000000"

class ScrollableFrame(Frame):
    def __init__(self, width=100, height=100, bg=Collor.bg, **kw):

        super().__init__(bg=bg, width=width, height=height, **kw)

        f = Frame(master=self, bg=bg)
        self.innerFrame = f
        self.width = width
        self.height = height
        f.place(x=0, y=0, width=width, height=height)
        self.re_bind()
        # f.bind("<MouseWheel>", lambda e: self.onScroll(e, f))
        f.bind()
        ef = Frame(master=self, width=width * 10, height=4, bg=Collor.selector_none)
        ef.place(x=0, y=height - 4)
        ef.bind("<Configure>", self.updateHeight)

        self.curs = Frame(master=self, bg=Collor.highlight, height=10, width=6, highlightthickness=0)
        Label(master=self.curs)
        self.curs.place(y=0, x=-6, height=10, )

    def updateHeight(self, u=None):
        # print("h",self.innerFrame.winfo_height(),self.innerFrame.place_info())
        self.innerFrame.place_configure(height=self.innerFrame.winfo_reqheight())

    def forget_bind(self):
        self.unbind_all("<MouseWheel>")

    def re_bind(self):
        self.innerFrame.bind_class('.', "<MouseWheel>", lambda e: self.onScroll(e))
        self.innerFrame.configure(highlightbackground=Collor.selector_none, highlightcolor=Collor.selector_none)

    def updateWidth(self, u):
        self.configure(width=self.innerFrame.winfo_width())
        self.innerFrame.bind_class('.', "<MouseWheel>", lambda e: self.onScroll(e))

    def onScroll(self, e, delta=0):
        self.updateHeight(1)

        f = self.innerFrame
        y = int(f.place_info()["y"])
        w = int(f.winfo_reqheight()) - self.winfo_height()
        # print(self)
        if not delta:
            delta = e.delta

        if delta > 0:
            y += 20
        else:
            y -= 20
        # print(y+self.winfo_height(),self.innerFrame.winfo_reqheight())
        if ((-y) > w):
            # print("None")
            return
        elif ((y) > 0):
            # print("None")
            return

        f.place_configure(y=y)
        if y == 0:
            y = 1
        hight_frame = self.winfo_height()
        rest = hight_frame / self.innerFrame.winfo_height()
        # print(hight_frame, self.innerFrame.winfo_height(), (y),rest,self.width,hight_frame/rest)

        new_height = hight_frame * rest

        # print(new_height, self.height)
        self.curs.configure(height=new_height, )

        self.curs.place_configure(y=((hight_frame * rest) - new_height) - y, height=new_height,
                                  x=self.winfo_width() - 6)

    def getInnerFrame(self):
        return self.innerFrame