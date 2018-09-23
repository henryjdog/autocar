import gps
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    R = 6371 * 1000
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    m = R * c
    return m 


session = gps.gps('localhost', '2947')
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

time_prev = None
lon_prev = None
lat_prev = None

while True:
    try:
        report = session.next()
        # Wait for a 'TPV' report and display current lat, lon
        if report['class'] == 'TPV':
            if hasattr(report, 'lat'):
                time = report.time
                lat = report.lat
                lon = report.lon
                speed = report.speed * 1.68781
                if lon_prev is None:
                    time_prev = time
                    lon_prev = lon
                    lat_prev = lat
                else: 
                    m = haversine(lon_prev, lat_prev, lon, lat)
#                    speed_calc = m / (time-time_prev)
                    time_prev = time
                    lon_prev = lon
                    lat_prev = lat

                    print time, lat, lon, speed, m#, speed_calc 

    except KeyError:
        pass
