import sqlite3
import tkinter as tk
from tkinter import messagebox


# ── Paleta (igual que menu.py) ──────────────────────────────────────────────
BG      = "#0f1117"
BG2     = "#181c27"
ACENTO  = "#4f8ef7"
ACENTO2 = "#3a6fd8"
LINEA   = "#2a3150"
TEXT    = "#e8eaf6"
TEXT2   = "#7986a8"


def hora_fin_valida(inicio, fin):
    h_ini, m_ini = int(inicio.split(":")[0]), int(inicio.split(":")[1])
    h_fin, m_fin = int(fin.split(":")[0]),   int(fin.split(":")[1])
    return (h_fin * 60 + m_fin) > (h_ini * 60 + m_ini)


def reservar_aula():

    def guardar():
        Aula        = entry_aula.get().strip()
        Fecha       = entry_fecha.get().strip()
        HoraInicio  = entry_inicio.get().strip()
        HoraFin     = entry_fin.get().strip()
        Responsable = entry_responsable.get().strip()
        Descripcion = entry_descripcion.get().strip()

        # VALIDACIONES DE LAS FECHAS Y HORAS:
        if not Aula:
            messagebox.showerror("Error", "El aula no puede estar vacía.")
            return

        if len(Fecha) != 10 or Fecha[2] != "/" or Fecha[5] != "/":
            messagebox.showerror("Error", "Fecha incorrecta. Use DD/MM/AAAA (ej: 15/02/2026)")
            return

        partes = Fecha.split("/")
        if not partes[0].isdigit() or not partes[1].isdigit() or not partes[2].isdigit():
            messagebox.showerror("Error", "Día, mes y año deben ser números.")
            return
        partes = Fecha.split("/")

        dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])

        if dia == 0:
            messagebox.showerror("Error", "El día no puede ser 00.")
            return
        if mes == 0:
            messagebox.showerror("Error", "El mes no puede ser 00.")
            return
        if anio == 0:
            messagebox.showerror("Error", "El año no puede ser 0000.")
            return
        if dia > 31:
            messagebox.showerror("Error", "El día no puede ser mayor a 31.")
            return
        if mes > 12:
            messagebox.showerror("Error", "El mes no puede ser mayor a 12.")
            return
     

        if len(HoraInicio) != 5 or HoraInicio[2] != ":":
            messagebox.showerror("Error", "Hora de inicio incorrecta. Use HH:MM (ej: 08:00)")
            return

        i = HoraInicio.split(":")
        if not i[0].isdigit() or not i[1].isdigit():
            messagebox.showerror("Error", "La hora de inicio debe contener solo dígitos.")
            return
        
        if int(i[0]) > 23:
            messagebox.showerror("Error", "La hora de inicio no puede ser mayor a 23.")
            return
        if int(i[1]) > 59:
            messagebox.showerror("Error", "Los minutos de inicio no pueden ser mayores a 59.")
            return

        if len(HoraFin) != 5 or HoraFin[2] != ":":
            messagebox.showerror("Error", "Hora de fin incorrecta. Use HH:MM (ej: 10:00)")
            return

        f = HoraFin.split(":")
        if not f[0].isdigit() or not f[1].isdigit():
            messagebox.showerror("Error", "La hora de fin debe contener solo dígitos.")
            return

        if int(f[0]) > 23:
            messagebox.showerror("Error", "La hora de fin no puede ser mayor a 23.")
            return
        if int(f[1]) > 59:
            messagebox.showerror("Error", "Los minutos de fin no pueden ser mayores a 59.")
            return

        if not hora_fin_valida(HoraInicio, HoraFin):
            messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio.")
            return

        if not Responsable or Responsable.isdigit():
            messagebox.showerror("Error", "Ingrese el nombre del responsable.")
            return

        # --- [VALIDACIÓN DE DISPONIBILIDAD] ---
        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()

        query_check = """
            SELECT * FROM reservas 
            WHERE aula = ? 
            AND fecha = ? 
            AND (? < hora_fin AND ? > hora_inicio)
        """
        cursor.execute(query_check, (Aula, Fecha, HoraInicio, HoraFin))
        conflicto = cursor.fetchone()

        if conflicto:
            messagebox.showerror(
                "Conflicto de Horario",
                f"El aula {Aula} ya se encuentra reservada para el {Fecha} "
                f"entre las {conflicto[3]} y {conflicto[4]}."
            )
            conn.close()
            return

        # GUARDAR EN LA BASE DE RESERVAS.DB
        cursor.execute("""
            INSERT INTO reservas (aula, fecha, hora_inicio, hora_fin, responsable, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (Aula, Fecha, HoraInicio, HoraFin, Responsable, Descripcion))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "¡Reserva registrada exitosamente!")
        ventana.destroy()

    # ── Ventana principal ────────────────────────────────────────────────────
    ventana = tk.Toplevel()
    ventana.title("Registrar Reserva")
    ventana.geometry("460x620")
    ventana.resizable(False, False)
    ventana.configure(bg=BG)

    # ── Encabezado ───────────────────────────────────────────────────────────
    header = tk.Frame(ventana, bg=BG2, height=110)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Registrar Reserva",
        font=("Segoe UI", 20, "bold"),
        bg=BG2, fg=TEXT
    ).place(relx=0.5, rely=0.42, anchor="center")

    tk.Label(
        header,
        text="Complete los datos del aula a reservar",
        font=("Segoe UI", 10),
        bg=BG2, fg=TEXT2
    ).place(relx=0.5, rely=0.75, anchor="center")

    # Línea de acento (igual que en el menú)
    tk.Frame(ventana, bg=ACENTO, height=2).pack(fill="x")

    # ── Zona de campos ───────────────────────────────────────────────────────
    centro = tk.Frame(ventana, bg=BG)
    centro.pack(fill="both", expand=True)

    campos = [
        ("Aula",                   "entry_aula"),
        ("Fecha  (DD/MM/AAAA)",    "entry_fecha"),
        ("Hora de inicio  (HH:MM)","entry_inicio"),
        ("Hora de fin  (HH:MM)",   "entry_fin"),
        ("Responsable",            "entry_responsable"),
        ("Descripción  (opcional)", "entry_descripcion"),
    ]

    entries = {}
    for label_text, key in campos:
        # Etiqueta
        tk.Label(
            centro,
            text=label_text,
            font=("Segoe UI", 9),
            bg=BG, fg=TEXT2,
            anchor="w"
        ).pack(fill="x", padx=40, pady=(12, 2))

        # Campo de texto con estilo oscuro
        entry = tk.Entry(
            centro,
            font=("Segoe UI", 11),
            bg=BG2, fg=TEXT,
            insertbackground=TEXT,          # cursor de texto visible
            relief="flat",
            highlightthickness=1,
            highlightbackground=LINEA,
            highlightcolor=ACENTO
        )
        entry.pack(fill="x", padx=40, ipady=6)
        entries[key] = entry

    entry_aula        = entries["entry_aula"]
    entry_fecha       = entries["entry_fecha"]
    entry_inicio      = entries["entry_inicio"]
    entry_fin         = entries["entry_fin"]
    entry_responsable = entries["entry_responsable"]
    entry_descripcion = entries["entry_descripcion"]

    # ── Botón Guardar ────────────────────────────────────────────────────────
    btn = tk.Button(
        centro,
        text="Guardar Reserva",
        font=("Segoe UI", 13),
        bg=ACENTO, fg=TEXT,
        activebackground=ACENTO2,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        width=28,
        height=2,
        command=guardar
    )
    btn.pack(pady=24)
    btn.bind("<Enter>", lambda e: btn.configure(bg=ACENTO2))
    btn.bind("<Leave>", lambda e: btn.configure(bg=ACENTO))

    # ── Pie ──────────────────────────────────────────────────────────────────
    pie = tk.Frame(ventana, bg=BG2, height=36)
    pie.pack(side="bottom", fill="x")
    pie.pack_propagate(False)

    tk.Label(
        pie,
        text="© 2025 Gestión de Aulas  |  v1.0",
        font=("Segoe UI", 8),
        bg=BG2, fg=TEXT2
    ).place(relx=0.5, rely=0.5, anchor="center")

    ventana.mainloop()