from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import json
import geopandas as gpd
from shapely.geometry import Point, shape
import geojson as gj
import googlemaps
import pprint

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
	agebs = col_ageb.find()
	results = []
	for ageb in agebs:
		results.append(ageb.get('geometry'))
	return HttpResponse(json.dumps(results), content_type='application/json')


def geocoding(request):
	address = request.GET.get('address')
	print("address received:", address)
	API_KEY = 'XXXXXXXXXXXXX'
	gmaps = googlemaps.Client(key=API_KEY)
	# Geocoding an address
	# address : 'Pennsylvania 272, Colonia Nápoles, Ciudad de México'
	geocode_result = gmaps.geocode(address)
	pprint.pprint(geocode_result)
	res = geocode_result[0].get('geometry').get('location')
	lat, lon  = res.get('lat'), res.get('lng')
	print(lat,lon)
	return HttpResponse(json.dumps({"lat":lat,"lon":lon}), content_type='application/json')



def XXXXpropiedades(request):
	LON, LAT = 19.385422, -99.176435
	LON, LAT = 19.410559,-99.1694129 # NUMA
	conn = MongoClient()
	db = conn.metroscubicos
	col_propiedades = db.propiedades
	propiedades = col_propiedades.find()

	features = []
	for propiedad in propiedades[1:50]:
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


def propiedades(request):
	LON, LAT = 19.385422, -99.176435
	LON, LAT = 19.410559,-99.1694129 # NUMA
	conn = MongoClient()
	db = conn.metroscubicos
	col_propiedades = db.propiedades
	propiedades = col_propiedades.find()

	features = []
	for propiedad in propiedades[1:50]:
		location = propiedad.get('location')
		lat = location.get('latitude')
		lon = location.get('longitude')
		price = propiedad.get('price')
		if lat and lon:
			my_feature = gj.Feature(geometry=gj.Point((lon, lat)), properties={"title": price})
			features.append(my_feature)
			#my_feature =gj.Point((lon, lat))
			features.append(my_feature)
			#puntos.append(Point((lat,lon))) 

	feature_collection = gj.FeatureCollection(features)
	return HttpResponse(json.dumps(feature_collection), content_type='application/json')
	#return HttpResponse(json.dumps(features), content_type='application/json')

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


def ageb_buffer(request):
	lat = float(request.GET.get('lat'))
	lon = float(request.GET.get('lon'))
	print(lat,lon)
	#LON, LAT = 19.410559,-99.1694129 # NUMA
	RADIO  = 0.00500 # 250 mts
	# calcula buffer alrededor de un punto (LAT,LON), usando r = RADIO
	gdf = gpd.GeoDataFrame([{'geometry': Point(lon, lat).buffer(RADIO)}])
	# carga datos desde mongo
	conn = MongoClient()
	db = conn.metroscubicos
	col_ageb = db.ageb
	agebs = col_ageb.find()
	
	results = []
	gdf2 = gpd.GeoDataFrame( columns=['geometry'])
	for ageb in agebs:
		results.append(ageb.get('geometry'))
		gdf2 = gdf2.append({'geometry':shape(ageb.get('geometry'))[0]}, ignore_index=True)

	#calcula interseccion de poligonos ageb con buffer de r = RADIO y centro (LAT,LON)
	newdf = gpd.tools.overlay(gdf, gdf2, how="intersection")
	out = []
	for i in newdf['geometry']:
		out.append(i)
	return HttpResponse(gpd.GeoSeries(out).to_json(), content_type='application/json')



def propiedades_buffer(request):
	lat = float(request.GET.get('lat'))
	lon = float(request.GET.get('lon'))
	LON, LAT = 19.410559,-99.1694129 # NUMA
	RADIO  = 0.00500 # 500 mts
	# calcula buffer alrededor de un punto (LAT,LON), usando r = RADIO
	gdf = gpd.GeoDataFrame([{'geometry': Point(lon, lat).buffer(RADIO)}])

	conn = MongoClient()
	db = conn.metroscubicos
	col_propiedades = db.propiedades
	propiedades = col_propiedades.find()

	features = []
	for propiedad in propiedades[1:50]:
		location = propiedad.get('location')
		lat = location.get('latitude')
		lon = location.get('longitude')
		price = propiedad.get('price')
		if lat and lon:
			b = gdf.iloc[0].geometry
			p = Point((lat,lon))
			gdf_point = gpd.GeoDataFrame([{'geometry': Point(lon, lat)}])
			if gdf_point.iloc[0].geometry.within(b):
				print(gdf_point.iloc[0].geometry.within(b))
				my_feature = gj.Feature(geometry=gj.Point((lon, lat)), properties={"precio": price, "precio_ref": price})
				features.append(my_feature)
			#puntos.append(Point((lat,lon))) 

	feature_collection = gj.FeatureCollection(features)
	return HttpResponse(json.dumps(feature_collection), content_type='application/json')


def XXXpropiedades_buffer(request):
	lat = float(request.GET.get('lat'))
	lon = float(request.GET.get('lon'))
	LON, LAT = 19.410559,-99.1694129 # NUMA
	RADIO  = 0.00500 # 500 mts
	# calcula buffer alrededor de un punto (LAT,LON), usando r = RADIO
	gdf = gpd.GeoDataFrame([{'geometry': Point(lon, lat).buffer(RADIO)}])

	conn = MongoClient()
	db = conn.metroscubicos
	col_propiedades = db.propiedades
	propiedades = col_propiedades.find()

	features = []
	for propiedad in propiedades[1:50]:
		location = propiedad.get('location')
		lat = location.get('latitude')
		lon = location.get('longitude')
		price = propiedad.get('price')
		if lat and lon:
			b = gdf.iloc[0].geometry
			p = Point((lat,lon))
			gdf_point = gpd.GeoDataFrame([{'geometry': Point(lon, lat)}])
			if gdf_point.iloc[0].geometry.within(b):
				print(gdf_point.iloc[0].geometry.within(b))
				#my_feature = gj.Feature(geometry=gj.Point((lon, lat)), properties={"title": price})
				#features.append(my_feature)
				my_feature = gj.Point((lon, lat))
				features.append(my_feature)
			#puntos.append(Point((lat,lon))) 

	feature_collection = gj.FeatureCollection(features)
	#return HttpResponse(json.dumps(feature_collection), content_type='application/json')
	return HttpResponse(json.dumps(features), content_type='application/json')