from tkinter import *
from tkinter import messagebox  # Necesario para mostrar mensajes de error o información
from tkinter import ttk  # Necesario para el Scrollbar moderno
from matplotlib.figure import Figure # Necesario para crear figuras de Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Necesario para integrar Matplotlib con Tkinter
# Importamos las funciones de los otros archivos.
import airport as ap
import aircraft as ac
import LEBL2 as lb

# Lista global de aeropuertos
airports = []

# Funciones para los botones
def Load():
    airports.clear()
    
    resultado = airports.extend(ap.LoadAirports(pathEntry.get()))
    if resultado == 0:
        messagebox.showerror("Carga de Aeropuertos", "Error al cargar el archivo.")
    else:
        messagebox.showinfo("Carga de Aeropuertos", "¡Aeropuertos cargados correctamente!")
    for a in airports:
        ap.SetSchengen(a)

def Add():
    new = ap.Airport(ICAOEntry.get(), float(latEntry.get()), float(lonEntry.get()))
    ap.SetSchengen(new)
    resultado = ap.AddAirport(airports, new)
    if resultado == 0:
        messagebox.showinfo("Agregar Aeropuerto", f"¡Aeropuerto {ICAOEntry.get()} agregado!")
    else:
        messagebox.showerror("Agregar Aeropuerto", f"Error: No se pudo agregar el aeropuerto {ICAOEntry.get()}.")

def Remove():
    resultado = ap.RemoveAirport(airports, ICAOEntry.get())
    if resultado == 0:
        messagebox.showinfo("Eliminar Aeropuerto", f"¡Aeropuerto {ICAOEntry.get()} eliminado!")
    else:
        messagebox.showerror("Eliminar Aeropuerto", f"Error: Aeropuerto {ICAOEntry.get()} no encontrado.")

def plot():
    if not airports:
        messagebox.showwarning("Gráfico", "No hay aeropuertos para mostrar.")
    ax = clear_ax()
    ap.PlotAirports(airports, ax)
    draw_chart()

def Map():
    if airports:
        resultado =ap.MapAirports(airports, "airports.kml")
        if resultado == 0:
            messagebox.showerror("Google Earth", "Error al crear el archivo.")
        else:
            messagebox.showinfo("Google Earth", "¡Archivo 'airports.kml' creado para Google Earth!")

def SaveSchengen():
    if not airports:
        print("No hay aeropuertos para guardar.")
        return
    
    # Llama a la función de airport.py y guarda el archivo como "schengen_airports.txt"
    resultado = ap.SaveSchengenAirports(airports, "schengen_airports.txt")
    
    if resultado == 0:
        messagebox.showinfo("Guardar Aeropuertos Schengen", "¡Aeropuertos Schengen guardados en 'schengen_airports.txt'!")
    else:
        messagebox.showerror("Guardar Aeropuertos Schengen", "Error al guardar o la lista estaba vacía.")

# Lista global de vuelos
aircrafts = []
# Botones para funciones de aircraft
def LoadFlights():
    aircrafts.clear()
    resultado = aircrafts.extend(ac.LoadArrivals(flightPathEntry.get()))
    if resultado == 0:
        messagebox.showerror("Carga de Vuelos", "Error al cargar el archivo.")
    else:
        messagebox.showinfo("Carga de Vuelos", "¡Vuelos cargados correctamente!")

def PlotArrivals():
    ax = clear_ax()
    ac.PlotArrivals(aircrafts, ax)
    draw_chart()

def PlotAirlines():
    ax = clear_ax()
    ac.PlotAirlines(aircrafts, ax)
    draw_chart()

def PlotFlightsType():
    ax = clear_ax()
    ac.PlotFlightsType(aircrafts, ax)
    draw_chart()

def SaveFlights():
    if not aircrafts:
        print("No hay vuelos para guardar.")
    resultado = ac.SaveFlights(aircrafts, "ArrivalsFlights.txt")
    
    if resultado == 0:
        messagebox.showinfo("Guardar Vuelos", "¡Vuelos guardados en 'ArrivalsFlights.txt'!")
    else:
        messagebox.showerror("Guardar Vuelos", "Error al guardar o la lista estaba vacía.")

