import customtkinter as ctk
import infoPD
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import pandas as pd
import numpy as np

canvas = None
db = pd.DataFrame()
show_regression_line = False

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Amazon Scraper")
app.geometry("900x600")

def on_closing():
    app.destroy()
    sys.exit()

def crear_grafico(df, show_regression=False):
    global canvas

    if canvas:
        canvas.get_tk_widget().pack_forget()

    fig, ax = plt.subplots(figsize=(5, 4))

    df = df.dropna(subset=['Precio', 'Estrellas'])

    x = df['Precio']
    y = df['Estrellas']

    ax.scatter(x, y, color="blue", label='Datos')

    if show_regression:
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        x_fit = np.linspace(x.min(), x.max(), 100)
        y_fit = polynomial(x_fit)

        ax.plot(x_fit, y_fit, color='red', linestyle='--', label='Regression Line')

    ax.set_xlabel('Price')
    ax.set_ylabel('Stars')
    ax.set_title('Price vs Stars')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=center_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def filter(df, stars_filter): 
    lower_bound = stars_filter - 1
    upper_bound = stars_filter
    
    filtered_df = df.dropna(subset=['Estrellas'])
    filtered_df = filtered_df[(filtered_df['Estrellas'] > lower_bound) & (filtered_df['Estrellas'] <= upper_bound)]
    
    return filtered_df

def buscar():
    global db
    element = search_entry.get()
    
    if not os.path.exists("data/"):
        os.makedirs("data/")

    if os.path.isfile(f"data/{element}.csv"):
        db = pd.read_csv(f'data/{element}.csv')
    else:
        db = infoPD.getInfo(search_entry.get())
        db.to_csv(f'data/{element}.csv', index=False)

    db['Precio'] = pd.to_numeric(db['Precio'], errors='coerce')
    db['Estrellas'] = pd.to_numeric(db['Estrellas'], errors='coerce')

    info_text.delete("1.0", "end")
    textInfo = f"Average Prices: {round(db['Precio'].mean(), 2)}$ \n"
    textInfo += f"Average Stars: {round(db['Estrellas'].mean(), 1)} \n"
    info_text.insert("1.0", textInfo)

    crear_grafico(db, show_regression_line)

def toggle_regression_line():
    global show_regression_line
    show_regression_line = not show_regression_line
    crear_grafico(db, show_regression_line)

# Panel Superior: Barra de Búsqueda
search_frame = ctk.CTkFrame(app)
search_frame.pack(side="top", fill="x", pady=10, padx=10)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar un producto...")
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_button = ctk.CTkButton(search_frame, text="Buscar", command=buscar)
search_button.pack(side="right", padx=5)

# Panel Izquierdo: Botones de Filtros y Preferencias
left_frame = ctk.CTkFrame(app, width=150)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# Crear botones de filtro
filter_button1 = ctk.CTkButton(left_frame, text="1-2 Stars", command=lambda: crear_grafico(filter(db, 2), show_regression_line))
filter_button1.pack(pady=5)

filter_button2 = ctk.CTkButton(left_frame, text="2-3 Stars", command=lambda: crear_grafico(filter(db, 3), show_regression_line))
filter_button2.pack(pady=5)

filter_button3 = ctk.CTkButton(left_frame, text="3-4 Stars", command=lambda: crear_grafico(filter(db, 4), show_regression_line))
filter_button3.pack(pady=5)

filter_button4 = ctk.CTkButton(left_frame, text="4-5 Stars", command=lambda: crear_grafico(filter(db, 5), show_regression_line))
filter_button4.pack(pady=5)

filter_button5 = ctk.CTkButton(left_frame, text="All Data", command=lambda: crear_grafico(db, show_regression_line))
filter_button5.pack(pady=5)

# Panel Central: Espacio para Gráficas
center_frame = ctk.CTkFrame(app)
center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Panel Inferior: Botón para Toggle de Recta de Regresión
bottom_frame = ctk.CTkFrame(app)
bottom_frame.pack(side="bottom", fill="x", pady=10, padx=10)

toggle_regression_button = ctk.CTkButton(bottom_frame, text="Toggle Regresion Line", command=toggle_regression_line)
toggle_regression_button.pack()

# Panel Derecho: Información en Texto Plano
right_frame = ctk.CTkFrame(app, width=200)
right_frame.pack(side="right", fill="y", padx=10, pady=10)

info_label = ctk.CTkLabel(right_frame, text="Data", font=("Arial", 14))
info_label.pack(pady=10)

info_text = ctk.CTkTextbox(right_frame, height=300, width=180)
info_text.insert("0.0", "")
info_text.pack(pady=10)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
