import matplotlib.pyplot as plt
import math

from airport import LoadAirports

class Aircraft:
    def __init__(self, aircraft, origin, arrival, airline):
        self.aircraft = aircraft
        self.origin = origin
        self.arrival = arrival
        self.airline = airline

def LoadArrivals (filename):
    arrivals = []
    try:
        file = open(filename)
        lines = file.readlines()
        for i in range(1, len(lines)):
            parts = lines[i].split()
            if len(parts) == 4:
                aircraft = parts[0]
                origin = parts[1]
                arrival = parts[2]
                airline = parts[3]
                arrivals.append(Aircraft(aircraft, origin, arrival, airline))
    except FileNotFoundError:
        print("File not found")
    return arrivals

def PlotArrivals (aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return
    arrivals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    cantidad = [0]*24
    for aircraft in aircrafts:
        hour,minute = aircraft.arrival.split(":")
        cantidad[int(hour)] = cantidad[int(hour)] + 1
    plt.bar(arrivals, cantidad, color='#1e9faa')
    plt.xlabel('Hour')
    plt.ylabel('Vuelos')
    plt.title('Arrivals every hour')
    plt.show()

def SaveFlights (aircrafts, filename):
    if not aircrafts:
        return
    f = open(filename, 'w')
    f.write("Aircraft origin  arrival airline\n")
    for aircraft in aircrafts:
        f.write(f"{aircraft.aircraft} {aircraft.origin} {aircraft.arrival}{aircraft.airline}\n")
    f.close()
def PlotAirlines (aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return
    cont = {}
    for aircraft in aircrafts:
        airline = aircraft.airline
        if airline not in cont:
            cont[airline] = 0
        cont[airline] = cont[airline] + 1
    plt.bar(cont.keys(), cont.values(), color='#32612d')
    plt.xlabel('Airlines')
    plt.ylabel('Vuelos')
    plt.title('Flights every airline')
    plt.show()
def PlotFlightsType (aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    schengen = 0
    noschengen = 0
    for aircraft in aircrafts:
        if aircraft.origin[:2] in schengencode:
            schengen = schengen + 1
        else:
            noschengen = noschengen + 1
    plt.bar(["Schengen", "No Schengen"], [schengen, noschengen], color=["#8f1fcf", "#e57d90"])
    plt.xlabel('Type')
    plt.ylabel('Flights')
    plt.title('Flights schengen/No schengen')
    plt.show()
def MapFlights (aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    LEBLlon = 41.297445
    LEBLlat = 2.0832941
    f = open("flights.kml", "w")
    f.write('<Document>\n')
    f.write('<Placemark> \n')
    f.write('<name>Route {aircraft.origin}-LEBL</name>\n')
    f.write('<Style>\n')
    f.write('<LineStyle>\n')
    f.write('<color>' + "blue" + '</color>\n')
    f.write('</LineStyle>\n')
    f.write('</Style>\n')
    f.write(str(aircrafts.lon) + ',' + str(aircrafts.lat) + ',0\n')
    f.write(str(LEBLlon) + ',' + str(LEBLlat) + ',0\n')
    f.write('<coordinates>\n')
    f.write('</LineString>\n')
    f.write('</Placemark>\n')
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
def LongDistanceArrivals (aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return
    LEBLlon = 41.297445
    LEBLlat = 2.0832941
    R = 6371
    airports = LoadAirports("Airports.txt")
    for aircraft in aircrafts:
        if airports.code == airports.origin:
            lat1 = math.radians(aircraft.latitude)
            lon1 = math.radians(aircraft.longitude)
            lat2 = math.radians(LEBLlon)
            lon2 = math.radians(LEBLlat)
            a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
            distance = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            if distance > 2000:
                result = 0
                result = result + [aircraft]
if  __name__ == "__main__":
    aircrafts = LoadArrivals("arrivals.txt")
    print("Total aircrafts: ", len(aircrafts))
    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)
