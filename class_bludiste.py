from collections import deque
from typing import List, Tuple

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
