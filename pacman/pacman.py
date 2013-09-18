import os
from Tkinter import *
import random
import sys
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import string


default_path = sys.path[0] #home directory

class Node (): #nodes used in astar pathfinding
    def __init__(self,pos,endpos):
      self.g = 0
      self.h = 0
      self.pos = pos
      self.endpos = endpos

    def setG(self,g):
      self.g = g

    def getG(self):
      return self.g

    def getH(self):
      """ This function returns the manhattan heuristic for astar.
      It takes the perfect path from the point to the ending, and then returns 
      the magnitude of that path."""
      return abs(self.pos[0] - self.endpos[0]) + abs(self.pos[1] - self.endpos[1])

    def getF(self):
      return self.g + self.getH()

    def setParent(self,parent):
      self.parent = parent

    def getParent(self):
      return self.parent

    def __hash__(self):
      #faster, simpler hashing
      return hash(self.pos)

    def __eq__(self,other):
      #We need to make this function so that nodes will be recognized in sets
      return self.pos == other.pos #no two nodes have the same position7





def pathfind(board,startpos,endpos):
  """A Star Pathfinding Function"""
  openlist = set()
  closedlist = set()
  startNode = Node(startpos,endpos)
  startNode.setParent = None
  dirs = [(0,1),(1,0),(0,-1),(-1,0)]
  currentNode = startNode
  currentNode.setG(0)
  openlist.add(currentNode)
  #start the loop
  while currentNode.pos != endpos and len(openlist) != 0:
      currentNode = getLowestFNode(openlist) #get the lowest F
      openlist.remove(currentNode)
      closedlist.add(currentNode)
      for direction in dirs: #try every neighbornode
        neighborNode = Node((currentNode.pos[0]+direction[0],
          currentNode.pos[1]+direction[1]),endpos)
        if neighborNode not in closedlist: #it might eb what we're looking for
          if neighborNode not in openlist and isValidMove(neighborNode,board):
            neighborNode.setG(currentNode.getG()+1)
            neighborNode.setParent(currentNode)
            openlist.add(neighborNode)
          elif neighborNode in openlist and isValidMove(neighborNode,board):
            #if we find a better way to this node, we reset its G value
            tempG = currentNode.getG() + 1
            if tempG < neighborNode.getG():
              neighborNode.setG(tempG)
              neighborNode.setParent(currentNode)
  
  #now we have to get the path back
  pathList = []
  while currentNode.pos != startpos: #keep going back in the list
    pathList.append(currentNode.pos)
    currentNode = currentNode.getParent()

  # The list is backwards, so we must reverse it

  pathList = pathList[::-1]

  return pathList

def getLowestFNode(openlist): #takes in a list of nodes
  lowestF = 1000 #arbitrarily high
  lowestFNode = None
  for node in openlist:
    tmp = node.getF()
    if node.getF() < lowestF:
      lowestFNode = node
      lowestF = tmp
  return lowestFNode


def isValidMove(node,board):
  pos = node.pos
  #check if the position is in bounds, and that it is a legal tile
  return ((len(board) > pos[0] >= 0) and (len(board[0]) > pos[1] >= 0) and 
  (board[pos[0]][pos[1]] == 0 or board[pos[0]][pos[1]] == 17 
    or board[pos[0]][pos[1]] == 18))

def isValidPosString(string):
  return (len(string.split(" ")) == 2 and string.split(" ")[0].isdigit() and
    string.split(" ")[1].isdigit())


def isValidCornersString(string):
  a = string.split(" ")
  if len(a) != 6:
    return False
  for c in a:
    if not c.isdigit():
      return False
  return True


