import tkinter as tk
from tkinter import ttk
import random

ball = {"dirx" : 15, "diry" : -15, "x" : 350, "y" : 300, "w" : 10}

blocks = []
block_size = {"x": 75, "y": 30}

bar = {"x": 0, "w": 100}

class Blockout(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.bind('<Motion>', self.motion)
        self.master.title("Blockout")
        self.is_gameover = False
        self.point = 0
        self.cv = tk.Canvas(self, width=600, height=400)
        self.cv.pack()
        self.message_var = tk.StringVar()
        self.message_var.set('point: 0')
        message_label = ttk.Label(self, textvariable=self.message_var)
        message_label.pack()
        self.create_widgets()

    def create_widgets(self):
        for iy in range(0, 5):
            for ix in range(0, 8):
                color = "white"
                if (iy + ix) % 2 == 1: color = "gray"
                x1 = ix * block_size["x"]
                x2 = x1 + block_size["x"]
                y1 = iy * block_size["y"]
                y2 = y1 + block_size["y"]
                blocks.append([x1, y1, x2, y2, color])
        self.game_loop()

    def draw_objects(self):
        self.cv.delete('all')
        self.cv.create_rectangle(0, 0, 600, 400, fill="black", width=0)
        for w in blocks:
            x1, y1, x2, y2, c = w
            self.cv.create_rectangle(x1, y1, x2, y2, fill=c, width=0)
        self.cv.create_oval(
            ball["x"]-ball["w"],
            ball["y"]-ball["w"],
            ball["x"]+ball["w"],
            ball["y"]+ball["w"],
            fill="red"
        )
        self.cv.create_rectangle(bar["x"], 390, bar["x"] + bar["w"], 400, fill="yellow")

    def move_ball(self):
        if self.is_gameover:
            self.message_var.set("--GAMEOVER-- point: " + str(self.point))
            return
        bx = ball["x"] + ball["dirx"]
        by = ball["y"] + ball["diry"]
        if bx < 0 or bx > 600:
            ball["dirx"] *= -1
        if by < 0 :
            ball["diry"] *= -1
        if by > 390 and (bar["x"] <= bx <= (bar["x"] + bar["w"])):
            ball["diry"] *= -1
            if bar["x"] <= bx < (bar["x"] + bar["w"]//2):
                ball["dirx"] = -15
            elif (bar["x"] + bar["w"]//2) == bx:
                ball["dirx"] = 0
            elif (bar["x"] + bar["w"]//2) < bx <= (bar["x"] + bar["w"]):
                ball["dirx"] = 15
            by = 380
        hit_i = -1
        for i, w in enumerate(blocks):
            x1, y1, x2, y2, color = w
            w3 = ball["w"] / 3
            if (x1-w3 <= bx <= x2+w3) and (y1-w3 <= by <= y2+w3):
                hit_i = i
                break
        if hit_i >= 0:
            del blocks[hit_i]
            if random.randint(0, 1) == 0: ball["dirx"] *= -1
            ball["diry"] *= -1
            self.point += 10
            if len(blocks) == 0:
                self.message_var.set("--GAMECLEAR-- point: " + str(self.point))
                return
            self.message_var.set("point: "+str(self.point))
        if by > 400:
            self.is_gameover = True
        if 0 <= bx <= 600: 
            ball["x"] = bx
        if 0 <= by <= 400: 
            ball["y"] = by

    def game_loop(self):
        self.draw_objects()
        self.move_ball()
        self.after(50, self.game_loop)

    def motion(self, e):
        bar["x"] = e.x

def main():
    root = Blockout()
    root.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
