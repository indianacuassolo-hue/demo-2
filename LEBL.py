from airport import IsSchengenAirport
import matplotlib.patches as patches

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.gates = []
        self.airlines = []
        self.boarding_areas = []

class BoardingArea:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.gate = []

class Gate:
    def __init__(self, Id):
        self.Id = Id
        self.ocupado = False
        self.aircraft = ""

def SetGates(area, init_gate, end_gate, prefix):

    if end_gate <= init_gate:
        return -1

    area.gate = []

    for i in range(init_gate, end_gate + 1):
        gate_name = prefix + str(i)
        new_gate = Gate(gate_name)
        area.gate.append(new_gate)

    return 0

def LoadAirlines (terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("File not found")
        return -1

    terminal.airlines = []

    for line in f:
        line = line.strip()
        if line == "":
            continue

        parts = line.split('\t')

        if len(parts) == 2:
            airline_name = parts[0]
            airline_code = parts[1]
            terminal.airlines.append((airline_name, airline_code))
        else:
            print(f"Line format error in {filename}: {line}")

    f.close()
    return 0

def LoadAirportStructure (filename):
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("File not found")
        return -1
    
    lines = f.readlines()
    
    first_line = lines[0].split()
    airport_code = first_line[0]
    num_terminals = int(first_line[1])

    bcn = BarcelonaAP(airport_code)

    i = 1
    
    for t in range(num_terminals):

        terminal_parts = lines [i].split()
        terminal_name = terminal_parts[1]
        num_areas = int(terminal_parts[2])
        i += 1

        terminal = Terminal(terminal_name)

        for a in range(num_areas):
            area_parts = lines[i].split()
            area_name = area_parts[1]
            area_type = area_parts[2]
            init_gate = int(area_parts[4])
            end_gate = int(area_parts[6])

            i += 1

            area = BoardingArea(area_name, area_type)

            prefix = terminal_name + area_name

            SetGates(area, init_gate, end_gate, prefix)

            terminal.boarding_areas.append(area)
        
        LoadAirlines(terminal, terminal_name)

        bcn.terminals.append(terminal)

    return bcn

def GateOccupancy(bcn):

    occupancy = []

    for terminal in range(len(bcn.terminals)):
        for area in range(len(bcn.terminals[terminal].boarding_areas)):
            for gate in range(len(bcn.terminals[terminal].boarding_areas[area].gate)):
                occupancy.append((bcn.terminals[terminal].boarding_areas[area].gate[gate].Id, bcn.terminals[terminal].boarding_areas[area].gate[gate].ocupado, bcn.terminals[terminal].boarding_areas[area].gate[gate].aircraft))

    return occupancy

def PlotAirportSchematic(bcn, ax, terminal_filter=None):
    # Limpiamos el gráfico y ocultamos los ejes numéricos
    ax.clear()
    ax.axis('off') 
    
    y_offset = 0 # Controla la altura a la que se dibuja cada terminal
    
    for terminal in bcn.terminals:
        # ¡NUEVO!: Si hemos pedido un terminal específico y este no coincide, lo saltamos
        if terminal_filter is not None and terminal.name != terminal_filter:
            continue
            
        # 1. Dibujar la línea principal del Terminal (Tronco horizontal)
        ax.plot([0, len(terminal.boarding_areas) * 2], [y_offset, y_offset], lw=6, color='#004b79')
        ax.text(-0.5, y_offset, terminal.name, fontsize=12, fontweight='bold', va='center')
        
        for a_idx, area in enumerate(terminal.boarding_areas):
            x_area = a_idx * 2 + 1
            num_gates = len(area.gate)
            y_bottom = y_offset - (num_gates * 0.5) - 0.5
            
            # 2. Dibujar el pilar del Área de Embarque (Tronco vertical)
            ax.plot([x_area, x_area], [y_offset, y_bottom], lw=4, color='#004b79')
            ax.text(x_area, y_bottom - 0.5, area.name, fontsize=10, ha='center', fontweight='bold')
            
            for g_idx, gate in enumerate(area.gate):
                y_gate = y_offset - (g_idx + 1) * 0.5
                
                # 3. Dibujar la "rama" de la puerta
                ax.plot([x_area, x_area + 0.5], [y_gate, y_gate], lw=2, color='#004b79')
                
                # Etiqueta de la puerta (ej. T1BAaG1)
                ax.text(x_area + 0.25, y_gate + 0.1, gate.Id, fontsize=6, ha='center')
                
                # 4. Dibujar la caja de estado (Verde=Libre, Rojo=Ocupado)
                color = 'red' if gate.ocupado else '#2ca02c'
                rect = patches.Rectangle((x_area + 0.6, y_gate - 0.15), 0.3, 0.3, facecolor=color)
                ax.add_patch(rect)
                
                # 5. Si está ocupada, escribir la ID del avión al lado
                if gate.ocupado and gate.aircraft != "":
                    # Usamos gate.aircraft.aircraft como arreglamos en el paso anterior
                    ax.text(x_area - 0.2, y_gate, gate.aircraft.aircraft, fontsize=8, color='red', ha='right', va='center')
        
        # Calcular el espacio necesario para el siguiente terminal hacia abajo
        if terminal.boarding_areas:
            y_offset -= (max([len(a.gate) for a in terminal.boarding_areas]) * 0.5 + 3)
        else:
            y_offset -= 3
            
    # Ajustar la cámara del gráfico para que se vea todo
    ax.autoscale_view()

def IsAirlineInTerminal (terminal, name):

    if name == "":
        return False, -1
    
    if len(terminal.airlines) == 0:
        return False, 0
    
    for airline in terminal.airlines:
        airline_name = airline[0]
        airline_code = airline[1]
        if airline_name == name or airline_code == name:
            return True, 0
        
    return False, 0

def SearchTerminal(bcn, name):

    for terminal in bcn.terminals:
        found, status = IsAirlineInTerminal(terminal, name)
        if found:
            return terminal.name
        
    return ""

def AssignGate(bcn, aircraft):

    if IsSchengenAirport(aircraft.origin):
        flight_type = "Schengen"
    else:
        flight_type = "Non-Schengen"

    terminal_name = SearchTerminal(bcn, aircraft.airline)

    terminal_obj = None
    for terminal in bcn.terminals:
        if terminal.name == terminal_name:
            terminal_obj = terminal
    
    if terminal_obj is None:
        if len(bcn.terminals) > 0:
            terminal_obj = bcn.terminals[0]
        else:
            return -1
        
    for area in terminal_obj.boarding_areas:
        if area.type.lower() == flight_type.lower():
            for gate in area.gate:
                if gate.ocupado == False:
                    gate.ocupado = True
                    gate.aircraft = aircraft
                    return 0
    
    return -1

def PrintGateOccupancy(bcn):

    for terminal in range(len(bcn.terminals)):
        print(f"Terminal: {bcn.terminals[terminal].name}")
        for area in range(len(terminal.boarding_areas)):
            print(f"  Boarding Area: {terminal.boarding_areas[area].name} ({terminal.boarding_areas[area].type})")
            for gate in range(len(terminal.boarding_areas[area].gate)):
                free = 0
                occupied = 0
                for gate in range(len(area.gate)):
                    if gate.ocupado:
                        occupied += 1
                    else:
                        free += 1
                    
                print("Area" + area.name + "(" + area.type + "): " + str(free) + " free gates, " + str(occupied) + " occupied gates")

def PlotGateOccupancy(bcn, ax):
    
    labels = []
    free_gates = []
    occupied_gates = []

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            free = 0
            occupied = 0
            for gate in area.gate:
                if gate.ocupado:
                    occupied += 1
                else:
                    free += 1
            
            labels.append("Area" + area.name + "\n(" + area.type + ")")
            free_gates.append(free)
            occupied_gates.append(occupied)

    ax.bar(labels, occupied_gates, label = "Occupied Gates", color = '#F472B6')
    ax.bar(labels, free_gates, bottom = occupied_gates, label = "Free Gates", color = '#782BA5')
    ax.set_xlabel("Boarding Areas")
    ax.set_ylabel("Number of Gates")
    ax.set_title("Gate Occupancy")
    ax.legend()
    ax.tick_params(axis='x', rotation=45)