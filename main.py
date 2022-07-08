# Author: Ben Platt
# Last updated: 07/08/2022
#
# This program acts as a visual enhancer to showing what is
# going on when a sorting algorithm runs, using a tkinter GUI
# Inspired by (of many): https://www.youtube.com/watch?v=kPRA0W1kECg&t=116s
# Quicksort code and learning from https://www.youtube.com/watch?v=9KBwdDEwal8
#
# Ideas for future expansion of the program:
# 1). Incorporating sounds like many other visualizations do (i.e. each size has an associated frequency).
# 2). Adding a dropdown bar that allows the user to select from a list of multiple sorting algorithms to use.

from tkinter import *
from tkinter import font
import sizes
import time

# ----------------- Begin Initializations -----------------
# initialize root and window geometry, accessible to the whole program
root = Tk()
root.title("Sorting Visualization - Ben Platt")
root.geometry("900x900")
root.configure(bg="black")

# beginning state
global state
state = "STARTING"
bttnFont = font.Font(size=30, font="Arial")
userInfoStart = Label(root, text="Welcome! Press the start button to begin sorting", font=("Arial", 20), fg="white", bg="black")
startBttn = Button(root, padx=20, pady=20, bg="green", activebackground="#B2E77C", text="START", font=bttnFont, command=lambda: quicksort(rectangles, 0, len(rectangles) - 1))

# Running state
userInfoRunning = Label(root, text="Sorting...", font=("Arial", 20), fg="white", bg="black")

# Canvas for sorting
# to get the border looking right, do height (or width) = desired height - 4
canvas = Canvas(root, width=896, height=496, bg="black")
canvas.place(x=0, y=400)

# Randomly generated rectangle sizes
rectangles = sizes.generateSizes()
# ----------------- End Initializations -----------------


# ----------------- Begin Update Functions -----------------
# Called from the update function to redraw the rectangles
def drawRectangles():
    # coords for rectangle
    # top left
    x0 = 0
    y1 = 800
    # y0 is y1 + size
    # bottom right
    width = 7.17
    # id = C.create_rectangle(x0, y0, x1, y1, option, ...)
    # for coloring the special rectangles
    global pivot
    global ith
    global jth
    if state is "STARTING":
        pivot = None
        ith = None
        jth = None
    # going through the list of rectangle sizes and drawing them accordingly
    for i in rectangles:
        # get parameters
        x1 = x0 + width
        y0 = y1 - i
        # draw all the rectangles
        newRect = canvas.create_rectangle(x0, y0, x1, y1, fill="white", tags="rect")
        # color the special ones in the quicksort function
        if state is not "ENDING":
            if i is pivot and pivot is not None:
                canvas.itemconfig(newRect, fill="red")
            if i is ith and ith is not None:
                canvas.itemconfig(newRect, fill="green")
            if i is jth and jth is not None:
                canvas.itemconfig(newRect, fill="green")
        # after drawing -> next iteration
        x0 = x1


# What the user sees first thing when they run the program
def starting():
    global state
    if state is "STARTING":
        # starting info and button
        userInfoStart.place(x=200, y=200)
        startBttn.place(x=400, y=250)
        drawRectangles()


# What the user see's after the program finishes
def ending():
    endingLabel = Label(root, text="Complete!", font=("Arial", 20), fg="white", bg="black")
    endingLabel.place(x=200, y=200)


# called to check if sorting is complete
def checkSorting(arr):
    length = len(arr)
    for i in range(0, length):
        if i is 0:
            continue
        if arr[i-1] > arr[i]:
            return False
    return True


# updates the gui and slows the algorithm down
def update():
    canvas.delete("rect")
    drawRectangles()
    time.sleep(0.01)
    root.update()
# ----------------- End Update Functions -----------------


# ----------------- Begin Quicksort -----------------
# Quicksort function is called when the start button is pressed (see initializations)
def quicksort(arr, left, right):
    global state
    if state is "STARTING":
        state = "RUNNING"
    if startBttn is not None and userInfoStart is not None:
        startBttn.destroy()
        userInfoStart.destroy()
        userInfoRunning.place(x=200, y=200)
    if left < right:
        partition_pos = partition(arr, left, right)
        quicksort(arr, left, partition_pos - 1)
        quicksort(arr, partition_pos + 1, right)
    if checkSorting(arr):
        update()
        ending()
        state = "ENDING"


def partition(arr, left, right):
    # global variables used for coloring the pivots and the rectangles that are being checked
    global ith
    global jth
    ith = arr[left]
    jth = arr[right-1]
    global pivot
    i = left
    j = right - 1
    pivot = arr[right]
    while i < j:
        while i < right and arr[i] < pivot:
            i += 1
        while j > left and arr[j] >= pivot:
            j -= 1
        if i < j:
            update()
            arr[i], arr[j] = arr[j], arr[i]
    if arr[i] > pivot:
        update()
        arr[i], arr[right] = arr[right], arr[i]
    return i
# ----------------- End Quicksort -----------------


# What is being run in the script (the "loop")
if __name__ == '__main__':
    starting()
    # Ending the loop execution here, after the program has run
    root.mainloop()
