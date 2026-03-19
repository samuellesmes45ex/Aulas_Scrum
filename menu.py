import sqlite3
import tkinter as tk
from consultas import ConsultarReservaApp
from registroReservas import reservar_aula
from modificarReservas import modificar_reserva
from cancelarReservas import cancelar_reserva

BG        = "#0f1117"
BG2       = "#181c27"
ACENTO    = "#4f8ef7"
ACENTO2   = "#3a6fd8"
LINEA     = "#2a3150"
TEXT      = "#e8eaf6"
TEXT2     = "#7986a8"
PELIGRO   = "#e05c6a"
PELIGRO2  = "#c0404e"
SALIR     = "#252d42"
SALIR2    = "#2e3852"

conn = sqlite3.connect("reservas.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aula TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        responsable TEXT NOT NULL,
        descripcion TEXT
    )
""")
conn.commit()
conn.close()


def menu():
    root = tk.Tk()
    root.title("Sistema de Reservas")

    ancho = root.winfo_screenwidth()
    alto  = root.winfo_screenheight()
    w     = int(ancho * 0.90)
    h     = int(alto  * 0.90)
    x     = (ancho - w) // 2
    y     = (alto  - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(False, False)
    root.configure(bg=BG)

    # ENCABEZADO
    header = tk.Frame(root, bg=BG2, height=160)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="Sistema de Reservas",
             font=("Segoe UI", 28, "bold"),
             bg=BG2, fg=TEXT).place(relx=0.5, rely=0.40, anchor="center")

    tk.Label(header, text="Gestion de aulas universitarias",
             font=("Segoe UI", 12),
             bg=BG2, fg=TEXT2).place(relx=0.5, rely=0.72, anchor="center")

    tk.Frame(root, bg=ACENTO, height=2).pack(fill="x")

    # ZONA CENTRAL (expand para ocupar el espacio disponible)
    centro = tk.Frame(root, bg=BG)
    centro.pack(fill="both", expand=True)

    tk.Label(centro, text="Seleccione una opcion",
             font=("Segoe UI", 12),
             bg=BG, fg=TEXT2).pack(pady=(40, 20))

    opciones = [
        ("Reservar aula",     ACENTO,  ACENTO2,  reservar_aula),
        ("Consultar reserva", ACENTO,  ACENTO2,  lambda: consultar_reserva(root)),
        ("Modificar reserva", ACENTO,  ACENTO2,  modificar_reserva),
        ("Cancelar reserva",  PELIGRO, PELIGRO2, cancelar_reserva),
        ("Salir",             SALIR,   SALIR2,   lambda: root.destroy()),
    ]

    for texto, color, hover, comando in opciones:
        btn = tk.Button(
            centro,
            text=texto,
            font=("Segoe UI", 13),
            bg=color, fg=TEXT,
            activebackground=hover,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            width=36,
            height=2,
            command=comando
        )
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e, b=btn, h=hover: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

    # PIE
    pie = tk.Frame(root, bg=BG2, height=48)
    pie.pack(side="bottom", fill="x")
    pie.pack_propagate(False)

    tk.Label(pie, text="© 2025 Gestion de Aulas  |  v1.0",
             font=("Segoe UI", 9),
             bg=BG2, fg=TEXT2).place(relx=0.5, rely=0.5, anchor="center")

    root.mainloop()


def consultar_reserva(ventana_principal):
    ConsultarReservaApp(ventana_principal)

def salir(root):
    root.destroy()

menu()