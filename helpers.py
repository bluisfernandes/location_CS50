import random



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

from geojson import Feature, Point, MultiPoint, FeatureCollection

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

print("hello")


def geojson_rdm_points(n =100):
    long1= -33.4051268999
    long2 = -33.5042356
    lat1 = -70.505497
    lat2 = -70.8000687
    latx = (lat1+lat2)/2
    longx=(long1+long2)/2

    areafeature=[]
    for i in range(n):
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat1,latx,long1,longx)[0]), properties={"area":1, "color":random.randrange(0, 25)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat2,latx,long1,longx)[0]), properties={"area":2, "color":random.randrange(25, 50)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat1,latx,long2,longx)[0]), properties={"area":3, "color":random.randrange(50, 75)}))
        areafeature.append(Feature(geometry=Point(coords_rdm(1,lat2,latx,long2,longx)[0]), properties={"area":4, "color":random.randrange(75, 100)}))

    geojson  = FeatureCollection(areafeature)

    return geojson