def saveBoard(canvas):
  #get all the board data
  message = "All Rows and Columns start at 0."
  title = "Information"
  tkMessageBox.showinfo(title, message)
  message = "Where does pacman start? Ender an integer row,\
   a space, and then an integer column"
  title = "Saving..."
  pacManPosString = "a"
  while not isValidPosString(pacManPosString):
    pacManPosString = tkSimpleDialog.askstring(title, message)
  message = "Where does Ghost 1 start? Ender an integer row,\
   a space, and then an integer column"
  title = "Saving..."
  ghost1PosString = "a"
  while not isValidPosString(ghost1PosString):
    ghost1PosString = tkSimpleDialog.askstring(title, message)
  message = "Where does Ghost 2 start? Ender an integer row,\
   a space, and then an integer column"
  title = "Saving..."
  ghost2PosString = "a"
  while not isValidPosString(ghost2PosString):
    ghost2PosString = tkSimpleDialog.askstring(title, message)
  message = "Where does Ghost 3 start? Ender an integer row,\
   a space, and then an integer column"
  title = "Saving..."
  ghost3PosString = "a"
  while not isValidPosString(ghost3PosString):
    ghost3PosString = tkSimpleDialog.askstring(title, message)
  (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
  message = "What are three corner positions on this boad?\
   It is important for the AI. Enter each coordinate as a row,\
    a space, then a column. Then press space again and start\
     the next coordinate. Example: \"1 1 1 12 24 1\" "
  title = "Saving..."
  cornerString = "a"
  while not isValidCornersString(cornerString):
    cornerString = tkSimpleDialog.askstring(title,message)
  #start the boardstring and write in the info
  boardString = ""
  boardString += pacManPosString + "\n"
  boardString += ghost1PosString + "\n"
  boardString += ghost2PosString + "\n"
  boardString += ghost3PosString + "\n"
  boardString += cornerString + "\n"
  message = "What is the number for this level?\
   Enter an integer between 4 and 8"
  title = "Last Step..."
  levelnum = "a"
  while True:
    levelnum = tkSimpleDialog.askstring(title, message)
    if levelnum.isdigit() and 4 <int(levelnum) <8:
      break
  for row in xrange(rows):
    for col in xrange(cols):
      boardString += str(canvas.data.tiles.index(canvas.data.board[row][col]))
      if col != cols-1: #don't add a space to the last one
        boardString += " "
    if row != rows-1:
      boardString += "\n" #don't add a newline at the end
  text_file = open("levels/%s.txt" % (levelnum),"w")
  text_file.write(boardString)
  text_file.close()
  print boardString

def resetPositions(canvas):
  canvas.data.lives -= 1
  canvas.data.pacManPos = canvas.data.defaultPacManPos
  canvas.data.ghost1.resetPos()
  canvas.data.ghost2.resetPos()
  canvas.data.ghost3.resetPos()


class Ghost(object):
  ghostCount = 0

  def __init__(self,pos):
    self.defaultpos = pos
    self.pos = pos
    self.oldpos = pos
    Ghost.ghostCount %= 3
    Ghost.ghostCount += 1
    self.number = Ghost.ghostCount
    self.mode = 0 #normal mode
    self.image = PhotoImage(file = "ghosts/%d.gif" % (Ghost.ghostCount))
    self.tempImg = False
    self.modeCount = 0
    self.animations = self.loadGhostAnimation()

  def resetPos(self):
    self.pos = self.defaultpos
    self.path = []

  def setMode(self,mode):
    self.mode = mode
    self.modeCount = 0


  def loadGhostAnimation(self):
    images = []
    for i in xrange(3):
      images.append(PhotoImage(file = "ghostanimations/%d.gif" % (i)))
    return images

  def moveGhost(self,canvas,other = None):
    if self.mode == 0:
      moveCount = canvas.data.moveCount
      if self.number == 1: #get the first ghost's path
        if moveCount >= 10: #don't scatter
          if canvas.data.moveCount == 10 or canvas.data.moveCount == 20:
            #update the path
            self.path = pathfind(canvas.data.board,self.pos,
              canvas.data.pacManPos)
            if len(self.path) != 0:
              self.oldpos = self.pos #make the move
              self.pos = self.path[0]
              self.path.pop(0)
          else:
            if len(self.path) != 0: #continue on the path
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else: #update the path
              self.path = pathfind(canvas.data.board,self.pos,
                canvas.data.pacManPos)
              self.oldpos = self.pos
              if len(self.path) != 0:
                self.pos = self.path[0]
                self.path.pop(0)
        else: #scatter
          if canvas.data.moveCount == 0:
            self.path = pathfind(canvas.data.board,self.pos,
              canvas.data.corners[0]) #default scatter to same corner
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
          else:
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              self.path = pathfind(canvas.data.board,self.pos,
              canvas.data.corners[1]) #scatter to a new corner
      elif self.number == 2: #time for ghost 2's path
        if moveCount < 10 or moveCount >= 20:
          if moveCount == 0 or moveCount == 20: #set the path
            goalPos = getSpotAheadofPacman(canvas,4)
            if goalPos != self.pos:
              self.path = pathfind(canvas.data.board,self.pos,goalPos)
            elif goalPos == self.pos: #go after the fuck
              self.path = pathfind(canvas.data.board,
                self.pos,canvas.data.pacmanPos)
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
          else: #just continue on the path
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              self.path = pathfind(canvas.data.board,
                self.pos,canvas.data.pacManPos)
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
        else: #scatter, bitch
          if moveCount == 10:
            self.path = pathfind(canvas.data.board,
              self.pos,canvas.data.corners[1])
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
          else:
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              #scatter somewhere else, we're too close to the corner
              self.path = pathfind(canvas.data.board,
              self.pos,canvas.data.corners[0])
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
      elif self.number == 3: #last ghost's path
        if moveCount <20:
          if moveCount == 0 or moveCount == 10:
            #calculate goal position
            otherGhostPos = other.pos
            pacManAdvancedPos = getSpotAheadofPacman(canvas,2)
            (drow,dcol) = (pacManAdvancedPos[0]-otherGhostPos[0],
              pacManAdvancedPos[1]-otherGhostPos[1])
            hopefulPos = (drow*2,dcol*2)
            pathList = pathfind(canvas.data.board,self.pos,hopefulPos)
            actualPos = pathList[-1] 
            #the last value of this list is the closest we are going to get
            if actualPos != self.pos:
              self.path = pathfind(canvas.data.board,self.pos,actualPos)
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              self.path = pathfind(canvas.data.board,
                self.pos,canvas.data.pacManPos)
          else: #just continue on the path
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              self.path = pathfind(canvas.data.board,
                self.pos,canvas.data.pacManPos)
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
        else:
          if moveCount == 20:
            self.path = pathfind(canvas.data.board,
              self.pos,canvas.data.corners[2])
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
          else:
            if len(self.path) != 0:
              self.oldpos = self.pos
              self.pos = self.path[0]
              self.path.pop(0)
            else:
              self.path = pathfind(canvas.data.board,
              self.pos,canvas.data.corners[1]) #other corner if too close
    elif self.mode == 1: #you're liable to be eaten, run away
      if self.modeCount == 0:
        #randomly scatter...
        choice = random.choice(canvas.data.corners)
        self.path = pathfind(canvas.data.board,self.pos,choice)
        if len(self.path) != 0:
          self.oldpos = self.pos
          self.pos = self.path[0]
          self.path.pop(0)
        else:
          while self.pos == choice:
            choice = random.choice(canvas.data.corners)
          self.path = pathfind(canvas.data.board,self.pos,choice)
          self.oldpos = self.pos
          self.pos = self.path[0]
          self.path.pop(0)
        self.modeCount += 1
        if self.modeCount == 30:
          self.mode = 0
          self.modeCount = 0
      elif self.modeCount == 30:
        self.mode = 0
        self.modeCount = 0
      else:
        if len(self.path) != 0:
          self.oldpos = self.pos
          self.pos = self.path[0]
          self.path.pop(0)
        else:
          choice = random.choice(canvas.data.corners)
          while self.pos == choice:
            choice = random.choice(canvas.data.corners)
          self.path = pathfind(canvas.data.board,self.pos,choice)
          self.oldpos = self.pos
          self.pos = self.path[0]
          self.path.pop(0)
        self.modeCount += 1
        if self.modeCount == 30:
          self.mode = 0
          self.modeCount == 0
    elif self.mode == 2: #you've been eaten
      #go back home
      self.path = pathfind(canvas.data.board,self.pos,self.defaultpos) 
      if len(self.path) != 0:
        self.oldpos = self.pos
        self.pos = self.path[0]
      else:
        self.mode = 0

  def drawGhost(self, canvas):
    if self.mode == 0:
      if not self.oldpos == self.pos:
        (row,col) = self.pos
        if self.oldpos[0] > self.pos[0]: #decreasing row
          (cx,cy) = (col*16+8,(row+1)*16+8-2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,image = self.image)
        elif self.oldpos[0] < self.pos[0]: #increasing row
          (cx,cy) = (col*16+8,(row-1)*16+8+2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,image = self.image)
        elif self.oldpos[1] > self.pos[1]: #decreasing col
          (cx,cy) = ((col+1)*16+8-2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,image = self.image)
        elif self.oldpos[1] < self.pos[1]: #increasing row
          (cx,cy) = ((col-1)*16+8+2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,image = self.image)
      else:
        (row,col) = self.pos
        (cx,cy) = (col*16+8,row*16+8)
        self.tempImg = canvas.create_image(cx,cy,image = self.image)
    elif self.mode == 1:
      if not self.oldpos == self.pos:
        (row,col) = self.pos
        if self.oldpos[0] > self.pos[0]: #decreasing row
          (cx,cy) = (col*16+8,(row+1)*16+8-2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,
            image = self.animations[self.modeCount % 2])
        elif self.oldpos[0] < self.pos[0]: #increasing row
          (cx,cy) = (col*16+8,(row-1)*16+8+2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,
            image = self.animations[self.modeCount % 2])
        elif self.oldpos[1] > self.pos[1]: #decreasing col
          (cx,cy) = ((col+1)*16+8-2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,
            image = self.animations[self.modeCount % 2])
        elif self.oldpos[1] < self.pos[1]: #increasing row
          (cx,cy) = ((col-1)*16+8+2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,
            image = self.animations[self.modeCount % 2])
      else:
        (row,col) = self.pos
        (cx,cy) = (col*16+8,row*16+8)
        self.tempImg = canvas.create_image(cx,cy,
          image = self.animations[self.modeCount % 2])
    elif self.mode == 2:
      if not self.oldpos == self.pos:
        (row,col) = self.pos
        if self.oldpos[0] > self.pos[0]: #decreasing row
          (cx,cy) = (col*16+8,(row+1)*16+8-2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,image = self.animations[2])
        elif self.oldpos[0] < self.pos[0]: #increasing row
          (cx,cy) = (col*16+8,(row-1)*16+8+2*canvas.data.i)
          self.tempImg = canvas.create_image(cx,cy,image = self.animations[2])
        elif self.oldpos[1] > self.pos[1]: #decreasing col
          (cx,cy) = ((col+1)*16+8-2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,image = self.animations[2])
        elif self.oldpos[1] < self.pos[1]: #increasing row
          (cx,cy) = ((col-1)*16+8+2*canvas.data.i,row*16+8)
          self.tempImg = canvas.create_image(cx,cy,image = self.animations[2])
      else:
        (row,col) = self.pos
        (cx,cy) = (col*16+8,row*16+8)
        self.tempImg = canvas.create_image(cx,cy,image = self.animations[2])

  def deleteTmp(self,canvas):
    if not self.tempImg == False:
      canvas.delete(self.tempImg)



def getSpotAheadofPacman(canvas,spot): 
  #try to get spot spaces ahead of pacman. if unable, find the next best thing
  velocity = canvas.data.pacManVelocity
  position = canvas.data.pacManPos
  (wantedPosRow,wantedPosCol) = (velocity[0]*spot + position[0],
    velocity[1]*spot + position[1])
  if wantedPosRow < 0: #above the board
    wantedPosRow = 0
  elif wantedPosRow > len(canvas.data.board)-1: 
    wantedPosRow = len(canvas.data.board) - 1
  elif wantedPosCol < 0:
    wantedPosCol = 0
  elif wantedPosCol > len(canvas.data.board[0]) - 1:
    wantedPosCol = len(canvas.data.board[0]) - 1
  if isLegalMove(wantedPosRow,wantedPosCol,canvas):
    return (wantedPosRow,wantedPosCol)
  else:
    for i in xrange(spot-1,-1,-1):
      wantedPos = (velocity[0]*i + position[0],velocity[1]*i + position[1])
    if wantedPosRow < 0: #above the board
      wantedPosRow = 0
    elif wantedPosRow > len(canvas.data.board)-1: 
      wantedPosRow = len(canvas.data.board) - 1
    elif wantedPosCol < 0:
      wantedPosCol = 0
    elif wantedPosCol > len(canvas.data.board[0]) - 1:
      wantedPosCol = len(canvas.data.board[0]) -1
    if isLegalMove(wantedPosRow,wantedPosCol,canvas):
      return (wantedPosRow,wantedPosCol)
  return canvas.data.pacManPos




class level():
  def __init__(self,number):
    self.levelNumber = number
    self.boardinfo = self.loadLevel()

  def loadLevel(self):
    """ Takes in a text file and converts it to a level output"""
    f=open(os.path.join(default_path,"levels",str(self.levelNumber) + ".txt"))
    board = [] #board will be a 2 dimensional array
    c = 0 #start a counter
    for line in f:
      if c == 0: #first line is the pacman position
        coords = line.split(" ")
        pacmanRow = int(coords[0])
        pacmanCol = int(coords[1])
        pacManPos = (pacmanRow,pacmanCol)
      elif c == 1: #ghost 1 pos
        coords = line.split(" ")
        ghost1Row = int(coords[0])
        ghost1Col = int(coords[1])
        ghost1Pos = (ghost1Row,ghost1Col)
      elif c == 2: #ghost 2 pos
        coords = line.split(" ")
        ghost2Row = int(coords[0])
        ghost2Col = int(coords[1])
        ghost2Pos = (ghost2Row,ghost2Col)
      elif c == 3: #ghost 3 pos
        coords = line.split(" ")
        ghost3Row = int(coords[0])
        ghost3Col = int(coords[1])
        ghost3Pos = (ghost3Row,ghost3Col)
      elif c == 4: #three corners
        cornerString = line.split(" ")
        corner1 = (int(cornerString[0]),int(cornerString[1]))
        corner2 = (int(cornerString[2]),int(cornerString[3]))
        corner3 = (int(cornerString[4]),int(cornerString[5]))
        corners = [corner1,corner2,corner3]
      else: #we're on the board dude
        board.append(line.split(" "))
        #creates a board of strings
      c += 1
    (rows,cols) = (len(board),len(board[0]))
    for row in xrange(rows):
      for col in xrange(cols):
        board[row][col] = int(board[row][col])
    return [board,pacManPos,ghost1Pos,ghost2Pos,ghost3Pos,corners]


def loadPacManAnimation():
  tiles = []
  for i in xrange(4):
    tiles.append([])
    for j in xrange(8):
      tiles[i].append(PhotoImage(file = "animation/%d.gif" % (i*8+j+1)))
  tiles.append(PhotoImage(file = "animation/0.gif"))
  return tiles


def loadHomeScreenImages():
  images = []
  for i in xrange(2):
    images.append(PhotoImage(file = "menuimages/%d.gif" % (i)))
  return images

def gameWon(canvas):
  canvas.data.gameOver = True
  canvas.create_rectangle(0,0,canvas.width,canvas.height,fill = "blue")
  canvas.create_text(canvas.width/2,canvas.height/10,
    text = "Congrats,You Win!", font = ("Comic Sans",10,"bold"),
     fill = "yellow")
  canvas.create_text(canvas.width/2,canvas.height/5,
    text = "Your Final Score is %s" % (canvas.data.score),
     font = ("Comic Sans",10,"bold"), fill = "yellow")
  delay = 3000 #wait 3 seconds
  canvas.after(delay,goToHomeScreen,canvas)

def placePortal(canvas):
  randomRow = random.randint(0,len(canvas.data.board)-1)
  randomCol = random.randint(0,len(canvas.data.board[0])-1)
  while canvas.data.board[randomRow][randomCol] != 18:
    randomRow = random.randint(0,len(canvas.data.board)-1)
    randomCol = random.randint(0,len(canvas.data.board[0])-1)
  canvas.data.board[randomRow][randomCol] = 20

def gameOver(canvas):
  canvas.data.gameOver = True
  canvas.delete(ALL)
  canvas.config(width = 300,height = 225)
  canvas.width = 300
  canvas.height = 225
  canvas.create_image(canvas.width/2,canvas.height/2,
    image = canvas.data.gameOverScreen)
  canvas.create_text(canvas.width/2,canvas.height/10,
    text = "Your Final Score is %s" % (canvas.data.score),
     font = ("Comic Sans",10,"bold"), fill = "yellow")
  delay = 3000 #wait 3 seconds
  canvas.after(delay,goToHomeScreen,canvas)

def checkMove(canvas):
  (row,col) = canvas.data.pacManPos
  if canvas.data.board[row][col] == 18:
    canvas.data.board[row][col] = 0
    canvas.data.pelletsEaten += 1
    canvas.data.score += 10
    if (float(canvas.data.pelletsEaten)/canvas.data.initialPellets > (0.1) and
      not canvas.data.portalPlaced):
      #make the portal to the next level
      canvas.data.portalPlaced = True
      placePortal(canvas)
  elif canvas.data.pacManPos == canvas.data.ghost1.pos:
    if canvas.data.ghost1.mode == 0:
      if canvas.data.lives == 0:
          gameOver(canvas)
      else:
        resetPositions(canvas)
    else:
      canvas.data.score += 100
      canvas.data.ghost1.mode = 2
  elif canvas.data.board[row][col] == 20: 
    #portal reached, go to the next level or quit
    if canvas.data.mode == 1:
      if canvas.data.levelnumber == 3:
        gameWon(canvas)
      else:
        canvas.data.score += 1000 #level completed bonus
        init(canvas,canvas.data.levelnumber+1)
    elif canvas.data.mode == 2:
      gameWon(canvas)
  elif canvas.data.pacManPos == canvas.data.ghost2.pos:
    if canvas.data.ghost2.mode == 0:
      if canvas.data.lives == 0:
          gameOver(canvas)
      else:
        resetPositions(canvas)
    else:
      canvas.data.score += 100
      canvas.data.ghost2.mode = 2
  elif canvas.data.pacManPos == canvas.data.ghost3.pos:
    if canvas.data.ghost3.mode == 0:
      if canvas.data.lives == 0:
          gameOver(canvas)
      else:
        resetPositions(canvas)
    else:
      canvas.data.score += 100
      canvas.data.ghost3.mode = 2
  elif canvas.data.board[row][col] == 19:
    canvas.data.board[row][col] = 0
    canvas.data.ghost1.setMode(1)
    canvas.data.ghost2.setMode(1)
    canvas.data.ghost3.setMode(1)

def mousePressed(event,canvas):
  if canvas.data.mode == 3: #must be in editing mode
    sideMargin = 50
    cellSize = 16
    topMargin = 40
    leftOffSet = (sideMargin - 2*cellSize) / 2
    topOffset = topMargin / 2
    additionalSpaceBetween = 4 #pixels
    moreSpaceBetween = 20
    (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
    (x,y) = (event.x,event.y)
    if ((leftOffSet < event.x < leftOffSet + cellSize)
     and ((topOffset < event.y < topOffset + cellSize*len(canvas.data.tiles)/2)
      + additionalSpaceBetween*len(canvas.data.tiles)/2)):
      #user is trying to change piece in first column
      canvas.data.currentPiece = canvas.data.tiles[(event.y - topOffset) / 
      (cellSize + additionalSpaceBetween)]
      redrawLevelEditor(canvas)
    elif ((leftOffSet + cellSize < event.x < leftOffSet + 2*cellSize)
     and ((topOffset < event.y < topOffset + cellSize*len(canvas.data.tiles)/2)
      + additionalSpaceBetween*len(canvas.data.tiles)/2)):
      #user is trying to change space in second column
      canvas.data.currentPiece = canvas.data.tiles[len(canvas.data.tiles)/2 + 
      (event.y - topOffset) / (cellSize + additionalSpaceBetween)]
      redrawLevelEditor(canvas)
    elif ((moreSpaceBetween + leftOffSet + 2*cellSize < x <
     moreSpaceBetween + leftOffSet + 3*cellSize + cols*cellSize)
     and (moreSpaceBetween + topOffset < y <
      moreSpaceBetween + topOffset + cellSize*rows)):
      #user is placing a piece
      row  = (y - moreSpaceBetween - topOffset) / cellSize
      col = (x - moreSpaceBetween - leftOffSet - 2*cellSize) / cellSize
      canvas.data.board[row][col] = canvas.data.currentPiece
      redrawLevelEditor(canvas)


def drawCurrentPiece(canvas):
  image = canvas.data.currentPiece
  canvas.create_image(canvas.data.canvasWidth/2 + 90,
    canvas.data.canvasHeight - 10,image = image)

def getInitialPellets(canvas):
  pellets = 0
  (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
  for row in xrange(rows):
    for col in xrange(cols):
      if canvas.data.board[row][col] == 18:
        pellets += 1
  return pellets

def rightmousePressed(event,canvas):
  if canvas.data.mode == 3:# must be in editing mode
    sideMargin = 50
    cellSize = 16
    topMargin = 40
    leftOffSet = (sideMargin - 2*cellSize) / 2
    topOffset = topMargin / 2
    additionalSpaceBetween = 4 #pixels
    moreSpaceBetween = 20
    (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
    (x,y) = (event.x,event.y)
    if ((moreSpaceBetween + leftOffSet + 2*cellSize < x < 
      moreSpaceBetween + leftOffSet + 3*cellSize + cols*cellSize)
       and (moreSpaceBetween + topOffset < y <
        moreSpaceBetween + topOffset + cellSize*rows)):
      row  = (y - moreSpaceBetween - topOffset) / cellSize
      col = (x - moreSpaceBetween - leftOffSet - 2*cellSize) / cellSize
      canvas.data.board[row][col] = canvas.data.tiles[18]
      redrawLevelEditor(canvas)


def redrawLevelEditor(canvas):
  canvas.delete(ALL)
  createSidebar(canvas)
  drawBoardLevelEditor(canvas)
  canvas.create_text(canvas.data.canvasWidth/2,10,text = "Level Editor",
    fill = "red", font = "Times 16 bold")
  canvas.create_text(canvas.data.canvasWidth/2,canvas.data.canvasHeight - 10,
    text = "Current Piece :",fill = "red", font = "Times 16 bold")
  drawCurrentPiece(canvas)



def keyPressed(event,canvas):
  if canvas.data.mode == 1 or canvas.data.mode == 2:
    if (event.keysym == "Right"):
      newRow,newCol = (canvas.data.pacManPos[0], canvas.data.pacManPos[1] + 1)
      canvas.data.wantedPacManVelocity = (0,1)
    elif (event.keysym == "Left"):
      newRow,newCol = (canvas.data.pacManPos[0], canvas.data.pacManPos[1] - 1)
      canvas.data.wantedPacManVelocity = (0,-1)
    elif (event.keysym == "Down"):
      newRow,newCol = (canvas.data.pacManPos[0] + 1, canvas.data.pacManPos[1])
      canvas.data.wantedPacManVelocity = (1,0)
    elif (event.keysym == "Up"):
      newRow,newCol = (canvas.data.pacManPos[0] - 1, canvas.data.pacManPos[1])
      canvas.data.wantedPacManVelocity = (-1,0)
  elif canvas.data.mode == 0:
    if (event.keysym == "Up"):
      canvas.data.selectedTile -= 1
      canvas.data.selectedTile %= 4
      redrawHomeScreen(canvas)
    elif (event.keysym == "Down"):
      canvas.data.selectedTile += 1
      canvas.data.selectedTile %= 4
      redrawHomeScreen(canvas)
    elif (event.keysym == "Return"):
      if canvas.data.selectedTile == 3: #quit
        sys.exit()
      elif canvas.data.selectedTile == 1:
        levelnum = "a"
        while not levelnum.isdigit():
          message = "Which level would you like to play? Enter an integer."
          title = "Select Level"
          levelnum = tkSimpleDialog.askstring(message,title)
        levelnum = int(levelnum)
        canvas.data.mode = 2 #only play one level
        canvas.data.score = 0
        canvas.data.timerFiredOn = False
        init(canvas,levelnum)
      elif canvas.data.selectedTile == 2:
        canvas.data.mode = 3 #editing move
        initLevelEditor(canvas)
      elif canvas.data.selectedTile == 0:
        canvas.data.mode = 1
        canvas.data.score = 0
        canvas.data.timerFiredOn = False
        init(canvas,1)
  elif canvas.data.mode == 3:
    if event.keysym == "s":
      saveBoard(canvas)

def createSidebar(canvas):
  """ Creates the sidebar for the level editor"""
  sideMargin = 50
  cellSize = 16
  topMargin = 40
  leftOffSet = (sideMargin - 2*cellSize) / 2
  topOffset = topMargin / 2
  additionalSpaceBetween = 4 #pixels
  for i in xrange(len(canvas.data.tiles)/2): # make the first column
    (cx,cy) = (leftOffSet + cellSize / 2,
     topOffset+cellSize*i+cellSize/2+additionalSpaceBetween*i)
    canvas.create_image(cx,cy, image = canvas.data.tiles[i])
  for i in xrange(len(canvas.data.tiles)/2): #second column
    (cx,cy) = (leftOffSet + 3 *cellSize / 2 + additionalSpaceBetween,
     topOffset+cellSize*i+cellSize/2+additionalSpaceBetween*i)
    canvas.create_image(cx,cy, 
      image = canvas.data.tiles[len(canvas.data.tiles)/2 + i])

def drawBoardLevelEditor(canvas):
  sideMargin = 50
  cellSize = 16
  topMargin = 40
  leftOffSet = (sideMargin - 2*cellSize) / 2
  topOffset = topMargin / 2
  additionalSpaceBetween = 4 #pixels
  moreSpaceBetween = 20
  (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
  for row in xrange(rows):
    for col in xrange(cols):
      canvas.create_rectangle(moreSpaceBetween + 
        leftOffSet + 2*cellSize + col*cellSize,
         moreSpaceBetween + topOffset + cellSize*row,
          moreSpaceBetween + leftOffSet + 3*cellSize + col*cellSize,
          moreSpaceBetween + topOffset + cellSize*row + cellSize,
          fill = "black", outline = "white")
      canvas.create_image(moreSpaceBetween + leftOffSet + 2*cellSize
       + col*cellSize + cellSize/2,
        moreSpaceBetween + topOffset + cellSize*row + cellSize/2,
         image = canvas.data.board[row][col])

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a

def isLegalMove(row,col,canvas):
  board = canvas.data.board
  (rows,cols) = (len(board),len(board[0]))
  if (board[row][col] == 0 or board[row][col] == 18 or board[row][col] == 17 
    or board[row][col] == 19 or canvas.data.board[row][col] == 20):
    return True
  else:
    return False

def loadTileImages():
  tiles = []
  for i in xrange(21):
    tiles.append(PhotoImage(file = "walls/%d.gif" % (i)))
  return tiles


def drawBoard(canvas):
  board = canvas.data.board
  (rows,cols) = (len(board),len(board[0]))
  extraspace = 160 #pixels at bottom of board
  cellSize = 16
  extraOffset = 4 #space between each life tile
  for row in xrange(rows):
   for col in xrange(cols):
      drawCell(canvas, row, col)
  canvas.create_text(canvas.width/2,canvas.height - 7*extraspace/8,
   text = "Lives Remaining:",font = ("ms Serif",10,"bold"),fill = "red")
  for i in xrange(-1,canvas.data.lives-1):
    (cx,cy) = (canvas.width/2,canvas.height-6*extraspace/8)
    canvas.create_image(cx+cellSize*i+extraOffset*i,cy,
      image = canvas.data.livesImage)
  canvas.create_text(canvas.width/2,canvas.height-extraspace/4,
    text = "Your score is %s" % (canvas.data.score),
    font = ("ms Serif",10,"bold"),fill = "red")



def drawCell(canvas,row,col):
  cx,cy = col*16+8,row*16+8
  canvas.create_image(cx,cy,
    image = canvas.data.tileImages[canvas.data.board[row][col]])

def drawPacMan(canvas):
  if not canvas.data.pacmanoldPos == canvas.data.pacManPos:
    (row,col) = canvas.data.pacManPos
    if canvas.data.pacmanoldPos[0] > canvas.data.pacManPos[0]: #decreasing row
      (cx,cy) = (col*16+8,(row+1)*16+8-2*canvas.data.i)
      canvas.data.pacmanImage = canvas.create_image(cx,cy,
        image = canvas.data.pacManAnimation[3][canvas.data.i])
    elif canvas.data.pacmanoldPos[0] < canvas.data.pacManPos[0]: #increase row
      (cx,cy) = (col*16+8,(row-1)*16+8+2*canvas.data.i)
      canvas.data.pacmanImage = canvas.create_image(cx,cy,
        image = canvas.data.pacManAnimation[0][canvas.data.i])
    elif canvas.data.pacmanoldPos[1] > canvas.data.pacManPos[1]: #decrease col
      (cx,cy) = ((col+1)*16+8-2*canvas.data.i,row*16+8)
      canvas.data.pacmanImage = canvas.create_image(cx,cy,
        image = canvas.data.pacManAnimation[1][canvas.data.i])
    elif canvas.data.pacmanoldPos[1] < canvas.data.pacManPos[1]: #increase row
      (cx,cy) = ((col-1)*16+8+2*canvas.data.i,row*16+8)
      canvas.data.pacmanImage = canvas.create_image(cx,cy,
        image = canvas.data.pacManAnimation[2][canvas.data.i])
  else:
    (row,col) = canvas.data.pacManPos
    (cx,cy) = (col*16+8,row*16+8)
    canvas.data.pacmanImage = canvas.create_image(cx,cy,
      image = canvas.data.pacManAnimation[4])

def redrawAll(canvas):
  if canvas.data.i == 7:
      canvas.delete(ALL)
      canvas.data.ghost1.drawGhost(canvas)
      canvas.data.ghost2.drawGhost(canvas)
      canvas.data.ghost3.drawGhost(canvas)  
      drawPacMan(canvas)  
      drawBoard(canvas)
  else:
    canvas.delete(canvas.data.pacmanImage)
    canvas.data.ghost1.deleteTmp(canvas)
    canvas.data.ghost2.deleteTmp(canvas)
    canvas.data.ghost3.deleteTmp(canvas)
    canvas.data.ghost1.drawGhost(canvas)
    canvas.data.ghost2.drawGhost(canvas)
    canvas.data.ghost3.drawGhost(canvas)
    drawPacMan(canvas)

def timerFired(canvas):
  if not canvas.data.gameOver:
      redrawAll(canvas)
      if canvas.data.i == 7:
        board = canvas.data.board
        (rows,cols) = (len(board),len(board[0]))
        alreadyMoved = False
        if not canvas.data.wantedPacManVelocity == canvas.data.pacManVelocity:
          (drow,dcol) = canvas.data.wantedPacManVelocity
          (newRow,newCol) = (canvas.data.pacManPos[0] + drow,
            canvas.data.pacManPos[1] + dcol)
          canvas.data.pacmanoldPos = canvas.data.pacManPos
          if isLegalMove(newRow % rows,newCol % cols,canvas):
            canvas.data.pacManPos = (newRow % rows,newCol % cols)
            canvas.data.pacManVelocity = canvas.data.wantedPacManVelocity
            alreadyMoved = True
        (drow,dcol) = canvas.data.pacManVelocity
        (newRow,newCol) = (canvas.data.pacManPos[0] + drow,
          canvas.data.pacManPos[1] + dcol)
        if not alreadyMoved:
          canvas.data.pacmanoldPos = canvas.data.pacManPos
        if (isLegalMove(newRow % rows,newCol % cols,canvas) 
                                      and not alreadyMoved):
          canvas.data.pacManPos = (newRow % rows,newCol % cols)
        checkMove(canvas)
        canvas.data.ghost1.moveGhost(canvas)
        checkMove(canvas)
        canvas.data.ghost2.moveGhost(canvas)
        checkMove(canvas)
        canvas.data.ghost3.moveGhost(canvas,canvas.data.ghost1)
        checkMove(canvas)
        canvas.data.i = 0
        canvas.data.moveCount += 1
        if canvas.data.moveCount == 30:
          canvas.data.moveCount = 0
      delay = 30 # milliseconds
      canvas.data.i += 1
      canvas.after(delay, timerFired, canvas) 

def goToHomeScreen(canvas):
  canvas.data.mode = 0
  canvas.data.selectedTile = 0 #default
  canvas.config(width = 960,height = 540)
  redrawHomeScreen(canvas)

def redrawHomeScreen(canvas):
  canvas.width = canvas.winfo_reqwidth()-4
  canvas.height = canvas.winfo_reqheight()-4
  background = canvas.data.homescreenimages[0]
  canvas.create_image(canvas.width/2,canvas.height/2,image = background)
  yOffset = canvas.height / 6
  xOffset = canvas.width / 8
  width = canvas.width/4
  height = canvas.height/6
  for i in xrange(4): #make the 4 buttons
    canvas.create_rectangle(xOffset,yOffset*(i+1),xOffset+width,
      yOffset*(i+1)+height,fill = "yellow")
    if i == 0: #play game option
      canvas.create_text(xOffset + width/2,yOffset*(i+1)+height/2,
        text = "Play Game",font = ("MS Serif", 18, "bold italic"))
    elif i == 1: #play custom level
      canvas.create_text(xOffset + width/2,yOffset*(i+1)+height/2,
        text = "Play Custom Level",font = ("MS Serif", 18, "bold italic"))
    elif i == 2: #create custom level
      canvas.create_text(xOffset + width/2,yOffset*(i+1)+height/2,
        text = "Create Custom Level",font = ("MS Serif", 18, "bold italic"))
    elif i == 3: #exit
      canvas.create_text(xOffset + width/2,yOffset*(i+1)+height/2,
        text = "Quit Game",font = ("MS Serif", 18, "bold italic"))
  #draw the selceted tile now
  selectedTileOffset = canvas.width/16
  selectedTileImage = canvas.data.homescreenimages[1]
  canvas.create_image(selectedTileOffset,
    yOffset*(canvas.data.selectedTile+1)+height/2,image = selectedTileImage)


def init(canvas,levelnumber):
    boardinfo = level(levelnumber).boardinfo
    canvas.data.moveCount = 0
    canvas.data.board = boardinfo[0]
    canvas.data.levelnumber = levelnumber
    (rows,cols) = (len(canvas.data.board),len(canvas.data.board[0]))
    cellSize = 16
    sideMargin = 0
    topMargin = 80
    canvasWidth = max(sideMargin*2 + cols*cellSize,sideMargin*2 + 10*cellSize)
    canvasHeight = max(topMargin*2 + rows*cellSize,16*9+topMargin*2) 
    #make sure tiles are displayed with a minimum value
    canvas.config(width = canvasWidth,height = canvasHeight)
    canvas.width = canvas.winfo_reqwidth() - 4
    canvas.height = canvas.winfo_reqheight() - 4
    canvas.data.gameOver = False
    canvas.data.portalPlaced = False
    canvas.data.pacManVelocity = (0,0)
    canvas.data.wantedPacManVelocity = (0,0)
    canvas.data.defaultPacManPos = boardinfo[1]
    canvas.data.pacManPos = boardinfo[1]
    canvas.data.pacmanoldPos = boardinfo[1]
    canvas.data.ghost1 = Ghost(boardinfo[2])
    canvas.data.ghost2 = Ghost(boardinfo[3])
    canvas.data.ghost3 = Ghost(boardinfo[4])
    canvas.data.corners = boardinfo[5]
    canvas.data.moveCount = 0
    canvas.data.lives = 3
    canvas.data.tileImages = loadTileImages()
    canvas.data.pacManAnimation = loadPacManAnimation()
    canvas.data.pacmanImage = canvas.data.pacManAnimation[4]
    canvas.data.livesImage = PhotoImage(file = "extras/life.gif")
    canvas.data.gameOverScreen = PhotoImage(file = "extras/gameoverscreen.gif")
    canvas.data.initialPellets = getInitialPellets(canvas)
    canvas.data.pelletsEaten = 0
    canvas.data.i = 0
    if not canvas.data.timerFiredOn:
      timerFired(canvas)
      canvas.data.timerFiredOn = True
    redrawAll(canvas)

def initLevelEditor(canvas):
  canvas.delete(ALL)
  message = "Welcome to the level editor! Press S to Save"
  title = "Information"
  tkMessageBox.showinfo(title, message)
  message = "Click on a piece, then select its place on the board!\
   Happy editing!"
  title = "Information"
  tkMessageBox.showinfo(title, message)
  canvas.data.tiles = loadTileImages()
  createSidebar(canvas)
  cellSize = 16
  message = "How many rows would you like?"
  title = "Initializing..."
  rows = tkSimpleDialog.askstring(title, message)
  while not rows.isdigit() and int(rows) > 0:
    message = "How many rows would you like? Enter an integer!"
    title = "Initializing..."
    rows = tkSimpleDialog.askstring(title, message)
  rows = int(rows)
  message = "How many columns would you like?"
  title = "Initializing..."
  cols = tkSimpleDialog.askstring(title, message)
  while not cols.isdigit() and int(cols) > 0:
    message = "How many cols would you like? Enter an integer!"
    title = "Initializing..."
    cols = tkSimpleDialog.askstring(title, message)
  cols = int(cols)
  sideMargin = 50
  topMargin = 40
  canvasWidth = max(sideMargin*2 + cols*cellSize,sideMargin*2 + 10*cellSize)
  canvasHeight = max(topMargin*2 + rows*cellSize,16*9+topMargin*2)
  #make sure tiles are displayed
  canvas.config(width = canvasWidth,height = canvasHeight)
  canvas.data.rows = rows
  canvas.data.cols = cols
  canvas.data.canvasWidth = canvasWidth
  canvas.data.canvasHeight = canvasHeight
  canvas.data.board = make2dList(canvas.data.rows,canvas.data.cols)
  for row in xrange(canvas.data.rows):
    for col in xrange(canvas.data.cols):
      canvas.data.board[row][col] = canvas.data.tiles[0]
  canvas.data.currentPiece = canvas.data.tiles[0]
  drawBoardLevelEditor(canvas)
  canvas.create_text(canvas.data.canvasWidth/2,10,text = "Level Editor",
    fill = "red", font = "Times 16 bold")
  canvas.create_text(canvas.data.canvasWidth/2,canvas.data.canvasHeight - 10,
    text = "Current Piece :",fill = "red", font = "Times 16 bold")


def run():
    # create the root and the canvas
    root = Tk()
    root.title("Pacman Presented By: Connell Donaghy")
    root.wm_iconbitmap('extras/pacman.ico')
    canvas = Canvas(root, width=960, height=540, background = "black")
    canvas.pack(fill=BOTH, expand=YES)
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.homescreenimages = loadHomeScreenImages()
    goToHomeScreen(canvas)
    def wrapKeyPressed(event):
      keyPressed(event,canvas)
    root.bind("<KeyPress>", wrapKeyPressed)
    def wrapmousePressed(event):
      mousePressed(event,canvas)
    root.bind("<Button-1>", wrapmousePressed)
    def wrapRightmousePressed(event):
      rightmousePressed(event,canvas)
    root.bind("<Button-3>",wrapRightmousePressed)
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)


run()