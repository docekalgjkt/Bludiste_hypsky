

import csv
import xml.etree.ElementTree as ET
from typing import List


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

