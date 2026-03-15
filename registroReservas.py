import sqlite3
import tkinter as tk
from tkinter import messagebox


def hora_fin_valida(inicio, fin):
    h_ini, m_ini = int(inicio.split(":")[0]), int(inicio.split(":")[1])
    h_fin, m_fin = int(fin.split(":")[0]),   int(fin.split(":")[1])
    return (h_fin * 60 + m_fin) > (h_ini * 60 + m_ini)


def reservar_aula():

    def guardar():
        Aula       = entry_aula.get().strip()
        Fecha      = entry_fecha.get().strip()
        HoraInicio = entry_inicio.get().strip()
        HoraFin    = entry_fin.get().strip()
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

        if len(HoraInicio) != 5 or HoraInicio[2] != ":":
            messagebox.showerror("Error", "Hora de inicio incorrecta. Use HH:MM (ej: 08:00)")
            return

        p = HoraInicio.split(":")
        if not p[0].isdigit() or not p[1].isdigit():
            messagebox.showerror("Error", "La hora de inicio debe contener solo dígitos.")
            return

        if len(HoraFin) != 5 or HoraFin[2] != ":":
            messagebox.showerror("Error", "Hora de fin incorrecta. Use HH:MM (ej: 10:00)")
            return

        p = HoraFin.split(":")
        if not p[0].isdigit() or not p[1].isdigit():
            messagebox.showerror("Error", "La hora de fin debe contener solo dígitos.")
            return

        if not hora_fin_valida(HoraInicio, HoraFin):
            messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio.")
            return

        if not Responsable or Responsable.isdigit():
            messagebox.showerror("Error", "Ingrese el nombre del responsable.")
            return

        # GUARDAR EN LA BASE DE RESERVAS.DB
        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (aula, fecha, hora_inicio, hora_fin, responsable, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (Aula, Fecha, HoraInicio, HoraFin, Responsable, Descripcion))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "¡Reserva registrada exitosamente!")
        ventana.destroy()

    
    ventana = tk.Toplevel()
    ventana.title("Registrar Reserva")
    ventana.geometry("420x580")
    ventana.resizable(False, False)
    ventana.configure(bg="#e8f4f8")

    # ENCABEZADO
    header = tk.Frame(ventana, bg="#1a7fb5", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(
        header,
        text="Registrar Reserva",
        font=("Georgia", 16, "bold"),
        bg="#1a7fb5", fg="white"
    ).place(relx=0.5, rely=0.5, anchor="center")

    campos = [
        ("Aula:",                    "entry_aula"),
        ("Fecha (DD/MM/AAAA):",      "entry_fecha"),
        ("Hora de inicio (HH:MM):",  "entry_inicio"),
        ("Hora de fin (HH:MM):",     "entry_fin"),
        ("Responsable:",             "entry_responsable"),
        ("Descripción (opcional):",  "entry_descripcion"),
    ]

    entries = {}
    for label_text, key in campos:
        tk.Label(
            ventana,
            text=label_text,
            font=("Helvetica", 10, "bold"),
            bg="#e8f4f8", fg="#1a5f7a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(12, 0))

        entry = tk.Entry(
            ventana,
            font=("Helvetica", 11),
            bg="white", fg="#1a3a4a",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#90c8e0",
            highlightcolor="#1a7fb5"
        )
        entry.pack(fill="x", padx=40, ipady=5)
        entries[key] = entry

    entry_aula        = entries["entry_aula"]
    entry_fecha       = entries["entry_fecha"]
    entry_inicio      = entries["entry_inicio"]
    entry_fin         = entries["entry_fin"]
    entry_responsable = entries["entry_responsable"]
    entry_descripcion = entries["entry_descripcion"]

    # BOTÓN PARA RESERVAR
    btn = tk.Button(
        ventana,
        text="Guardar Reserva",
        font=("Helvetica", 12, "bold"),
        bg="#1a7fb5", fg="white",
        activebackground="#155f8a",
        relief="flat", cursor="hand2",
        command=guardar
    )
    btn.pack(pady=24, ipadx=20, ipady=8)
    btn.bind("<Enter>", lambda e: btn.configure(bg="#155f8a"))
    btn.bind("<Leave>", lambda e: btn.configure(bg="#1a7fb5"))

    ventana.mainloop()


