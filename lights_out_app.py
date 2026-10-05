"""Interfaz moderna de Lights Out con tkinter y numpy.

Ejecutar con:

    python3 lights_out_app.py
"""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np

from lights_out import solve_lights_out


class LightsOutGame:
    """Presentación y control de una partida de Lights Out."""

    COLORS = {
        "background": "#12121b",
        "panel": "#1e1e2e",
        "panel_light": "#292940",
        "border": "#363650",
        "text": "#f4f4f5",
        "muted": "#a4a4b5",
        "accent": "#a78bfa",
        "accent_hover": "#bda8ff",
        "on": "#facc15",
        "on_hover": "#fde047",
        "off": "#303047",
        "off_hover": "#454560",
        "hint": "#34d399",
        "hint_hover": "#6ee7b7",
        "danger": "#fb7185",
    }
    SIZES = ("3", "4", "5", "6", "7")

    def __init__(self, root: tk.Tk, initial_size: int = 5) -> None:
        self.root = root
        self.root.title("LIGHTS OUT  /  ÁLGEBRA LINEAL")
        self.root.configure(bg=self.COLORS["background"])
        self.root.minsize(760, 560)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self.size = initial_size
        self.board = np.zeros((self.size, self.size), dtype=np.uint8)
        self.initial_board = self.board.copy()
        self.buttons: list[list[tk.Button]] = []
        self.solution: np.ndarray | None = None
        self.moves = 0
        self.started_at = time.monotonic()
        self.elapsed_before_pause = 0.0
        self.timer_running = True
        self.board_frame: tk.Frame | None = None

        self._configure_styles()
        self._build_layout()
        self._new_random_board()
        self._tick()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Modern.TCombobox",
            fieldbackground=self.COLORS["panel_light"],
            background=self.COLORS["panel_light"],
            foreground=self.COLORS["text"],
            bordercolor=self.COLORS["border"],
            arrowcolor=self.COLORS["accent"],
            padding=7,
        )

    def _build_layout(self) -> None:
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(
            self.root,
            bg=self.COLORS["panel"],
            width=245,
            padx=22,
            pady=24,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.content = tk.Frame(self.root, bg=self.COLORS["background"], padx=32, pady=28)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content()

    def _label(
        self,
        parent: tk.Widget,
        text: str,
        *,
        size: int = 10,
        color: str | None = None,
        weight: str = "normal",
    ) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color or self.COLORS["text"],
            font=("Segoe UI", size, weight),
        )

    def _build_sidebar(self) -> None:
        self._label(
            self.sidebar,
            "LIGHTS OUT",
            size=20,
            color=self.COLORS["accent"],
            weight="bold",
        ).pack(anchor="w")
        self._label(
            self.sidebar,
            "ÁLGEBRA LINEAL",
            size=9,
            color=self.COLORS["muted"],
            weight="bold",
        ).pack(anchor="w", pady=(0, 34))

        self._label(
            self.sidebar,
            "CONFIGURACIÓN",
            size=9,
            color=self.COLORS["muted"],
            weight="bold",
        ).pack(anchor="w", pady=(0, 8))
        self.size_var = tk.StringVar(value=str(self.size))
        self.size_selector = ttk.Combobox(
            self.sidebar,
            textvariable=self.size_var,
            values=self.SIZES,
            state="readonly",
            width=10,
            style="Modern.TCombobox",
        )
        self.size_selector.pack(fill="x", pady=(0, 24))
        self.size_selector.bind("<<ComboboxSelected>>", self._change_size)

        self._button(self.sidebar, "✦  NUEVO JUEGO", self.generate_random_board, "accent").pack(
            fill="x", pady=4
        )
        self._button(self.sidebar, "↺  REINICIAR", self.reset_game, "secondary").pack(
            fill="x", pady=4
        )
        self._button(
            self.sidebar,
            "⌁  RESOLVER / PISTA",
            self.show_solution,
            "secondary",
        ).pack(fill="x", pady=4)

        self._label(
            self.sidebar,
            "CONTROLES",
            size=9,
            color=self.COLORS["muted"],
            weight="bold",
        ).pack(anchor="w", pady=(34, 8))
        self._label(
            self.sidebar,
            "Pulsa una celda para conmutarla junto a sus vecinos.\n\n"
            "La pista marca las pulsaciones sugeridas sin cambiar el tablero.",
            size=10,
            color=self.COLORS["muted"],
        ).pack(anchor="w")

    def _button(
        self,
        parent: tk.Widget,
        text: str,
        command: object,
        kind: str,
    ) -> tk.Button:
        accent = kind == "accent"
        normal = self.COLORS["accent"] if accent else self.COLORS["panel_light"]
        hover = self.COLORS["accent_hover"] if accent else self.COLORS["border"]
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=normal,
            fg="#191925" if accent else self.COLORS["text"],
            activebackground=hover,
            activeforeground="#191925" if accent else self.COLORS["text"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
        )
        button.bind("<Enter>", lambda _event: button.configure(bg=hover))
        button.bind("<Leave>", lambda _event: button.configure(bg=normal))
        return button

    def _build_content(self) -> None:
        header = tk.Frame(self.content, bg=self.COLORS["background"])
        header.grid(row=0, column=0, sticky="ew", pady=(0, 22))
        header.grid_columnconfigure(0, weight=1)
        self._label(
            header,
            "APAGA TODAS LAS LUCES",
            size=23,
            weight="bold",
        ).grid(row=0, column=0, sticky="w")
        self.status_label = self._label(
            header,
            "Resuelve el tablero con el menor número de movimientos.",
            size=10,
            color=self.COLORS["muted"],
        )
        self.status_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

        metrics = tk.Frame(header, bg=self.COLORS["background"])
        metrics.grid(row=0, column=1, rowspan=2, sticky="e")
        self.moves_label = self._metric(metrics, "JUGADAS", "0")
        self.moves_label.grid(row=0, column=0, padx=(0, 22))
        self.timer_label = self._metric(metrics, "TIEMPO", "00:00")
        self.timer_label.grid(row=0, column=1)

        self.board_card = tk.Frame(
            self.content,
            bg=self.COLORS["panel"],
            highlightbackground=self.COLORS["border"],
            highlightthickness=1,
            padx=28,
            pady=28,
        )
        self.board_card.grid(row=1, column=0, sticky="nsew")
        self.board_card.grid_rowconfigure(0, weight=1)
        self.board_card.grid_columnconfigure(0, weight=1)

    def _metric(self, parent: tk.Widget, title: str, value: str) -> tk.Frame:
        frame = tk.Frame(parent, bg=self.COLORS["background"])
        tk.Label(
            frame,
            text=title,
            bg=self.COLORS["background"],
            fg=self.COLORS["muted"],
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="e")
        label = tk.Label(
            frame,
            text=value,
            bg=self.COLORS["background"],
            fg=self.COLORS["text"],
            font=("Consolas", 17, "bold"),
        )
        label.pack(anchor="e")
        return frame

    def _build_board(self) -> None:
        if self.board_frame is not None:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self.board_card, bg=self.COLORS["panel"])
        self.board_frame.grid(row=0, column=0)
        self.buttons = []

        for row in range(self.size):
            button_row = []
            for column in range(self.size):
                button = tk.Button(
                    self.board_frame,
                    command=lambda r=row, c=column: self.press_cell(r, c),
                    width=4 if self.size <= 5 else 3,
                    height=2 if self.size <= 5 else 1,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    font=("Segoe UI", 16, "bold"),
                )
                button.grid(row=row, column=column, padx=5, pady=5)
                button.bind("<Enter>", lambda event, r=row, c=column: self._hover_cell(r, c, True))
                button.bind("<Leave>", lambda event, r=row, c=column: self._hover_cell(r, c, False))
                button_row.append(button)
            self.buttons.append(button_row)
        self._refresh_buttons()

    def _change_size(self, _event: tk.Event) -> None:
        self.size = int(self.size_var.get())
        self._new_random_board()

    def _new_random_board(self) -> None:
        self.board = np.zeros((self.size, self.size), dtype=np.uint8)
        random_presses = np.random.randint(0, 2, size=(self.size, self.size))
        for row, column in zip(*np.nonzero(random_presses)):
            self._toggle_neighbors(int(row), int(column))
        self.initial_board = self.board.copy()
        self.moves = 0
        self.solution = None
        self._restart_timer()
        self._build_board()
        self._update_status()

    def generate_random_board(self) -> None:
        """Inicia una partida nueva con una configuración resoluble."""
        self._new_random_board()

    def reset_game(self) -> None:
        """Restaura el tablero inicial sin cambiar la configuración."""
        self.board = self.initial_board.copy()
        self.moves = 0
        self.solution = None
        self._restart_timer()
        self._refresh_buttons()
        self._update_status("Tablero reiniciado. ¡Intenta superar tu marca!")

    def _toggle_neighbors(self, row: int, column: int) -> None:
        for neighbor_row, neighbor_column in (
            (row, column),
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if 0 <= neighbor_row < self.size and 0 <= neighbor_column < self.size:
                self.board[neighbor_row, neighbor_column] ^= 1

    def press_cell(self, row: int, column: int) -> None:
        self._toggle_neighbors(row, column)
        self.moves += 1
        self.solution = None
        self._refresh_buttons()
        self._update_status()
        if not np.any(self.board):
            self._win_modal()

    def show_solution(self) -> None:
        """Calcula una pista sin modificar el estado actual del tablero."""
        try:
            solution = solve_lights_out(self.board.tolist())
        except ValueError as error:
            messagebox.showerror("Tablero no resoluble", str(error), parent=self.root)
            return
        self.solution = np.array(solution, dtype=np.uint8).reshape(self.size, self.size)
        self._refresh_buttons()
        self._update_status("Las celdas verdes forman una solución. El tablero no ha cambiado.")

    def _refresh_buttons(self) -> None:
        for row in range(self.size):
            for column in range(self.size):
                button = self.buttons[row][column]
                is_on = bool(self.board[row, column])
                is_hint = self.solution is not None and bool(self.solution[row, column])
                self._set_cell_colors(button, is_on, is_hint, False)

    def _set_cell_colors(
        self,
        button: tk.Button,
        is_on: bool,
        is_hint: bool,
        hovered: bool,
    ) -> None:
        if is_hint:
            normal = self.COLORS["hint_hover"] if hovered else self.COLORS["hint"]
        elif is_on:
            normal = self.COLORS["on_hover"] if hovered else self.COLORS["on"]
        else:
            normal = self.COLORS["off_hover"] if hovered else self.COLORS["off"]
        button.configure(
            bg=normal,
            activebackground=normal,
            fg="#171722" if is_on or is_hint else self.COLORS["text"],
            text="●" if is_on else "✦" if is_hint else "",
        )

    def _hover_cell(self, row: int, column: int, hovered: bool) -> None:
        button = self.buttons[row][column]
        self._set_cell_colors(
            button,
            bool(self.board[row, column]),
            self.solution is not None and bool(self.solution[row, column]),
            hovered,
        )

    def _update_status(self, message: str | None = None) -> None:
        self.moves_label.winfo_children()[1].configure(text=f"{self.moves:02d}")
        if message:
            self.status_label.configure(text=message)
        elif not np.any(self.board):
            self.status_label.configure(text="¡Tablero apagado! Has ganado.")
        else:
            self.status_label.configure(text="Cada movimiento conmuta la celda y sus vecinos.")

    def _restart_timer(self) -> None:
        self.started_at = time.monotonic()
        self.elapsed_before_pause = 0.0
        self.timer_running = True

    def _tick(self) -> None:
        elapsed = int(self.elapsed_before_pause + time.monotonic() - self.started_at)
        minutes, seconds = divmod(elapsed, 60)
        self.timer_label.winfo_children()[1].configure(text=f"{minutes:02d}:{seconds:02d}")
        self.root.after(500, self._tick)

    def _win_modal(self) -> None:
        modal = tk.Toplevel(self.root)
        modal.title("¡Victoria!")
        modal.configure(bg=self.COLORS["panel"])
        modal.resizable(False, False)
        modal.transient(self.root)
        modal.grab_set()
        tk.Label(
            modal,
            text="✦  ¡TABLERO APAGADO!  ✦",
            bg=self.COLORS["panel"],
            fg=self.COLORS["hint"],
            font=("Segoe UI", 18, "bold"),
            padx=34,
            pady=25,
        ).pack()
        tk.Label(
            modal,
            text=f"Completaste el tablero en {self.moves} jugadas.",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Segoe UI", 11),
        ).pack(pady=(0, 20))
        self._button(modal, "CONTINUAR", modal.destroy, "accent").pack(
            padx=34, pady=(0, 25), fill="x"
        )

    def _close(self) -> None:
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    LightsOutGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()


