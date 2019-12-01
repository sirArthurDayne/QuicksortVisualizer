import src.graphics as gl
from src.quicksort import *
import random, time

MAX_HEIGHT = 50
MAX_WIDTH = 20

class Bars:
    def __init__(self, _origin, _w, _h, _color, _value):
        self.origin = _origin
        self.w = _w
        self.h = _h
        self.color = _color
        self.value = _value
        self.obj = None
        self.TextVal = None

    def Draw(self, canvas):
        self.obj = DrawRect(canvas, self.origin, self.w, self.h, self.color)
        self.TextVal = PrintMessage(canvas, gl.Point(self.origin.x+10, self.origin.y + 10), self.value, 'white')

    def Clear(self):
        self.obj.undraw()
        self.TextVal.undraw()

def SierpinskiTriangle(canvas, a, b, c, iter):
    tri = gl.Polygon(a, b, c)
    tri.setFill(gl.color_rgb(int(a.x / canvas.width) * 255 + 10, int(b.x / canvas.width) * 255 + 50, int(c.x / canvas.width) * 255 + 30))
    # nuevos coord
    ab = gl.Point((a.x + b.x) / 2, (a.y + b.y) / 2)
    ac = gl.Point((a.x + c.x) / 2, (a.y + c.y) / 2)
    bc = gl.Point((b.x + c.x) / 2, (b.y + c.y) / 2)

    if iter > 1:#nuevos llamados
        SierpinskiTriangle(canvas, a, ab, ac, iter - 1)
        SierpinskiTriangle(canvas, ab, b, bc, iter - 1)
        SierpinskiTriangle(canvas, ac, bc, c, iter - 1)
    else:
        tri.draw(canvas)

def PrintMessage(canvas, pos, message, color):
    text = gl.Text(pos,str(message))
    text.setTextColor(color)
    text.setSize(12)
    text.setFace('courier') # font
    text.draw(canvas)
    return text

def DrawRect(canvas, pos, w, h, color):
    rect = gl.Rectangle(pos, gl.Point(pos.x + w, pos.y + h))
    rect.setFill(color)
    rect.setOutline('white')
    rect.draw(canvas)
    return rect

def RandInt(min, max):
    return random.randint(min, max)

def clear(win, List):
    for item in List:
        item.Clear()
    win.update()

def main():
    win = gl.GraphWin("Quicksort Visualizer", 1000, 720, autoflush=True)
    DARK_BLUE = gl.color_rgb(0, 0, 50)
    win.setBackground(DARK_BLUE)
    # App code starts here
    origin = gl.Point(50, win.height/2)
    numberList = [] # holds the number to be sorted
    BarsList = [] # holds all the bars

    size = 20 #amount of items to sort
    #Setup all the rectangles
    for x in range(size):
        n = RandInt(1, 100)
        numberList.append(n)
        r = random.randrange(255)
        g = random.randrange(255)
        b = random.randrange(255)
        bar = Bars(gl.Point(origin.x, origin.y), MAX_WIDTH, -n / MAX_HEIGHT * 100, gl.color_rgb(r, g, b), n)
        BarsList.append(bar)
        origin.x += MAX_WIDTH + 10

    print("unsorted-->", numberList)
    Quicksort(numberList, 0, len(numberList) - 1)
    print("sorted-->", numberList)

    #make animation (switch objects base on moveset)
    move = 0
    change = True
    while change:
        if move < len(moveset):# if the still movements to do
            #win.update()
            for i in range(size):#draw the result first
                BarsList[i].Draw(win)
            #get the distance
            difX = BarsList[moveset[move]._from].origin.x - BarsList[moveset[move]._to].origin.x
            BarsList[moveset[move]._to].origin.move(difX, 0)
            BarsList[moveset[move]._from].origin.move(-difX, 0)
            time.sleep(.5)
            #switch the list
            BarsList[moveset[move]._to], BarsList[moveset[move]._from] = BarsList[moveset[move]._from], BarsList[moveset[move]._to]
            print("move ", BarsList[moveset[move]._from].value, " to ", BarsList[moveset[move]._to].value)
            #clear for next iteration
            for i in range(size):
                BarsList[i].Clear()

            move += 1
        else:
            change = False

    #print final result on screen
    print("value (x, y)")
    for i in range(size):
        BarsList[i].Draw(win)
        print(str(BarsList[i].value), "(", str(BarsList[i].origin.x), ", ", str(BarsList[i].origin.y), ")")

    win.getMouse()# Pausa la ventana para ver el resultado
    win.close()  #Cierra el programa

main()
