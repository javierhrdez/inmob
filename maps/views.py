from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import json
import geopandas as gpd
from shapely.geometry import Point
import geojson as gj

# Create your views here.



#def index(request):
#    return HttpResponse("Sitio funcionando...")

def index(request):
    #question_list = Question.objects.all()
    context = {'question_list': 'hola'}
    return render(request, 'index.html', context)

def ageb(request):
	conn = MongoClient()
	db = conn.metroscubicos
	col_ageb = db.ageb
	LON, LAT = 19.385422, -99.176435
	ageb = col_ageb.find_one({ "geometry": { "$geoIntersects": { "$geometry": { "type": "Point", "coordinates": [ LAT,LON] } } } })    
	#agebs = col_ageb.find()
	results = []
	#for ageb in agebs:
	#	results.append(ageb.get('geometry'))
	#print(ageb.get('geometry'))
	#application_name = request.GET.get('application_name')
	#szTransactionName = request.GET.get('szTransactionName')
	#hours = request.GET.get('hours')
	#tipo = request.GET.get('tipo')
	#periodos = request.GET.get('periodos')
	#datos = trending_data(application_name, szTransactionName, hours, tipo, periodos)
	datos = ageb.get('geometry')
	return HttpResponse(json.dumps(datos), content_type='application/json')


def geocoding(request):
	conn = MongoClient()
	db = conn.metroscubicos
	col_ageb = db.ageb
	LON, LAT = 19.385422, -99.176435
	ageb = col_ageb.find_one({ "geometry": { "$geoIntersects": { "$geometry": { "type": "Point", "coordinates": [ LAT,LON] } } } })    
	#agebs = col_ageb.find()
	results = []
	#for ageb in agebs:
	#	results.append(ageb.get('geometry'))
	#print(ageb.get('geometry'))
	#application_name = request.GET.get('application_name')
	#szTransactionName = request.GET.get('szTransactionName')
	#hours = request.GET.get('hours')
	#tipo = request.GET.get('tipo')
	#periodos = request.GET.get('periodos')
	#datos = trending_data(application_name, szTransactionName, hours, tipo, periodos)
	datos = ageb.get('geometry')
	return HttpResponse(json.dumps(datos), content_type='application/json')



def propiedades(request):
	LON, LAT = 19.385422, -99.176435
	LON, LAT = 19.410559,-99.1694129 # NUMA
	conn = MongoClient()
	db = conn.metroscubicos
	col_propiedades = db.propiedades
	propiedades = col_propiedades.find()

	features = []
	for propiedad in propiedades[1:10]:
		location = propiedad.get('location')
		lat = location.get('latitude')
		lon = location.get('longitude')
		price = propiedad.get('price')
		if lat and lon:
			my_feature = gj.Feature(geometry=gj.Point((lon, lat)), properties={"title": price})
			features.append(my_feature)
			#puntos.append(Point((lat,lon))) 

	feature_collection = gj.FeatureCollection(features)
	return HttpResponse(json.dumps(feature_collection), content_type='application/json')


def buffer(request):
	LON, LAT = 19.410559,-99.1694129 # NUMA
	RADIO  = 0.01
	p1 = Point((LAT,LON))
	gdf = gpd.GeoDataFrame( geometry = [p1])
	
	gdf['buffer'] = gdf.geometry.buffer(RADIO)
	print(gdf.head())
	print(gdf.geometry.buffer(100))
	b = gdf.iloc[0].buffer
	print(gpd.GeoSeries([b]).to_json())
	d = gpd.GeoSeries([b]).__geo_interface__
	print(type(d))
	#return HttpResponse(json.dumps(d.get('features')[0].get('geometry')), content_type='application/json')
	return HttpResponse(gpd.GeoSeries([b]).to_json(), content_type='application/json')