def MapFlights():
    resultado = ac.MapFlights(aircrafts)
    if resultado == 0:
        messagebox.showinfo("Google Earth", "¡Archivo 'flights.kml' creado para Google Earth!")
    else:        
        messagebox.showerror("Google Earth", "Error al crear el archivo o la lista de vuelos estaba vacía.")

def LongDistance():
    long_distance = ac.LongDistanceArrivals(aircrafts)
    print("Vuelos de larga distancia: ", len(long_distance))
    resultado = ac.MapFlights(long_distance, "long_distance_flights.kml")
    if resultado == 0:
        messagebox.showinfo("Google Earth", "¡Archivo 'long_distance_flights.kml' creado para Google Earth!")
    else:
        messagebox.showerror("Google Earth", "Error al crear el archivo o la lista de vuelos estaba vacía.")

#Lista global para el aeropuerto LEBL
LEBL = []

# Funciones para los botones de LEBL
def LoadLEBLStructure():
    LEBL.clear()
    resultado = lb.LoadAirportStructure(leblPathEntry.get())
    if resultado == 0:
        messagebox.showerror("Carga de LEBL", "Error al cargar el archivo.")
    else:        
        LEBL.append(resultado)
        messagebox.showinfo("Carga de LEBL", "¡LEBL cargado correctamente!")

def LoadTerminals():
    if not LEBL:
        messagebox.showerror("Carga de Terminales", "Carga la estructura de LEBL antes de cargar las terminales.")
        return
    aeropuertoLEBL = LEBL[0]
    err = 0
    for t in aeropuertoLEBL.terminals:
        resultado = lb.LoadAirlines(t, t.name)
        if resultado != 0:
            err += 1
    if err == 0:
        messagebox.showinfo("Carga de Terminales", "¡Terminales y aerolíneas cargadas correctamente!")
    else:
        messagebox.showerror("Carga de Terminales", f"Error al cargar las terminales o aerolíneas. {err} terminales con error.")

def AssignGates():
    if not LEBL or not aircrafts:
        messagebox.showerror("Asignación de Puertas", "Carga la estructura y vuelos primero.")
        return
    aeropuertoLEBL = LEBL[0]

    for terminal in aeropuertoLEBL.terminals:
        for area in terminal.boarding:
            for gate in area.gates:
                gate.ocupado = False
                gate.aircraft = ""

    sin_asignar= 0 
    asignados = 0
    for flight in aircrafts:
        resultado = lb.AssignGate(aeropuertoLEBL, flight)
        if resultado == 0:
            asignados += 1
        else:
            sin_asignar += 1
    messagebox.showinfo("Asignación de Puertas", f"¡Asignación de puertas completada! {asignados} vuelos asignados, {sin_asignar} sin asignar.")

def ShowGateOccupancy():
    if not aircrafts or not LEBL:
        messagebox.showerror("Ocupación de Puertas", "Carga los vuelos, la estructura y terminales primero.")
        return
    
    aeropuerto = LEBL[0]
    if len(aeropuerto.terminals) == 0:
        messagebox.showerror("Error de Datos", "El archivo Terminals.txt se ha leído, pero tiene 0 terminales. ¡Revisa el formato del texto!")
        return

    resultado = lb.GateOccupancy(aeropuerto)
    if not resultado:
        messagebox.showerror("Ocupación de Puertas", "Las terminales están, pero tienen 0 puertas. Revisa los rangos en Terminals.txt.")
        return
    
    libre = 0
    ocupado = 0
    
    for puerta in resultado:
        if puerta[1] == "Occupied":
            ocupado += 1
        else:
            libre += 1
            
    messagebox.showinfo("Ocupación de Puertas", f"¡Ocupación de puertas obtenida!\nPuertas libres: {libre}\nPuertas ocupadas: {ocupado}.")

