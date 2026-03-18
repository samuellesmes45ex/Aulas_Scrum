import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def cancelar_reserva():

    def buscar():
        id_texto = entry_id.get().strip()

        if not id_texto.isdigit():
            messagebox.showwarning("Atención", "Ingrese un ID numérico válido.")
            return

        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (int(id_texto),))
        reserva = cursor.fetchone()
        conn.close()

        if not reserva:
            limpiar_datos()
            messagebox.showerror("Error", f"No se encontró ninguna reserva con ID {id_texto}.")
            return

        datos = {
            "aula":        reserva[1],
            "fecha":       reserva[2],
            "hora_inicio": reserva[3],
            "hora_fin":    reserva[4],
            "responsable": reserva[5],
            "descripcion": reserva[6] or "—",
        }
        for key, valor in datos.items():
            detalles[key].config(text=str(valor))

        btn_cancelar.configure(state="normal")
        lbl_estado.configure(
            text=f"✔  Reserva #{id_texto} encontrada. Confirme la cancelación.",
            fg="#f0a04c"
        )

    def confirmar_cancelacion():
        id_texto = entry_id.get().strip()

        respuesta = messagebox.askyesno(
            "Confirmar cancelación",
            f"¿Está seguro de que desea cancelar la reserva #{id_texto}?\n"
            "Esta acción no se puede deshacer."
        )

        if not respuesta:
            return

        conn = sqlite3.connect("reservas.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = ?", (int(id_texto),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Reserva #{id_texto} cancelada correctamente.")
        ventana.destroy()

    def limpiar_datos():
        for lbl in detalles.values():
            lbl.config(text="---")
        btn_cancelar.configure(state="disabled")
        lbl_estado.configure(
            text="Ingrese un ID y presione BUSCAR.",
            fg="#666680"
        )

    ventana = tk.Toplevel()
    ventana.title("Cancelar Reserva")
    ventana.geometry("600x560")
    ventana.resizable(False, False)
    ventana.configure(bg="#1e1e26")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Card.TFrame",   background="#2d2d3a", relief="flat")
    style.configure("Header.TLabel", background="#1e1e26", foreground="#ffffff",
                    font=("Segoe UI", 16, "bold"))
    style.configure("Field.TLabel",  background="#2d2d3a", foreground="#dcdcdc",
                    font=("Segoe UI", 10))
    style.configure("Value.TLabel",  background="#2d2d3a", foreground="#4cc9f0",
                    font=("Segoe UI", 10, "bold"))

    ttk.Label(ventana, text="CANCELAR RESERVA", style="Header.TLabel").pack(pady=(25, 10))

    search_frame = tk.Frame(ventana, bg="#1e1e26")
    search_frame.pack(pady=(0, 6))

    tk.Label(search_frame, text="ID:", bg="#1e1e26", fg="#dcdcdc",
             font=("Segoe UI", 10)).pack(side="left", padx=(0, 6))

    entry_id = tk.Entry(search_frame, width=12, font=("Segoe UI", 12),
                        bg="#3b3b4d", fg="white", insertbackground="white", border=0)
    entry_id.pack(side="left", ipady=5)

    btn_buscar = tk.Button(search_frame, text="BUSCAR", command=buscar,
                           bg="#4cc9f0", fg="#1e1e26", font=("Segoe UI", 9, "bold"),
                           relief="flat", padx=16, cursor="hand2")
    btn_buscar.pack(side="left", padx=(10, 0))
    btn_buscar.bind("<Enter>", lambda e: btn_buscar.configure(bg="#7dd6f0"))
    btn_buscar.bind("<Leave>", lambda e: btn_buscar.configure(bg="#4cc9f0"))

    lbl_estado = tk.Label(ventana, text="Ingrese un ID y presione BUSCAR.",
                          bg="#1e1e26", fg="#666680", font=("Segoe UI", 9, "italic"))
    lbl_estado.pack(pady=(2, 8))

    card = ttk.Frame(ventana, style="Card.TFrame", padding=20)
    card.pack(padx=40, pady=0, fill="both", expand=True)

    campos = [
        ("Aula",        "aula"),
        ("Fecha",       "fecha"),
        ("Hora Inicio", "hora_inicio"),
        ("Hora Fin",    "hora_fin"),
        ("Responsable", "responsable"),
        ("Descripción", "descripcion"),
    ]

    detalles = {}
    for label_text, key in campos:
        row = tk.Frame(card, bg="#2d2d3a")
        row.pack(fill="x", pady=7)

        tk.Label(row, text=f"{label_text.upper()}:", bg="#2d2d3a", fg="#dcdcdc",
                 font=("Segoe UI", 10), width=15, anchor="w").pack(side="left")

        val = tk.Label(row, text="---", bg="#2d2d3a", fg="#4cc9f0",
                       font=("Segoe UI", 10, "bold"))
        val.pack(side="left")
        detalles[key] = val

    btn_cancelar = tk.Button(ventana, text="CONFIRMAR CANCELACIÓN",
                             command=confirmar_cancelacion,
                             bg="#e05252", fg="white",
                             font=("Segoe UI", 11, "bold"),
                             relief="flat", cursor="hand2", state="disabled")
    btn_cancelar.pack(fill="x", padx=40, pady=(14, 6), ipady=10)
    btn_cancelar.bind("<Enter>", lambda e: btn_cancelar.configure(bg="#b33a3a")
                      if btn_cancelar["state"] == "normal" else None)
    btn_cancelar.bind("<Leave>", lambda e: btn_cancelar.configure(bg="#e05252")
                      if btn_cancelar["state"] == "normal" else None)

    btn_volver = tk.Button(ventana, text="VOLVER AL MENÚ", command=ventana.destroy,
                           bg="#3b3b4d", fg="white", font=("Segoe UI", 9, "bold"),
                           relief="flat", cursor="hand2")
    btn_volver.pack(fill="x", padx=40, pady=(0, 20), ipady=8)
    btn_volver.bind("<Enter>", lambda e: btn_volver.configure(bg="#555570"))
    btn_volver.bind("<Leave>", lambda e: btn_volver.configure(bg="#3b3b4d"))

    ventana.grab_set()