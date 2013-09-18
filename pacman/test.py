# nonResizableDemo.py

from Tkinter import *

def keyPressed(event,canvas):
  if event.keysym == "Up":
    print "here"
    canvas.config(width = 200, height = 400)

def redrawAll(canvas):
    canvas.delete(ALL)
    # Draw the demo info
    font = ("Arial", 16, "bold")
    msg = "Non-Resizable Demo"
    canvas.create_text(canvas.width/2, canvas.height/3, text=msg, font=font)
    # Draw the canvas size
    size = ( canvas.width, canvas.height )
    msg = "size = " + str(size)
    canvas.create_text(canvas.width/2, canvas.height*2/3, text=msg, font=font)

def init(canvas):
    canvas.width = canvas.winfo_reqwidth() - 4
    canvas.height = canvas.winfo_reqheight() - 4
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    canvas = Canvas(root, width=400, height=200)
    canvas.pack(fill=BOTH, expand=YES)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    def wrapKeyPressed(event):
      keyPressed(event,canvas)
    root.bind("<KeyPress>", wrapKeyPressed)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()