def SearchAirlineTerminal():
    if LEBL == 0 or aircrafts == 0:
        messagebox.showerror("Búsqueda de Vuelo", "Carga la estructura de LEBL y las terminales  antes de buscar un vuelo.")
    else:
        aeroline_name = airlineSearchEntry.get()
        if aeroline_name == "":
            messagebox.showerror("Búsqueda de Vuelo", "Introduce el nombre o código de la aerolínea a buscar.")
            return
        resultado = lb.SearchTerminal(LEBL[0], aeroline_name)
        if resultado == 0:
            messagebox.showerror("Búsqueda de Vuelo", f"Error al buscar la aerolínea {aeroline_name}.")
        else:

            messagebox.showinfo("Búsqueda de Vuelo", f"¡Aerolínea {aeroline_name} encontrada! Opera en la terminal: {resultado}.")

# --- Chart setup ---
fig = Figure(figsize=(6, 5), dpi=100)

def clear_ax():
    fig.clf()
    return fig.add_subplot(111)

def draw_chart():
    canvas.draw()

# Finestra
window = Tk()
window.title("Airport")
window.geometry("1500x700")
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=3)

#Canvas izquierdo para implementar un scrollbar
LEFT_panel = Frame(window, width=220)
LEFT_panel.pack(side="left", fill="y", padx=10, pady=10)

canvas_scroll = Canvas(LEFT_panel, width=200)
scrollbar = ttk.Scrollbar(LEFT_panel, orient="vertical", command=canvas_scroll.yview)
scrollable_frame = Frame(canvas_scroll)

scrollable_frame.bind( "<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))

canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
#Muestra la barra para que se sepa que existe la función del scroll.
canvas_scroll.configure(yscrollcommand=scrollbar.set) 
scrollbar.pack(side="right", fill="y")

canvas_scroll.pack(side="left", fill="both", expand=True)

#Canvas derecho para las gráficas y las listas (aun por implementar)
right_panel = Frame(window)
right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#Títols
tituloLabel = Label(scrollable_frame, text="AIRPORT", font=("Times New Roman", 18, "bold"))
tituloLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)

#Arxius
archivoLabel = Label(scrollable_frame, text="Archivo:")
archivoLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E+W)

pathEntry = Entry(scrollable_frame, width = 12)
pathEntry.insert(0, "Airports.txt")
pathEntry.grid(row=1, column=1, padx=5, pady=5, sticky=E+W)

# Pel que fa ICAO:
ICAOLabel = Label(scrollable_frame, text="ICAO:")
ICAOLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E+W)

ICAOEntry = Entry(scrollable_frame, width = 12)
ICAOEntry.grid(row=2, column=1, padx=5, pady=5, sticky=E+W)

#Para las coordenadas:
latLabel = Label(scrollable_frame, text="Latitud:")
latLabel.grid(row=3, column=0, padx=5, pady=5, sticky=E+W)
latEntry = Entry(scrollable_frame, width = 12)
latEntry.grid(row=3, column=1, padx=5, pady=5, sticky=E+W)

lonLabel = Label(scrollable_frame, text="Longitud:")
lonLabel.grid(row=4, column=0, padx=5, pady=5, sticky=E+W)
lonEntry = Entry(scrollable_frame, width = 12)
lonEntry.grid(row=4, column=1, padx=5, pady=5, sticky=E+W)

