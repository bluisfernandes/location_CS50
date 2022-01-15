from cs50 import SQL
import random
from geojson import Feature, Point, MultiPoint, FeatureCollection

db = SQL("sqlite:///location.db")



def coords_rdm (n_points=1, lat1= -33.4051268999, lat2 = -33.5042356, long1 = -70.505497, long2 = -70.8000687, decimals = 7):
    if decimals < 1:
        decimals = 1

    lat=[lat1, lat2]
    lat.sort()
    long=[long1, long2]
    long.sort()
    ref = [lat[0], lat[1], long[0], long[1]]
    ref_int = list(map(lambda x : int(x*10**decimals), ref))
    coords =[]

    for i in range(n_points):
        coords.append([random.randrange((ref_int[0]), (ref_int[1]))])

    coords.sort()
    for i in range(n_points):
        coords[i].append(random.randrange((ref_int[2]), (ref_int[3])))
    for i in range(n_points):
        for j in range(len(coords[i])):
            coords[i][j]= coords[i][j]/ 10**decimals

    return (coords)


def interpola(x, min_i = 0, max_i = 100, min_o = 0, max_o = 1):
    return min_o + (max_o - min_o)/(max_i - min_i)*(x - min_i)


# !pip install geojson
# import geojson

def geojson_rdm_multipoints(n =100):
    long1= -33.4051268999
    long2 = -33.5042356
    lat1 = -70.505497
    lat2 = -70.8000687
    latx = (lat1+lat2)/2
    longx=(long1+long2)/2

    pts1=coords_rdm(n,lat1,latx,long1,longx)
    pts2=coords_rdm(n,lat2,latx,long1,longx)
    pts3=coords_rdm(n,lat1,latx,long2,longx)
    pts4=coords_rdm(n,lat2,latx,long2,longx)

    areafeature1 = Feature(geometry=MultiPoint(pts1), properties={"color":"red"})
    areafeature2 = Feature(geometry=MultiPoint(pts2), properties={"color":"green"})
    areafeature3 = Feature(geometry=MultiPoint(pts3), properties={"color":"blue"})
    areafeature4 = Feature(geometry=MultiPoint(pts4), properties={"color":"yellow"})

    geojson = FeatureCollection([areafeature1,areafeature2,areafeature3,areafeature4])

    return geojson



def geojson_rdm_points(n =100):
    long1= -33.4051268999
    long2 = -33.5042356
    lat1 = -70.505497
    lat2 = -70.8000687
    latx = (lat1+lat2)/2
    longx=(long1+long2)/2

    areafeature=[]
    for i in range(n):
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat1,latx,long1,longx)[0]), properties={"area":1, "sensor":random.randrange(0, 2500)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat2,latx,long1,longx)[0]), properties={"area":2, "sensor":random.randrange(2500, 5000)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat1,latx,long2,longx)[0]), properties={"area":3, "sensor":random.randrange(5000, 7500)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat2,latx,long2,longx)[0]), properties={"area":4, "sensor":random.randrange(7500, 12200)}))

    geojson  = FeatureCollection(areafeature)

    return geojson


# Reads the json from android app and converts to a list of: [[long, lat, sensor, timestamp, user],]
def read_myjson(json):  
	data =[]

	for i in range(len(json["points"])):

		data.append([json["points"][i]["long"], json["points"][i]["lat"], json["info"][i]["sensor_light"],json["info"][i]["timestamp"],json["device"]])
	return data


# Converts the list of Attributes and convert to o pointfeatures
def geojson_pointfeature(data):
	pointfeature=[]
	for i in range(len(data)):
		pointfeature.append(Feature(geometry=Point([data[i][0],data[i][1]]), properties={"sensor":data[i][2],"timestamp": data[i][3]}))
	return pointfeature


# Converts the list of Attributes and convert to o pointfeatures
def geojson_featurecollection(pointfeature_list):
    featurecollection = FeatureCollection(pointfeature_list)
    return featurecollection


def store_data(data):
    for i in range(len(data)):
        try:
            point = db.execute("INSERT INTO location VALUES (?,?,?,?,?)",data[i][0],data[i][1],
                                                                    data[i][2],data[i][3],
                                                                    data[i][4])
        except Exception as e:  # or ValueError to narrow it down
            err = e
            # logging.error(f"fail inser{str(e)}")
    try:
        err #an error occour
    except NameError:
        # print("is invalid, ok, return 1")
        return point
    else:
        # print("deu ruim,return 0")
        return 0



