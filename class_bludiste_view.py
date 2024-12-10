from typing import Tuple
import tkinter as tk
from class_bludiste import Bludiste

class BludisteView:
    def __init__(self, bludiste: Bludiste, rozmerPolicka: int = 40, padding: int = 10):
        self.bludiste = bludiste
        self.rozmerPolicka = rozmerPolicka
        self.padding = padding

    def vykresli(self, canvas: tk.Canvas, player_pos: Tuple[int, int], cil_pos: Tuple[int, int]):
        """Vykreslí bludiště na canvas a označí start, cíl a hráče."""
        for i in range(self.bludiste.getVyska()):
            for j in range(self.bludiste.getSirka()):
                x1 = self.padding + j * self.rozmerPolicka
                y1 = self.padding + i * self.rozmerPolicka
                x2 = x1 + self.rozmerPolicka
                y2 = y1 + self.rozmerPolicka

                # Barva políčka (černá pro zdi, bílá pro volná políčka)
                fill_color = "black" if self.bludiste.bludiste[i][j] == 1 else "white"

                # Pokud je to start (vlevo nahoře), obarvíme zeleně
                if (j, i) == (0, 0):
                    fill_color = "green"

                # Pokud je to cíl, obarvíme žlutě
                if (j, i) == cil_pos:
                    fill_color = "yellow"

                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")

        # Vykreslení hráče
        px, py = player_pos
        px1 = self.padding + px * self.rozmerPolicka + 5
        py1 = self.padding + py * self.rozmerPolicka + 5
        px2 = px1 + self.rozmerPolicka - 10
        py2 = py1 + self.rozmerPolicka - 10
        canvas.create_oval(px1, py1, px2, py2, fill="blue")
