import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET
from typing import List, Tuple
from collections import deque


class MazeDAO:
    """DAO pro načítání dat z CSV nebo XML souborů."""

    @staticmethod
    def load_from_csv(file_path: str) -> List[List[int]]:
        """Načte bludiště z CSV souboru."""
        maze = []
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                maze.append([int(cell) for cell in row])
        return maze

    @staticmethod
    def load_from_xml(file_path: str) -> List[List[int]]:
        """Načte bludiště z XML souboru."""
        maze = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        for row in root.findall('row'):
            maze.append([int(cell.text) for cell in row.findall('cell')])
        return maze


class Bludiste:
    def __init__(self, data: List[List[int]]):
        """Inicializuje bludiště."""
        self.bludiste = data
        self.vyska = len(data)
        self.sirka = len(data[0]) if self.vyska > 0 else 0

    def getSirka(self) -> int:
        """Vrátí šířku bludiště."""
        return self.sirka

    def getVyska(self) -> int:
        """Vrátí výšku bludiště."""
        return self.vyska

    def jeVolno(self, pozice: Tuple[int, int]) -> bool:
        """Zjistí, zda je na dané pozici volno (hodnota 0)."""
        x, y = pozice
        return 0 <= x < self.sirka and 0 <= y < self.vyska and self.bludiste[y][x] == 0

    def nejvzdalenejsi_policko(self, start: Tuple[int, int]) -> Tuple[int, int]:
        """Najde nejvzdálenější volné políčko od startu."""
        sirka, vyska = self.getSirka(), self.getVyska()
        queue = deque([(start, 0)])  # (souřadnice, vzdálenost)
        navstiveno = [[False for _ in range(sirka)] for _ in range(vyska)]
        nejvzdalenejsi = start
        max_vzdalenost = 0

        while queue:
            (x, y), vzdalenost = queue.popleft()

            if vzdalenost > max_vzdalenost:
                max_vzdalenost = vzdalenost
                nejvzdalenejsi = (x, y)

            if not navstiveno[y][x]:
                navstiveno[y][x] = True

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < sirka and 0 <= ny < vyska and not navstiveno[ny][nx] and self.jeVolno((nx, ny)):
                        queue.append(((nx, ny), vzdalenost + 1))

        return nejvzdalenejsi

    def najdi_cestu(self, start: Tuple[int, int], cil: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Najde cestu z bodu start do bodu cíl pomocí BFS."""
        queue = deque([(start, [start])])  # (aktuální pozice, cesta k ní)
        navstiveno = [[False for _ in range(self.sirka)] for _ in range(self.vyska)]

        while queue:
            (x, y), cesta = queue.popleft()

            if (x, y) == cil:
                return cesta

            if not navstiveno[y][x]:
                navstiveno[y][x] = True

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.sirka and 0 <= ny < self.vyska and not navstiveno[ny][nx] and self.jeVolno((nx, ny)):
                        queue.append(((nx, ny), cesta + [(nx, ny)]))

        return []  # Pokud není nalezena cesta

class BludisteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bludiste = None
        self.bludisteView = None
        self.player_pos = (0, 0)
        self.cil_pos = None
        self.cesta = []
        self.index_cesty = 0

    def nacti_soubor(self):
        """Zobrazí dialog pro výběr souboru a načte bludiště."""
        file_path = filedialog.askopenfilename(
            title="Vyberte soubor bludiště",
            filetypes=(("CSV soubory", "*.csv"), ("XML soubory", "*.xml"))
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                data = MazeDAO.load_from_csv(file_path)
            elif file_path.endswith('.xml'):
                data = MazeDAO.load_from_xml(file_path)
            else:
                raise ValueError("Nepodporovaný formát souboru!")

            self.bludiste = Bludiste(data)
            self.cil_pos = self.bludiste.nejvzdalenejsi_policko((0, 0))
            self.bludisteView = BludisteView(self.bludiste)
            self.player_pos = (0, 0)
            self.cesta = self.bludiste.najdi_cestu(self.player_pos, self.cil_pos)
            self.index_cesty = 0
            self.vykresli_bludiste()
            self.automaticky_pohyb()
        except Exception as e:
            messagebox.showerror("Chyba", f"Došlo k chybě při načítání souboru:\n{e}")

    def vykresli_bludiste(self):
        """Vykreslí načtené bludiště na canvas."""
        if self.bludiste and self.bludisteView:
            self.canvas.delete("all")
            self.bludisteView.vykresli(self.canvas, self.player_pos, self.cil_pos)
        else:
            messagebox.showwarning("Varování", "Bludiště není načteno!")

    def automaticky_pohyb(self):
        """Přesune hráče automaticky podle předem vypočítané cesty."""
        if self.index_cesty < len(self.cesta):
            self.player_pos = self.cesta[self.index_cesty]
            self.index_cesty += 1
            self.vykresli_bludiste()
            self.root.after(300, self.automaticky_pohyb)  # Pohyb každých 300 ms
        else:
            messagebox.showinfo("Gratulace", "Dosáhli jste cíle!")


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

def main():
    root = tk.Tk()
    root.title("Bludiště v Tkinteru")

    app = BludisteApp(root)

    # Přidání menu
    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Soubor", menu=file_menu)
    file_menu.add_command(label="Načíst bludiště", command=app.nacti_soubor)
    file_menu.add_separator()
    file_menu.add_command(label="Konec", command=root.quit)

    root.geometry("800x600")
    root.mainloop()


if __name__ == "__main__":
    main()