featurecollection = {"features": [{"geometry": {"coordinates": [-70.60013, -33.416747], "type": "Point"}, "properties": {"sensor": 18443, "time": "2022-01-11T15:25:27.309"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600188, -33.416757], "type": "Point"}, "properties": {"sensor": 638, "time": "2022-01-11T15:25:32.765"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600262, -33.416718], "type": "Point"}, "properties": {"sensor": 2403, "time": "2022-01-11T15:25:33.772"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600313, -33.41674], "type": "Point"}, "properties": {"sensor": 297, "time": "2022-01-11T15:25:36.496"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60038, -33.41673], "type": "Point"}, "properties": {"sensor": 993, "time": "2022-01-11T15:25:45.505"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60042, -33.416695], "type": "Point"}, "properties": {"sensor": 701, "time": "2022-01-11T15:25:49.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600487, -33.416687], "type": "Point"}, "properties": {"sensor": 467, "time": "2022-01-11T15:25:55.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600553, -33.416693], "type": "Point"}, "properties": {"sensor": 257, "time": "2022-01-11T15:25:59.507"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60061, -33.416717], "type": "Point"}, "properties": {"sensor": 272, "time": "2022-01-11T15:26:03.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600667, -33.416745], "type": "Point"}, "properties": {"sensor": 9342, "time": "2022-01-11T15:26:06.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600732, -33.41676], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:10.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600793, -33.416777], "type": "Point"}, "properties": {"sensor": 372, "time": "2022-01-11T15:26:13.483"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600847, -33.416787], "type": "Point"}, "properties": {"sensor": 182, "time": "2022-01-11T15:26:16.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600903, -33.4168], "type": "Point"}, "properties": {"sensor": 2047, "time": "2022-01-11T15:26:20.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600945, -33.41684], "type": "Point"}, "properties": {"sensor": 667, "time": "2022-01-11T15:26:24.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601, -33.416863], "type": "Point"}, "properties": {"sensor": 661, "time": "2022-01-11T15:26:28.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60107, -33.416878], "type": "Point"}, "properties": {"sensor": 2587, "time": "2022-01-11T15:26:35.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601135, -33.416893], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:40.496"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601197, -33.416892], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:44.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601255, -33.416892], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:47.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601315, -33.4169], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:51.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601377, -33.416902], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:26:56.522"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60143, -33.416933], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:00.524"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601493, -33.416935], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:03.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601542, -33.416957], "type": "Point"}, "properties": {"sensor": 529, "time": "2022-01-11T15:27:06.520"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601592, -33.416975], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:09.516"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601648, -33.416987], "type": "Point"}, "properties": {"sensor": 2227, "time": "2022-01-11T15:27:14.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601712, -33.417005], "type": "Point"}, "properties": {"sensor": 9071, "time": "2022-01-11T15:27:18.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601768, -33.41701], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:21.521"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60183, -33.417003], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:25.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601885, -33.416968], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:29.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601943, -33.41697], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:33.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601997, -33.416963], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:38.520"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602048, -33.416923], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:42.487"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602093, -33.416893], "type": "Point"}, "properties": {"sensor": 9566, "time": "2022-01-11T15:27:45.505"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602128, -33.416857], "type": "Point"}, "properties": {"sensor": 722, "time": "2022-01-11T15:27:48.504"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602175, -33.41682], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:52.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602227, -33.416798], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:55.479"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602278, -33.416775], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:27:58.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602335, -33.416753], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:01.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602385, -33.41673], "type": "Point"}, "properties": {"sensor": 717, "time": "2022-01-11T15:28:05.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602438, -33.4167], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:10.540"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602487, -33.416663], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:14.483"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602535, -33.416628], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:18.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602585, -33.41661], "type": "Point"}, "properties": {"sensor": 10330, "time": "2022-01-11T15:28:22.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60265, -33.416598], "type": "Point"}, "properties": {"sensor": 2156, "time": "2022-01-11T15:28:26.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602708, -33.416592], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:30.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602762, -33.416565], "type": "Point"}, "properties": {"sensor": 2629, "time": "2022-01-11T15:28:35.494"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60281, -33.41654], "type": "Point"}, "properties": {"sensor": 796, "time": "2022-01-11T15:28:38.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602863, -33.416523], "type": "Point"}, "properties": {"sensor": 682, "time": "2022-01-11T15:28:41.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602932, -33.41652], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:28:44.535"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603005, -33.416518], "type": "Point"}, "properties": {"sensor": 10830, "time": "2022-01-11T15:28:47.476"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603073, -33.416513], "type": "Point"}, "properties": {"sensor": 702, "time": "2022-01-11T15:28:50.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603133, -33.416505], "type": "Point"}, "properties": {"sensor": 579, "time": "2022-01-11T15:28:53.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603188, -33.416488], "type": "Point"}, "properties": {"sensor": 2253, "time": "2022-01-11T15:28:56.492"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603243, -33.416475], "type": "Point"}, "properties": {"sensor": 741, "time": "2022-01-11T15:28:59.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603305, -33.416453], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:02.542"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60337, -33.416433], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:05.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603423, -33.416418], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:08.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603478, -33.41641], "type": "Point"}, "properties": {"sensor": 669, "time": "2022-01-11T15:29:12.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603543, -33.4164], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:18.523"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603577, -33.416363], "type": "Point"}, "properties": {"sensor": 642, "time": "2022-01-11T15:29:22.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603633, -33.416343], "type": "Point"}, "properties": {"sensor": 540, "time": "2022-01-11T15:29:26.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60369, -33.416323], "type": "Point"}, "properties": {"sensor": 2158, "time": "2022-01-11T15:29:30.525"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603748, -33.416305], "type": "Point"}, "properties": {"sensor": 615, "time": "2022-01-11T15:29:33.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603803, -33.416275], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:37.526"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603875, -33.416268], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:41.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603937, -33.416248], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:45.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603993, -33.41627], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:29:50.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60404, -33.416303], "type": "Point"}, "properties": {"sensor": 11669, "time": "2022-01-11T15:29:55.493"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604095, -33.41632], "type": "Point"}, "properties": {"sensor": 732, "time": "2022-01-11T15:30:00.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604147, -33.416305], "type": "Point"}, "properties": {"sensor": 588, "time": "2022-01-11T15:30:10.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604197, -33.41634], "type": "Point"}, "properties": {"sensor": 2362, "time": "2022-01-11T15:30:17.506"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60423, -33.416377], "type": "Point"}, "properties": {"sensor": 724, "time": "2022-01-11T15:30:22.513"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604282, -33.41642], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:27.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60432, -33.416452], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:30.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604363, -33.416492], "type": "Point"}, "properties": {"sensor": 10934, "time": "2022-01-11T15:30:35.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604402, -33.416542], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:39.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604432, -33.416592], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:43.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604467, -33.416627], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:46.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.6045, -33.416673], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:50.526"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604543, -33.416718], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:55.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604577, -33.416767], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:30:59.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604612, -33.416803], "type": "Point"}, "properties": {"sensor": 506, "time": "2022-01-11T15:31:03.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604673, -33.416833], "type": "Point"}, "properties": {"sensor": 579, "time": "2022-01-11T15:31:07.522"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604733, -33.416863], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:31:12.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604763, -33.416902], "type": "Point"}, "properties": {"sensor": 18443, "time": "2022-01-11T15:31:16.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60482, -33.416895], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:32:28.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604872, -33.416882], "type": "Point"}, "properties": {"sensor": 10497, "time": "2022-01-11T15:32:31.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604925, -33.416905], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:32:54.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60495, -33.416948], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:32:57.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604982, -33.417], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:01.536"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605017, -33.417047], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:05.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605052, -33.417097], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:09.535"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605085, -33.417148], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:13.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605123, -33.417193], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:17.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605145, -33.417247], "type": "Point"}, "properties": {"sensor": 18443, "time": "2022-01-11T15:33:21.499"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605173, -33.417292], "type": "Point"}, "properties": {"sensor": 12294, "time": "2022-01-11T15:33:25.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605197, -33.417342], "type": "Point"}, "properties": {"sensor": 9587, "time": "2022-01-11T15:33:30.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605217, -33.417387], "type": "Point"}, "properties": {"sensor": 515, "time": "2022-01-11T15:33:34.524"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60524, -33.417433], "type": "Point"}, "properties": {"sensor": 620, "time": "2022-01-11T15:33:39.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605258, -33.417478], "type": "Point"}, "properties": {"sensor": 259, "time": "2022-01-11T15:33:45.532"}, "type": "Feature"}], "type": "FeatureCollection"}

