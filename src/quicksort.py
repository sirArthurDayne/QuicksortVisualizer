#Esta clase guarda los movimientos que genere el arreglo
#f representa DESDE
#t representa HASTA
class move:
    def __init__(self, f, t):
        self._from = f
        self._to = t
#ARREGLOS QUE GUARDAN LOS MOVIMIENTOS Y ESTADOS
moveset = []
pivotState = []

#funcion auxiliar de quicksort, esta funcion nos devuelve el pivote
def getPivot(list, low, hi):
    mid = (hi + low) // 2
    pivot = hi
    if list[low] < list[mid]:
        if list[mid] < list[hi]:
            pivot = mid
    elif list[low] < list[hi]:
        pivot = low
    return pivot

#Funcion auxiliar de Quicksort, hace las comparaciones con los pivotes y sus vecinos
def Divide(list, low, hi):
    pivotIndex = getPivot(list, low, hi)
    pivotVal = list[pivotIndex]
    pivotState[pivotIndex] = 1# set pivot index

    #guarda el movimiento en el arreglo
    moveset.append(move(pivotIndex, low))
    #switch pivot to left most side of list
    list[pivotIndex], list[low] = list[low], list[pivotIndex]
    border = low

    for i in range(low, hi+1):
        if list[i] < pivotVal:
            pivotState[border] = 2
            border += 1
            # guarda el movimiento en el arreglo
            moveset.append(move(i, border))
            list[i], list[border] = list[border], list[i]
            pivotState[border] = 0

    # guarda el movimiento en el arreglo
    moveset.append(move(low, border))
    list[low], list[border] = list[border], list[low]

    return border



#Funcion Principal del Algoritmo quicksort
def Quicksort(list, start, end):
    pivot = None
    if start < end:
        pivot = Divide(list, start, end)
        pivotState[pivot] = 0

        #lado izquierdo
        Quicksort(list, start, pivot-1)
        #lado derecho
        Quicksort(list, pivot+1, end)

