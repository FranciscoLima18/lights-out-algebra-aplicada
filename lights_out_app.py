"""Interfaz gráfica de Lights Out basada en Tkinter.

Ejecutar con:
    python3 lights_out_app.py
"""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import messagebox, ttk

from lights_out import solve_lights_out


class LightsOutApp:
    """Aplicación interactiva para crear y resolver tableros Lights Out."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Lights Out — Álgebra Aplicada")
        self.root.resizable(False, False)
        self.size = tk.IntVar(value=3)
        self.board: list[list[int]] = []
        self.buttons: list[list[tk.Button]] = []

        controls = ttk.Frame(root, padding=10)
        controls.grid(row=0, column=0, sticky="ew")
        ttk.Label(controls, text="Tamaño:").grid(row=0, column=0, padx=(0, 5))
        ttk.Combobox(
            controls,
            textvariable=self.size,
            values=(3, 4, 5, 6, 7),
            state="readonly",
            width=5,
        ).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(controls, text="Nuevo tablero", command=self.new_board).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(controls, text="Resolver", command=self.solve).grid(
            row=0, column=3, padx=5
        )

        self.grid_frame = ttk.Frame(root, padding=(10, 0, 10, 10))
        self.grid_frame.grid(row=1, column=0)
        self.status = ttk.Label(root, text="", padding=(10, 0, 10, 10))
        self.status.grid(row=2, column=0)
        self.new_board()

    def new_board(self) -> None:
        size = self.size.get()
        self.board = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
        self.build_grid()
        self.update_status("Presiona las luces para apagarlas.")

    def build_grid(self) -> None:
        for child in self.grid_frame.winfo_children():
            child.destroy()
        self.buttons = []
        for row in range(len(self.board)):
            button_row = []
            for column in range(len(self.board)):
                button = tk.Button(
                    self.grid_frame,
                    width=4,
                    height=2,
                    command=lambda r=row, c=column: self.press(r, c),
                )
                button.grid(row=row, column=column, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)
        self.refresh_grid()

    def refresh_grid(self) -> None:
        for row, values in enumerate(self.board):
            for column, value in enumerate(values):
                self.buttons[row][column].configure(
                    bg="#facc15" if value else "#303047",
                    activebackground="#fde047" if value else "#454560",
                )

    def press(self, row: int, column: int) -> None:
        size = len(self.board)
        for neighbor_row, neighbor_column in (
            (row, column),
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= neighbor_row < size and 0 <= neighbor_column < size:
                self.board[neighbor_row][neighbor_column] ^= 1
        self.refresh_grid()
        if not any(any(row_values) for row_values in self.board):
            self.update_status("¡Tablero resuelto!")
        else:
            self.update_status("Continúa jugando o pulsa «Resolver».")

    def solve(self) -> None:
        try:
            presses = solve_lights_out(self.board)
        except ValueError as error:
            messagebox.showerror("Sin solución", str(error))
            return
        for index, press in enumerate(presses):
            if press:
                self.press(*divmod(index, len(self.board)))
        self.update_status("Solución aplicada.")

    def update_status(self, text: str) -> None:
        self.status.configure(text=text)


def main() -> None:
    root = tk.Tk()
    LightsOutApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
