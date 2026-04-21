from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import airport as ap
import aircraft as ac

airports = []

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

aircrafts = []

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
window.geometry("1100x700")
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=3)

#Títols
tituloLabel = Label(window, text="----AIRPORT----", font=("Times New Roman", 18, "bold"))
tituloLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=E+W)

#Arxius
archivoLabel = Label(window, text="Archivo:")
archivoLabel.grid(row=1, column=0, padx=5, pady=5, sticky=E+W)

pathEntry = Entry(window)
pathEntry.insert(0, "Airports.txt")
pathEntry.grid(row=1, column=1, padx=5, pady=5, sticky=E+W)

# Pel que fa ICAO:
ICAOLabel = Label(window, text="ICAO:")
ICAOLabel.grid(row=2, column=0, padx=5, pady=5, sticky=E+W)

ICAOEntry = Entry(window)
ICAOEntry.grid(row=2, column=1, padx=5, pady=5, sticky=E+W)

#Para las coordenadas:
latLabel = Label(window, text="Latitud:")
latLabel.grid(row=3, column=0, padx=5, pady=5, sticky=E+W)
latEntry = Entry(window)
latEntry.grid(row=3, column=1, padx=5, pady=5, sticky=E+W)

lonLabel = Label(window, text="Longitud:")
lonLabel.grid(row=4, column=0, padx=5, pady=5, sticky=E+W)
lonEntry = Entry(window)
lonEntry.grid(row=4, column=1, padx=5, pady=5, sticky=E+W)

#Botons, per fer un botó:
#bg(background), "color/#codi hexadecimal", fg(foreground, color lletra), "white", font(tipus lletra, mida, estil)
#.grid() organitza els elements en files (row) i columnes (column), sticky serveix per estirar-se
Button(window, text="Load Airports", bg="#F472B6", fg="white", command=Load).grid(row=5, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Add Airport",   bg="#F472B6", fg="white", command=Add).grid(row=6, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Remove Airport",bg="#F472B6",   fg="white", command=Remove).grid(row=7, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Save Schengen",  bg="#F472B6", fg="white", command=SaveSchengen).grid(row=8, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Ver Gráfico",   bg="#F472B6", fg="white", command=plot).grid(row=9, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Google Earth",  bg="#F472B6", fg="white", command=Map).grid(row=10, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

# Separador y título sección flights
Label(window, text="----FLIGHTS----", font=("Times New Roman", 18, "bold")).grid(row=11, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

# Arxiu flights
flightArchivoLabel = Label(window, text="Archivo:")
flightArchivoLabel.grid(row=12, column=0, padx=5, pady=5, sticky=E+W)

flightPathEntry = Entry(window)
flightPathEntry.insert(0, "Arrivals.txt")
flightPathEntry.grid(row=12, column=1, padx=5, pady=5, sticky=E+W)

# Botons flights
Button(window, text="Load Flights",     bg="#F472B6", fg="white", command=LoadFlights).grid(row=13, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Save Flights",     bg="#F472B6", fg="white", command=SaveFlights).grid(row=14, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Plot Arrivals",    bg="#F472B6", fg="white", command=PlotArrivals).grid(row=15, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Plot Airlines",    bg="#F472B6", fg="white", command=PlotAirlines).grid(row=16, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Schengen Chart",   bg="#F472B6", fg="white", command=PlotFlightsType).grid(row=17, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Google Earth",     bg="#F472B6", fg="white", command=MapFlights).grid(row=18, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)
Button(window, text="Long Distance",    bg="#F472B6", fg="white", command=LongDistance).grid(row=19, column=0, columnspan=2, padx=5, pady=3, sticky=E+W)

#Un recuadro en el que muestre si se ejecuta una función correctamente o no.


#Para mostrar los gráficos en la misma ventana
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=2, column=2, columnspan=2, rowspan=15, padx=12, pady=12, sticky=N+S+E+W)

window.mainloop()