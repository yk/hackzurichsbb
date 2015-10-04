import random
import feedback
import dbapi
import json


train_info = {}


def get_handicap_for_number(number):
    if number == 0:
        return "unknown"
    if number == 1:
        return "none"
    if number == 2:
        return "assisted"
    if number == 3:
        return "restricted"
    if number == 4:
        return "full"

def get_handicap_for_string(string):
    if string == "unknown":
        return 0
    if string == "none":
        return 1
    if string == "assisted":
        return 2
    if string == "restricted":
        return 3
    if string == "full":
        return 4



def get_handicap_for_section(section):
    # if 'handicappedAccess' in section['arrival']:
    #     return get_handicap_for_number(int(section['arrival']['handicappedAccess']))
    # train = section['journey']['number']
    res = "unknown"

    res, pdflist = get_handicap_for_section_from_pdfs(res, section)
    res, deplist, arrlist = get_handicap_for_section_from_stations(res, section)

    return res, pdflist, deplist, arrlist


def get_handicap_for_section_from_pdfs(current_opinion, section):
    # if not yet initialized, do it now
    if not train_info:
        initialize_train_info()

    train = section['journey']['number']
    if train in train_info:
        current_opinion = train_info[train]

    pdflist = []
    if current_opinion == "full":
        pdflist = ["Train fully accessible."]
    elif current_opinion == "restricted":
        pdflist = ["Train accessible with minor inconveniences."]
    elif current_opinion == "assisted":
        pdflist = ["Registration requiered. Please contact SBB for futher details\n(0800 007 102)."]

    return current_opinion, pdflist


#returns (Int, List, List)
def get_handicap_for_section_from_stations(current_opinion, section):
    current_opinion_number = get_handicap_for_string(current_opinion)

    departure_station_id = section['departure']['station']['id'].lstrip("0")
    departure_plattform_nr = section['departure']['platform'] 
    arrival_station_id = section['arrival']['station']['id'].lstrip("0")
    arrival_plattform_nr = section['arrival']['platform']


    departure_opinion = get_handicap_station_perron(current_opinion_number, departure_station_id, departure_plattform_nr)
    arrival_opinion = get_handicap_station_perron(current_opinion_number, arrival_station_id, arrival_plattform_nr)

    if current_opinion_number < departure_opinion or current_opinion_number < arrival_opinion:
        if departure_opinion < arrival_opinion:
            current_opinion = get_handicap_for_number(departure_opinion)
        else:
            current_opinion = get_handicap_for_number(arrival_opinion)

    return current_opinion, get_description_for_station(departure_station_id) , get_description_for_station(arrival_station_id)


def initialize_train_info():
    print("initializing train info")
    f = open("parser/trainInfo.out", "r")
    for line in f:
        line = line.lower()
        trainId = line.split(" ")[0]
        if "full" in line or "bus" in line or "domino" in  line or "flirt" in line or "gtw seetal" in line or "lötschberger" in line or "nina" in line or "npz-jumbo" in line:
            res = "full"
        elif "restricted" in line or "bem 550" in line or "gtw thurbo" in line or "gtw bls" in line:
            res = "restricted"
        elif "assisted" in line or "ec" in line or "et 426" in line or "ew" in line or "etr 470" in line or "etr 610" in line or "ic2000" in line or "ice" in line or "icn" in line or "npz" in line or "railjet" in line or "revvivo" in line or "tgv lyria" in line or "vt 611" in line or "vt 628" in line:
            res = "assisted"
        else:
            res = "none"

        train_info[trainId] = res

def get_handicap_station_perron(current_opinion_number, stationId, plattformNr):

    if current_opinion_number < 3:
        #check if there is a lift 
        res = dbapi.get_station_agency(stationId)
        binding = json.loads(res.text)
        if 'help_wheelchair_mounting_Train' in binding and getValue(binding['help_wheelchair_mounting_Train']) == 1:
            current_opinion_number = 1

    #the following set it to restricted
    if current_opinion_number >= 4:
        res = dbapi.get_perron(stationId, plattformNr)
        resobj = json.loads(res.text)
        if (len(resobj['results']['bindings']) > 0):
            binding = resobj['results']['bindings'][0]
            if binding['Auftritt'] and getAuftrittScore(binding['Auftritt']) == 1:
                current_opinion_number = 4
            if binding['Hilfstritt'] and getHilfstrittScore(binding['Hilfstritt']) == 1:
                current_opinion_number = 4

    #when there is no steppless access set to assisted
    if current_opinion_number >= 3:
        res = dbapi.get_station_agency(stationId)
        resobj = json.loads(res.text)
        if (len(resobj['results']['bindings']) > 0):
            binding = resobj['results']['bindings'][0]
            if getValue(binding['stepless_access']) == 0: 
                current_opinion_number = 3

    return current_opinion_number


def get_description_for_station(stationId):
    res = dbapi.get_station_agency(stationId)
    resobj = json.loads(res.text)

    result = []
    if (len(resobj['results']['bindings']) > 0):
        binding = resobj['results']['bindings'][0]
        if 'handicapped_accessible_counter' in binding and getValue(binding['handicapped_accessible_counter']) == 1:
            result.append('It is easy to reach a counter.')
        if 'handicapped_accessible_toilett' in binding and getValue(binding['handicapped_accessible_toilett']) == 1:
            result.append('Handicapped accessible restrooms available.')
        if 'help_wheelchair_mounting_Train' in binding and getValue(binding['help_wheelchair_mounting_Train']) == 0:
            result.append('No wheelchair mounting train available.')
        if 'stepless_access' in binding and getValue(binding['stepless_access']) == 0:
            result.append('Unavoidable steps may be present.')

    return result

#def get_handicap_for_perron(stationId, plattformNr):
    #res = dbapi.get_perron(stationId, plattformNr)
    #resobj = json.loads(res.text)
    #result = 0;

    #binding = resobj['results']['bindings'][0]
    #if binding['Auftritt']: 
        #result += getAuftrittScore(binding['Auftritt'])     
    #if binding['Hilfstritt']: 
        #result += getHilfstrittScore(binding['Hilfstritt'])
    #if binding['PKH']: 
        #result += getPKHScore(binding['PKH'])
 
 
    #return result

def getValue(obj):
    if obj['value'] == '1':
        return 1
    else: 
        return 0

def getAuftrittScore(val):
    if val == "Kein":
        return 0
    elif val == "Beton":
        return 0
    elif val == "Gitterrost":
        return 1
    elif val == "Andere":
        return 1
    return 0

def getHilfstrittScore(val):
    if val == "nicht vorhanden":
        return 1
    else:
        return 0 

    return 0

def getPKHScore(val):
    if val == "<=P20":
        return 0
    elif val == "P25":
        return 0
    elif val == "P30":
        return 0
    elif val == "P35":
        return 0
    elif val == "P40":
        return 0
    elif val == "P42":
        return 0
    else: #P55
        return 0
    return 0

def annotate_connections(connections):
    for connection in connections:
        for section in connection['sections']:
            #feedback.annotate_section(section)
            hc, pdflist, deplist, arrlist = get_handicap_for_section(section)
            print("Train: " + section['journey']['number'] + " - " + hc)
            section['handicap'] = hc
            section['pdflist'] = pdflist
            section['deplist'] = deplist
            section['arrlist'] = arrlist


if __name__ == '__main__':
    #print(get_handicap_for_station("8506011"))
    print(get_handicap_for_perron("8506011", "1"))
