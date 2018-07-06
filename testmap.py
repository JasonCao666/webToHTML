from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import math
from osgeo import ogr, osr
import matplotlib.cm as cmx
import matplotlib.colors as colors

def createCircleAroundWithRadius(lat, lon, radiusMiles):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    latArray = []
    lonArray = []

    for brng in range(0,360):
        lat2, lon2 = getLocation(lat,lon,brng,radiusMiles)
        latArray.append(lat2)
        lonArray.append(lon2)
    return lonArray,latArray


def getLocation(lat1, lon1, brng, distanceMiles):
    lat1 = lat1 * math.pi/ 180.0
    lon1 = lon1 * math.pi / 180.0
            #earth radius
            #R = 6378.1Km
            #R = ~ 3959 Miles
    R = 3959
    distanceMiles = distanceMiles/R
    brng = (brng / 90)* math.pi / 2
    lat2 = math.asin(math.sin(lat1) * math.cos(distanceMiles)+ math.cos(lat1) * math.sin(distanceMiles) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(distanceMiles)* math.cos(lat1),math.cos(distanceMiles)-math.sin(lat1)*math.sin(lat2))
    lon2 = 180.0 * lon2/ math.pi
    lat2 = 180.0 * lat2/ math.pi
    return lat2, lon2

westbounds = -105.053514
eastbounds = -95.30829
northbounds = 44.001707
southbounds = 39.999932
fig = plt.figure(1)

#merc basemap, center on specified lat and lon, and zoom to bounds
mp = Basemap(projection='merc', lat_0 = 44, lon_0 = -105, ax=fig.gca(),
             resolution = 'h', area_thresh = 0.1,
             llcrnrlon=westbounds, llcrnrlat=southbounds,
             urcrnrlon=eastbounds, urcrnrlat=northbounds)

mp.drawstates()
mp.drawcounties()
memorialStaduimLat = 40.820485
memorialStadiumLon = -96.705588
distanceInMiles = 50

#color radius green - seems like a fine color
c = 'g'

# retrieve X and Y radius values using memorial stadium as center point, draw 50 miles out
X,Y = createCircleAroundWithRadius(memorialStaduimLat,memorialStadiumLon,distanceInMiles)
X,Y = mp(X,Y)
mp.plot(X,Y,marker=None,color=c,linewidth=2)

x,y = mp(memorialStadiumLon,memorialStaduimLat)
mp.plot(x,y ,marker='D',color=c,markersize=4)


plt.show()

