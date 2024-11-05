import tkinter as tk
from typing import List, Tuple

class Bludiste:
    def __init__(self, bludiste: List[List[int]]):
        self.bludiste = bludiste

    def jeVolno(self, souradnice: Tuple[int, int]) -> bool:
        """Kontroluje, zda je na souřadnicích volno (0)."""
        x, y = souradnice
        return self.bludiste[y][x] == 0

    def getSirka(self) -> int:
        """Vrací šířku bludiště (počet sloupců)."""
        return len(self.bludiste[0])

    def getVyska(self) -> int:
        """Vrací výšku bludiště (počet řádků)."""
        return len(self.bludiste)

    def getRozmery(self) -> Tuple[int, int]:
        """Vrací rozměry bludiště (šířka, výška)."""
        return self.getSirka(), self.getVyska()

    def jeVychod(self, souradnice: Tuple[int, int]) -> bool:
        """Kontroluje, zda jsou souřadnice na východu bludiště."""
        x, y = souradnice
        return y == len(self.bludiste) - 1 and x == len(self.bludiste[0]) - 3

class BludisteView:
    def __init__(self, bludiste: Bludiste, rozmerPolicka: int = 40, padding: int = 10):
        self.bludiste = bludiste
        self.rozmerPolicka = rozmerPolicka
        self.padding = padding

    def vykresli(self, canvas: tk.Canvas):
        """Vykreslí bludiště na canvas."""
        for i in range(self.bludiste.getVyska()):
            for j in range(self.bludiste.getSirka()):
                x1 = self.padding + j * self.rozmerPolicka
                y1 = self.padding + i * self.rozmerPolicka
                x2 = x1 + self.rozmerPolicka
                y2 = y1 + self.rozmerPolicka
                if self.bludiste.bludiste[i][j] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

class BludisteApp:
    def __init__(self, root: tk.Tk, bludiste: List[List[int]]):
        self.canvas = tk.Canvas(root, width=len(bludiste[0]) * 40 + 20,
                                height=len(bludiste) * 40 + 20)
        self.canvas.pack()
        self.bludiste = Bludiste(bludiste)
        self.bludisteView = BludisteView(self.bludiste)

    def spustit(self):
        """Spustí aplikaci a vykreslí bludiště."""
        self.bludisteView.vykresli(self.canvas)

# Příklad bludiště - 1 je stěna, 0 je cesta
bludiste_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Inicializace hlavního okna Tkinter
root = tk.Tk()
root.title("Bludiště v Tkinteru")

# Inicializace aplikace
app = BludisteApp(root, bludiste_data)

# Spuštění aplikace
app.spustit()

# Spuštění hlavní smyčky Tkinteru
root.mainloop()
