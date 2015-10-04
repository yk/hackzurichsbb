__author__ = 'yk'

import requests
import urllib

RDF_REPOSITORY = 'Test'
SPARQL_ENDPOINT = "http://130.211.166.43/openrdf-sesame/repositories/%s" % RDF_REPOSITORY


def send_query(query):
    params = { 'query': query }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/sparql-results+json'
    }

    return requests.post(SPARQL_ENDPOINT, urllib.parse.urlencode(params), headers=headers)


def get_all_types():
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?x WHERE {?t rdf:type ?x}
    """
    return send_query(query)

def get_prefixes(): 
    return """
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX schema: <http://schema.org/>
		PREFIX sbb: <http://schema.sbb.ch/>
		PREFIX sbbdata: <http://data.sbb.ch/>
            """


def get_station(stationId):
		query = """
                    %s
		    SELECT ?y ?x WHERE {  
                        ?y sbb:agencyId "%s"^^xsd:int .
			?x sbbdata:stationid "%s" .
			?x schema:name ?name .
			?y rdfs:label ?name .
		    }
		""" % (get_prefixes(), stationId, stationId)
		return send_query(query)

def get_perrons(stationId):
		query = """
                    %s
                    SELECT ?agency ?code ?perro WHERE {  
                       ?agency sbb:agencyId "%s"^^xsd:int .
                       ?agency sbb:code ?code .
                       ?perro rdf:type schema:Perronkante .
                       ?perro sbb:code ?code
                }
		""" % (get_prefixes(), stationId)
		return send_query(query)


station_agency = {}

def get_station_agency(stationId):
                if stationId in station_agency:
                    return station_agency[stationId]

                query = """
                %s
                
                SELECT ?agency ?station ?equipment ?handicapped_accessible_counter ?handicapped_accessible_toilett 
                       ?help_wheelchair_mounting_Train ?mobilift ?stepless_access ?name ?code

                WHERE {
                        ?station sbbdata:stationid "%s" .
                        ?station rdf:type schema:TrainStation .
                        ?equipment sbbdata:station ?station .
                        ?equipment rdf:type sbbdata:Equipment . 
                                
                        ?equipment sbbdata:handicapped_accessible_counter ?handicapped_accessible_counter .
                        ?equipment sbbdata:handicapped_accessible_toilett ?handicapped_accessible_toilett .
                        ?equipment sbbdata:help_wheelchair_mounting_Train ?help_wheelchair_mounting_Train .
                        ?equipment sbbdata:mobilift ?mobilift .
                        ?equipment sbbdata:stepless_access ?stepless_access .
                                                                              
                        ?agency sbb:agencyId "%s"^^xsd:int . 
                        ?agency rdfs:label ?name .
                        ?agency sbb:code ?code .
                       }
                """ % (get_prefixes(), stationId, stationId)
                station_agency[stationId] = send_query(query)
                return station_agency[stationId]

perron = {}
def get_perron(stationId, gleisNr):
                key = stationId + gleisNr
                if key in perron:
                    return perron[key]

                query = """
                %s
              SELECT ?agency ?code ?perron ?PKH ?Hilfstritt ?Auftritt WHERE {
	        ?agency sbb:agencyId "%s"^^xsd:int .
		?agency sbb:code ?code .
		?perron sbb:code ?code .
		?perron rdf:type schema:Perronkante .
		?perron sbbdata:gleisNr "%s" .
		?perron sbbdata:Auftritt ?Auftritt .
		?perron sbbdata:Hilfstritt ?Hilfstritt .
		?perron sbbdata:PK-H ?PKH .
	      }
	    """ % (get_prefixes(), stationId, gleisNr)
                perron[key] = send_query(query)
                return perron[key]




if __name__ == '__main__':
	#print(get_all_types().text)
	#print(get_station("8500010").text)
	#print(get_perrons("8506000").text)
        print(get_station_agency("8506000").text)
	#print(get_perron("8506000", "1").text)
