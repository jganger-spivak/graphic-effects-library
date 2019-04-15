import tkinter as tk
import pygame

pygame.init()
class Application(tk.Frame):
    def __init__(self, master=None, width=400, height=400):
        super().__init__(master)
        self.master = master
        self.x = tk.IntVar()
        self.y = tk.IntVar()
        self.x.set(0)
        self.y.set(0)
        self.cmds = [
            'RGB',
            'RECT',
            'CIRCLE'
        ]
        self.selectedcmd = tk.StringVar()
        self.selectedcmd.set(self.cmds[0])
        self.width = tk.IntVar()
        self.height = tk.IntVar()
        self.width.set(10)
        self.height.set(10)
        self.rvalue = tk.IntVar()
        self.gvalue = tk.IntVar()
        self.bvalue = tk.IntVar()
        self.rvalue.set(255)
        self.gvalue.set(0)
        self.bvalue.set(0)
        self.winwidth = width
        self.winheight = height
        self.color = pygame.Color(self.rvalue.get(), self.gvalue.get(), self.bvalue.get())
        self.displaycolor = '#FF0000'
        self.pack()
        self.create_widgets()
        self.screen = pygame.display.set_mode((self.winwidth, self.winheight))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, self.winwidth, self.winheight))
        pygame.display.flip()
    def create_widgets(self):
        self.winfo_toplevel().title("GEL Editor")

        self.cmdselect = tk.OptionMenu(self, self.selectedcmd, *self.cmds)
        self.cmdselect.pack(side='top')

        self.xlabel = tk.Label(self, text='X location')
        self.xlabel.pack(side='top')
        self.xentry = tk.Entry(self, exportselection=0)
        self.xentry.pack(side='top')
        
        self.ylabel = tk.Label(self, text='Y location')
        self.ylabel.pack(side='top')
        self.yentry = tk.Entry(self, exportselection=0)
        self.yentry.pack(side='top')
        
        self.widthlabel = tk.Label(self, text='Object width/radius')
        self.widthlabel.pack(side='top')
        self.widthentry = tk.Entry(self, exportselection=0)
        self.widthentry.pack(side='top')
        
        self.heightlabel = tk.Label(self, text='Object height')
        self.heightlabel.pack(side='top')
        self.heightentry = tk.Entry(self, exportselection=0)
        self.heightentry.pack(side='top')
        
        self.add = tk.Button(self)
        self.add["text"] = '==Add Object=='
        self.add['command'] = self.add_element
        self.add.pack(side='top')

        self.colorlabel = tk.Label(self, text='Color (Red, Green, Blue) format (0-255)')
        self.colorlabel.pack(side='right')
        
        self.redentry = tk.Entry(self, exportselection=0)
        self.redentry.pack(side='left')
        self.greenentry = tk.Entry(self, exportselection=0)
        self.greenentry.pack(side='left')
        self.blueentry = tk.Entry(self, exportselection=0)
        self.blueentry.pack(side='left')

        self.currentcolor = tk.Label(self, text='CURRENT COLOR', fg=self.displaycolor)
        self.currentcolor.pack(side='bottom')
        
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def updateValues(self):
        if self.selectedcmd.get() == 'RGB':
            if not int(self.redentry.get()) == self.color.r:
                self.rvalue.set(int(self.redentry.get()))
            if not int(self.greenentry.get()) == self.color.g:
                self.gvalue.set(int(self.greenentry.get()))
            if not int(self.blueentry.get()) == self.color.b:
                self.bvalue.set(int(self.blueentry.get()))
        elif self.selectedcmd.get() == 'RECT':
            try:
                self.x.set(int(self.xentry.get()))
            except ValueError:
                print('ERROR: Please enter a number for X value')
            try:
                self.y.set(int(self.yentry.get()))
            except ValueError:
                print('ERROR: Please enter a number for Y value')
            try:
                self.width.set(int(self.widthentry.get()))
            except ValueError:
                print('ERROR: Please enter a number for width value')
            try:
                self.height.set(int(self.heightentry.get()))
            except ValueError:
                print('ERROR: Please enter a number for height value')
        
    def add_element(self):
        self.updateValues()
        if self.selectedcmd.get() == 'RECT':
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x.get(), self.y.get(), self.width.get(), self.height.get()))
        if self.selectedcmd.get() == 'RGB':
            self.color = pygame.Color(self.rvalue.get(), self.gvalue.get(), self.bvalue.get())
            self.displaycolor = '#%02x%02x%02x' % (self.rvalue.get(), self.gvalue.get(), self.bvalue.get())
            self.currentcolor['fg'] = self.displaycolor
        if self.selectedcmd.get() == 'CIRCLE':
            pass
        pygame.display.flip()

root = tk.Tk()
app = Application(master=root, width=int(input('Enter width:')), height=int(input('Enter height:')))
app.mainloop()
pygame.quit()
