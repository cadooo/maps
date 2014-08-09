import BeautifulSoup
import re, json

UPPER = { "long": -119.5048, "lat": 49.9060}
LOWER = { "long": -119.4537, "lat": 49.8492}

f = open('gsmap.html','r')
soup = BeautifulSoup.BeautifulSoup(f)

out = dict()
out["type"] = "FeatureCollection"
out["features"] = list()

def getCDATA(txt):
  m = re.search('CDATA\[(.*?)\]',txt)
  if m:
    return m.group(1)

def geoFence(point):
  coord = point["geometry"]["coordinates"]
  if not float(coord[0]) > UPPER["long"]:
    return
  if not float(coord[0]) < LOWER["long"]: 
    return
  if not float(coord[1]) < UPPER["lat"]: 
    return
  if not float(coord[1]) > LOWER["lat"]:
    return
  out["features"].append(point)

for item in soup.findAll('row'):
  point = dict()
  point["type"] = "Feature"
  point["properties"] = dict()
  point["geometry"] = dict()
  point["geometry"]["type"] = "Point"

  coord = list() 
  #getCDATA(item.find('address').text)
  coord.append(getCDATA(item.find('long').text))
  coord.append(getCDATA(item.find('lat').text))
  point["geometry"]["coordinates"] = coord
  geoFence(point)

with open('gs.geojson', 'w') as outfile:
  json.dump(out,outfile)
