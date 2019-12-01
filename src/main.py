import src.graphics as gl
from src.quicksort import *
import random, time, enum

class STATES(enum.Enum):
    TITLE = 1
    MAIN_MENU = 2
    PLAYING = 3
    RESULT = 4
    EXIT = 5



MAX_HEIGHT = 50
MAX_WIDTH = 20
MAX_DISTANCE = 20 # distance between bars

option = STATES.MAIN_MENU.value
DARK_BLUE = gl.color_rgb(0, 0, 50)


class Bars:
    def __init__(self, _origin, _w, _h, _color, _value):
        self.origin = _origin
        self.w = _w
        self.h = _h
        self.color = _color
        self.value = _value
        self.obj = None
        self.TextVal = None

    def Draw(self, canvas, state=0):
        self.obj = DrawRect(canvas, self.origin, self.w, self.h, self.color, state)
        self.TextVal = PrintMessage(canvas, gl.Point(self.origin.x+10, self.origin.y + 10), self.value, 'white', state)

    def Clear(self):
        self.obj.undraw()
        self.TextVal.undraw()


def ClearLists(num, bars):
    for i in range(len(bars)):
        bars[i].Clear()
    bars.clear()
    num.clear()
    moveset.clear()

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

def PrintMessage(canvas, pos, message, color = "white", state=0):
    text = gl.Text(pos, str(message))
    if state == 0:
        text.setTextColor(color)
    elif state == 1:
        text.setTextColor('red')
    else:
        text.setTextColor('green')
    text.setSize(12)
    text.setFace('courier') # font
    text.draw(canvas)
    return text


def DrawRect(canvas, pos, w, h, color, state=0):
    rect = gl.Rectangle(pos, gl.Point(pos.x + w, pos.y + h))
    rect.setFill(color)
    if state == 0:
        rect.setOutline('white')
    elif state == 1:#pivot color
        rect.setOutline('red')
    else:#borders color
        rect.setOutline('green')

    rect.draw(canvas)
    return rect

def RandInt(min, max):
    return random.randint(min, max)

def RandRBG():
    r = random.randrange(255)
    g = random.randrange(255)
    b = random.randrange(255)
    return gl.color_rgb(r,g,b)

def SetupQuickSort(origin, size, numberList, BarsList):
    for x in range(size):
        n = RandInt(1, 100)
        numberList.append(n)
        bar = Bars(gl.Point(origin.x, origin.y), MAX_WIDTH, -n / MAX_HEIGHT * 100, RandRBG(), n)
        BarsList.append(bar)
        origin.x += MAX_WIDTH + MAX_DISTANCE
        pivotState.append(0) #not pivot

    print("unsorted-->", numberList)
    Quicksort(numberList, 0, len(numberList) - 1)
    print("sorted-->", numberList)

def DrawQuickSort(canvas, Bars):
    for i in range(len(Bars)):  # draw the result first
        Bars[i].Draw(canvas, pivotState[i])

def DrawQuickSortAnimation(canvas, BarsList, size, steps):
    move = 0
    change = True
    while change:
        if move < len(moveset):  # if the still movements to do
            # win.update()
            DrawQuickSort(canvas, BarsList)
            # get the distance
            difX = BarsList[moveset[move]._from].origin.x - BarsList[moveset[move]._to].origin.x
            BarsList[moveset[move]._to].origin.move(difX, 0)
            BarsList[moveset[move]._from].origin.move(-difX, 0)
            time.sleep(steps)
            # switch the list
            BarsList[moveset[move]._to], BarsList[moveset[move]._from] = BarsList[moveset[move]._from], BarsList[
                moveset[move]._to]
            print("move ", BarsList[moveset[move]._from].value, " to ", BarsList[moveset[move]._to].value)
            # clear for next iteration
            for i in range(size):
                BarsList[i].Clear()
            move += 1
        else:
            change = False


def DrawMainMenu(canvas):

    PrintMessage(canvas, gl.Point(200, 100), "Seleccione cantidad de elementos")
    input_box = gl.Entry(gl.Point(400, 100), 4)
    input_box.draw(canvas)
    txt = PrintMessage(canvas, gl.Point(200, 120), "", "red")
    ans = DrawRect(canvas, gl.Point(450, 90), 50, 30, "red")
    op = True
    while op:
        mouse = canvas.getMouse()
        if (ans.getP1().x < mouse.getX() < ans.getP2().x) and (mouse.getY() > ans.getP1().y and mouse.getY() < ans.getP2().y):
            SIZE = int(input_box.getText())
            txt.setText("cantidad escogida: " + str(SIZE))
            print(str(SIZE))
            op = False
            return SIZE # user selected
    return 1#min val


def main():
    win = gl.GraphWin("Quicksort Visualizer", 1080, 720, autoflush=True)
    win.setBackground(DARK_BLUE)
    PrintMessage(win, gl.Point(win.width / 2, 50), "Algoritmo Quicksort")
    # App code starts here
    SIZE = DrawMainMenu(win) #get amount of elements
    origin = gl.Point(50, win.height/2 + 100)
    numberList = [] # holds the number to be sorted
    BarsList = [] # holds all the bars
    # Setup all the rectangles
    SetupQuickSort(origin, SIZE, numberList, BarsList)
    # make animation (switch objects base on moveset)
    DrawQuickSortAnimation(win, BarsList, SIZE, 0.5)
    # # print final result on screen
    print("value (x, y)")
    for i in range(SIZE):
        BarsList[i].Draw(win)
        print(str(BarsList[i].value), "(", str(BarsList[i].origin.x), ", ", str(BarsList[i].origin.y), ")")


    win.getMouse()# Pausa la ventana para ver el resultado
    win.close()  #Cierra el programa

main()
