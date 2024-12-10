
import tkinter as tk
from tkinter import filedialog, messagebox
from class_mazedao import MazeDAO
from class_bludiste import Bludiste
from class_bludiste_view import BludisteView

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
