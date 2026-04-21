import matplotlib.pyplot as plt

# ============================================================
# CLASS DEFINITION
# ============================================================

class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = False  # Default: not Schengen


# ============================================================
# SCHENGEN FUNCTIONS
# ============================================================

def IsSchengenAirport(code):
    """
    Receives the ICAO code of an airport and checks if it belongs
    to a Schengen country. Returns True or False.
    Returns False if code is empty or too short.
    BUG FIX: 'ET' (Ethiopia) was in the original list but is NOT Schengen — removed.
    """
    schengen_prefixes = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED',
        'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM',
        'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS', 'GC'
    ]
    if not code or len(code) < 2:
        return False
    prefix = str(code[0:2]).upper()
    return prefix in schengen_prefixes


def SetSchengen(airport):
    """Receives an Airport and sets its schengen attribute."""
    airport.schengen = IsSchengenAirport(airport.ICAO)


def PrintAirport(airport):
    """Prints the data of an airport to the console."""
    print(f"ICAO: {airport.ICAO}")
    print(f"Coordinates: {airport.latitude:.6f}, {airport.longitude:.6f}")
    print(f"Schengen: {airport.schengen}")


# ============================================================
# FILE I/O FUNCTIONS
# ============================================================

def LoadAirports(filename):
    """
    Opens the file and returns a list of Airport objects.
    Expected file format (DMS):
        CODE LAT LON
        BIKF N635906 W0223620
    Sets the Schengen attribute for each loaded airport.
    Returns empty list if file not found or on error.
    """
    airports = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines[1:]:  # skip header
            parts = line.strip().split()
            if len(parts) == 3:
                code = parts[0]

                lat_str = parts[1]
                lat = int(lat_str[1:3]) + int(lat_str[3:5]) / 60 + int(lat_str[5:7]) / 3600
                if lat_str[0] == 'S':
                    lat = -lat

                lon_str = parts[2]
                lon = int(lon_str[1:4]) + int(lon_str[4:6]) / 60 + int(lon_str[6:8]) / 3600
                if lon_str[0] == 'W':
                    lon = -lon

                a = Airport(code, lat, lon)
                SetSchengen(a)
                airports.append(a)

    except FileNotFoundError:
        return []
    except Exception:
        return airports

    return airports


def SaveSchengenAirports(airports, filename):
    """
    Writes Schengen airports from the list to a file.
    Returns -1 if list is empty, 0 on success.
    BUG FIX: original returned a string on error and was missing newline after header.
    """
    if len(airports) == 0:
        return -1

    with open(filename, 'w') as f:
        f.write("CODE LAT LON\n")
        for a in airports:
            if a.schengen:
                f.write(f"{a.ICAO} {a.latitude} {a.longitude}\n")
    return 0


def AddAirport(airports, airport):
    """
    Adds airport to the list only if its ICAO code is not already present.
    Returns True if added, False if it was a duplicate.
    """
    for a in airports:
        if a.ICAO == airport.ICAO:
            return False
    airports.append(airport)
    return True


def RemoveAirport(airports, code):
    """
    Removes the airport with the given ICAO code from the list.
    Returns -1 if not found, 0 on success.
    BUG FIX (CRITICAL): original rebuilt a local list which did NOT modify
    the caller's list. Fixed using list.pop().
    """
    for i in range(len(airports)):
        if airports[i].ICAO == code:
            airports.pop(i)
            return 0
    return -1


def SetAllSchengen(airports):
    """
    Iterates over the list and sets the Schengen attribute for every airport.
    Returns the count of Schengen airports found.
    """
    count = 0
    for a in airports:
        SetSchengen(a)
        if a.schengen:
            count += 1
    return count


def CountSchengen(airports):
    """Returns (n_schengen, n_total) for the given list."""
    n_schengen = sum(1 for a in airports if a.schengen)
    return n_schengen, len(airports)


def CreateAirport(icao, lat, lon):
    """
    Validates inputs, creates an Airport, sets its Schengen attribute,
    and returns (airport, error_message).
    On success: (Airport, None).
    On failure: (None, str describing the problem).
    """
    icao = icao.strip().upper()
    if len(icao) < 2:
        return None, "ICAO code must be at least 2 characters."
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        return None, "Latitude and Longitude must be decimal numbers.\nExample: 41.2974 / 2.0833"
    a = Airport(icao, lat, lon)
    SetSchengen(a)
    return a, None


# ============================================================
# PLOT FUNCTIONS
# ============================================================

def PlotAirports(airports, ax):
    """
    Shows a stacked bar chart with Schengen vs Non-Schengen airports.
    Returns an error string if the list is empty, None on success.
    """
    if len(airports) == 0:
        return "The airport list is empty — nothing to plot."

    n_schengen, n_total = CountSchengen(airports)
    n_no_schengen = n_total - n_schengen

    labels = ['Airports']
    ax.bar(labels, [n_schengen],    label='Schengen',    color='steelblue')
    ax.bar(labels, [n_no_schengen], bottom=[n_schengen], label='No Schengen', color='lightcoral')
    ax.set_ylabel('Count')
    ax.set_title('Schengen vs Non-Schengen Airports')
    ax.legend()
    return None


# ============================================================
# KML / GOOGLE EARTH FUNCTION
# ============================================================

def MapAirports(airports, filename="airports.kml"):
    if not airports:
        return "The airport list is empty — nothing to export."

    try:
        with open(filename, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            f.write('<Document>\n')
            f.write('  <name>Airports Map</name>\n')

            for a in airports:
                color = "ffff0000" if a.schengen else "ff0000ff"
                f.write('  <Placemark>\n')
                f.write(f'    <name>{a.ICAO}</name>\n')
                f.write('    <Style>\n')
                f.write('      <IconStyle>\n')
                f.write(f'        <color>{color}</color>\n')
                f.write('      </IconStyle>\n')
                f.write('    </Style>\n')
                f.write('    <Point>\n')
                f.write(f'      <coordinates>{a.longitude},{a.latitude},0</coordinates>\n')
                f.write('    </Point>\n')
                f.write('  </Placemark>\n')

            f.write('</Document>\n')
            f.write('</kml>\n')
    except IOError as e:
        return f"Could not write file: {e}"

    return None