#Botons, per fer un botó:
#bg(background), "color/#codi hexadecimal", fg(foreground, color lletra), "white", font(tipus lletra, mida, estil)
#.grid() organitza els elements en files (row) i columnes (column), sticky serveix per estirar-se
Button(scrollable_frame, text="Load Airports", bg="#F472B6", fg="white", command=Load).grid(row=5, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Add Airport",   bg="#F472B6", fg="white", command=Add).grid(row=6, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Remove Airport",bg="#F472B6",   fg="white", command=Remove).grid(row=7, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Save Schengen",  bg="#F472B6", fg="white", command=SaveSchengen).grid(row=8, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Ver Gráfico",   bg="#F472B6", fg="white", command=plot).grid(row=9, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Google Earth",  bg="#F472B6", fg="white", command=Map).grid(row=10, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

# Separador y título sección flights
Label(scrollable_frame, text="FLIGHTS", font=("Times New Roman", 18, "bold")).grid(row=11, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

# Arxiu flights
flightArchivoLabel = Label(scrollable_frame, text="Archivo:")
flightArchivoLabel.grid(row=12, column=0, padx=5, pady=5, sticky=E+W)

flightPathEntry = Entry(scrollable_frame, width = 12)
flightPathEntry.insert(0, "Arrivals.txt")
flightPathEntry.grid(row=12, column=1, padx=5, pady=5, sticky=E+W)

# Botons flights
Button(scrollable_frame, text="Load Flights",     bg="#F472B6", fg="white", command=LoadFlights).grid(row=13, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Save Flights",     bg="#F472B6", fg="white", command=SaveFlights).grid(row=14, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Plot Arrivals",    bg="#F472B6", fg="white", command=PlotArrivals).grid(row=15, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Plot Airlines",    bg="#F472B6", fg="white", command=PlotAirlines).grid(row=16, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Schengen Chart",   bg="#F472B6", fg="white", command=PlotFlightsType).grid(row=17, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Google Earth",     bg="#F472B6", fg="white", command=MapFlights).grid(row=18, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Long Distance",    bg="#F472B6", fg="white", command=LongDistance).grid(row=19, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

#Separador y título sección LEBL
Label(scrollable_frame, text="LEBL", font=("Times New Roman", 18, "bold")).grid(row=20, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

#Archivo para LEBL
leblArchivoLabel = Label(scrollable_frame, text="Archivo LEBL:")
leblArchivoLabel.grid(row=21, column=0, padx=5, pady=5, sticky=E+W)

leblPathEntry = Entry(scrollable_frame, width = 12)
leblPathEntry.insert(0, "Terminals.txt")
leblPathEntry.grid(row=21, column=1, padx=5, pady=5, sticky=E+W)

#Para buscar en que terminal opera x aerolínea.
airlineSearchLabel = Label(scrollable_frame, text="Buscar Aerolínea:")
airlineSearchLabel.grid(row=22, column=0, padx=5, pady=5, sticky=E+W)

airlineSearchEntry = Entry(scrollable_frame, width = 12)
airlineSearchEntry.grid(row=22, column=1, padx=5, pady=5, sticky=E+W)

# Botones para funciones de LEBL
Button(scrollable_frame, text="Load LEBL Structure", bg="#F472B6", fg="white", command=LoadLEBLStructure).grid(row=23, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Load Terminals", bg="#F472B6", fg="white", command=LoadTerminals).grid(row=24, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Assign Gates", bg="#F472B6", fg="white", command=AssignGates).grid(row=25, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Gate Occupancy", bg="#F472B6", fg="white", command=ShowGateOccupancy).grid(row=26, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(scrollable_frame, text="Search Flight Terminal", bg="#F472B6", fg="white", command=SearchAirlineTerminal).grid(row=27, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

#Un recuadro en el que muestre si se ejecuta una función correctamente o no.


#Para mostrar los gráficos en la misma ventana
canvas = FigureCanvasTkAgg(fig, master=right_panel)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

#Función para que el scroll solo funcione en la parte de los botones y no en el gráfico.
def _on_mousewheel(event):
    canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")

#Las funciones para activar y desactivar el scroll al entrar o salir del área de los botones.
def _activar_scroll(event):
    window.bind_all("<MouseWheel>", _on_mousewheel)

def _desactivar_scroll(event):
    window.unbind_all("<MouseWheel>")

# Vinculamos las funciones de activar y desactivar el scroll a los eventos de entrar y salir del área de los botones.
LEFT_panel.bind('<Enter>', _activar_scroll)
LEFT_panel.bind('<Leave>', _desactivar_scroll)

window.mainloop()