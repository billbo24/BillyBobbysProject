from dataclasses import dataclass
import time
from tkinter import ttk
import tkinter as tk

@dataclass
class Player:
    name: str
    age: int


class Controller:

    def __init__(self, players: list[Player]) -> None:
        self.players = players

    def set_view(self, view: 'View'):
        self.view = view
        self.view.set_view(self.players, self.test_cmd)

    def test_cmd(self):
        for player in self.players:
            print(player.name, player.age)



class View(ttk.Frame):

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

    def draw(self):
        for idx, player in enumerate(self.players):
            lbl_name = ttk.Label(self, text=player.name)
            lbl_name.grid(row=idx, column=1)

            lbl_age = ttk.Label(self, text=player.age)
            lbl_age.grid(row=idx, column=2)

        self.btn = ttk.Button(self, text='press me')
        self.btn.grid(row=idx + 1, column=0, columnspan=2)


    def set_view(self, players: list[Player], runCmd):
        self.players = players

        self.draw()

        self.btn.configure(command=runCmd)


# app = tk.Tk()

# p = [Player('Billy', 69), Player('Bobby', 420)]
# v = View(app)
# v.pack()
# c = Controller(p)
# c.set_view(v)

# app.mainloop()







def timer(f):

    def inner(*args):

        x = time.time()
        y = f(*args)
        print(y)
        print(time.time() - x)

    return inner


@timer
def test_func(x: int, y: int) -> int:
    return x + y
