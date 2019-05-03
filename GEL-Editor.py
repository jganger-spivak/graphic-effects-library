import tkinter as tk
from tkinter import filedialog
import pygame

pygame.init()
class Application(tk.Frame):
    def __init__(self, master=None, width=400, height=400):
        super().__init__(master)
        self.master = master
        self.x = tk.IntVar()
        self.loadedText = 'SIZE: ' + str(width) + ', ' + str(height) + '\n'
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
        self.screen = pygame.display.set_mode((int(self.winwidth), int(self.winheight)))
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
            self.loadedtext += 'RGB: ' + str(self.rvalue.get()) + ', ' + str(self.gvalue.get()) + ', ' + str(self.bvalue.get()) + '\nRECT: (' + str(self.x.get()) + ', ' + str(self.y.get()) + ', ' + str(self.width.get()) + ', '  + str(self.height.get()) + ')\n'
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x.get(), self.y.get(), self.width.get(), self.height.get()))
        if self.selectedcmd.get() == 'RGB':
            self.color = pygame.Color(self.rvalue.get(), self.gvalue.get(), self.bvalue.get())
            self.displaycolor = '#%02x%02x%02x' % (self.rvalue.get(), self.gvalue.get(), self.bvalue.get())
            self.currentcolor['fg'] = self.displaycolor
        if self.selectedcmd.get() == 'CIRCLE':
            pass
        pygame.display.flip()
    def save(self):
        raise NotImplementedError
    def load(self):
        filepath = filedialog.askopenfilename()

    
    def compileLines(self, textlines, scalar):
      currentColor = pygame.Color(255, 255, 255)
      
      print('CompileLine run')
      maxwidth = 0
      maxheight = 0
      for line in textlines:
        if not line == "":
            if line[0:4] == "RGB:":
              datavals = line.replace(" ", "").replace("RGB:", "").split(",")
              currentColor.r = int(datavals[0])
              currentColor.g = int(datavals[1])
              currentColor.b = int(datavals[2])
            elif line[0:5] == "RGBA:":
              datavals = line.replace(" ", "").replace("RGBA:", "").split(",")
              currentColor.r = int(datavals[0])
              currentColor.g = int(datavals[1])
              currentColor.b = int(datavals[2])
              currentColor.a = int(datavals[3])
            elif line[0:5] == "RECT:":
              cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("RECT:", "")
              datavals = cleanline.split(",")
              x = int(datavals[0])
              y = int(datavals[1])
              width = int(datavals[2])
              height = int(datavals[3])
              pygame.draw.rect(self.screen, currentColor, pygame.Rect(x*scalar, y*scalar, width*scalar, height*scalar))
              pygame.display.flip()
              if (y + height) > maxheight:
                maxheight = y+height
              if (x + width) > maxwidth:
                maxwidth = x+width
            elif line[0:5] == "GRAD:":
              cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("GRAD:", "")
              datavals = cleanline.split(",")
              x = int(datavals[0])
              y = int(datavals[1])
              width = int(datavals[2])
              height = int(datavals[3])
              if (y + height) > maxheight:
                maxheight = y+height
              if (x + width) > maxwidth:
                maxwidth = x+width
              direction = datavals[4]
              endColor = pygame.Color(255, 255, 255)
              gradColor = pygame.Color(currentColor.r, currentColor.g, currentColor.b)
              endColor.r = int(datavals[5])
              endColor.g = int(datavals[6])
              endColor.b = int(datavals[7])
              try:
                endColor.a = int(datavals[8])
                if direction == 'side':
                  
                  diffred = currentColor.r - endColor.r
                  diffgreen = currentColor.g - endColor.g
                  diffblue = currentColor.b - endColor.b
                  diffalpha = currentColor.a - endColor.a
                  
                  rstep = int(diffred / width)
                  gstep = int(diffgreen / width)
                  bstep = int(diffblue / width)
                  astep = int(diffalpha / width)
                  for line in range(0, int(width*scalar)):
                    pygame.draw.rect(self.screen, gradColor, pygame.Rect((x+line)*scalar, y*scalar, scalar, height*scalar))
                    pygame.display.flip()
                    if endColor.r > currentColor.r:
                      gradColor.r += abs(rstep)
                    else:
                      gradColor.r -= rstep
                    
                    if endColor.g > currentColor.g:
                      gradColor.g += abs(gstep)
                    else:
                      gradColor.g -= gstep
                    
                    if endColor.b > currentColor.b:
                      gradColor.b += abs(bstep)
                    else:
                      gradColor.b -= bstep

                    if endColor.a > currentColor.a:
                      gradColor.a += abs(astep)
                    else:
                      gradColor.a -= astep
                    
                    
                elif direction == 'down':
                  raise NotImplementedError
                elif direction == 'circle':
                  diffred = currentColor.r - endColor.r
                  diffgreen = currentColor.g - endColor.g
                  diffblue = currentColor.b - endColor.b
                  diffalpha = currentColor.a - endColor.a
                  
                  rstep = int(diffred / width)
                  gstep = int(diffgreen / width)
                  bstep = int(diffblue / width)
                  astep = int(diffalpha / width)
                  for line in range(0, int((width*scalar)/2)):
                    pygame.draw.circle(self.screen, gradColor, (int(x*scalar), int(y*scalar)), abs(line-int((width*scalar)/2)), int(scalar))
                    pygame.display.flip()
                    print(gradColor)
                    if endColor.r > currentColor.r:
                      gradColor.r += abs(rstep)
                    else:
                      gradColor.r -= rstep
                    
                    if endColor.g > currentColor.g:
                      gradColor.g += abs(gstep)
                    else:
                      gradColor.g -= gstep
                    
                    if endColor.b > currentColor.b:
                      gradColor.b += abs(bstep)
                    else:
                      gradColor.b -= bstep

                    if endColor.a > currentColor.a:
                      gradColor.a += abs(astep)
                    else:
                      gradColor.a -= astep
              except IndexError:
                raise NotImplementedError
            elif line[0:7] == "CIRCLE:":
              cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("CIRCLE:", "")
              datavals = cleanline.split(",")
              x = int(datavals[0])
              y = int(datavals[1])
              radius = int(datavals[2])
              if (y + radius*2) > maxheight:
                maxheight = y+radius*2
              if (x + radius*2) > maxwidth:
                maxwidth = x+radius*2
              pygame.draw.circle(self.screen, currentColor, (int(x*scalar), int(y*scalar)), radius*scalar)
              pygame.display.flip()
      print('CompileLine finished')

root = tk.Tk()
fileloaded = False
if input('Load file? Y/N').upper() == 'Y':
    scalar = float(input('Please enter scale value, or 1 for no scaling: '))
    fh = open(filedialog.askopenfilename())
    text = fh.read()
    width = int(int(text.split('\n')[0].replace('SIZE:', '').split(',')[0]) * scalar)
    height = int(int(text.split('\n')[0].replace('SIZE:', '').split(',')[1]) * scalar)
    app = Application(master=root, width=width, height=height)
    app.loadedText = text
    text = '' #Garbage collection woo!
    app.compileLines(app.loadedText, scalar)
    pygame.display.flip()
    
else:
    app = Application(master=root, width=int(input('Enter width:')), height=int(input('Enter height:')))
app.mainloop()
pygame.quit()
