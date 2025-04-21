'''
api.py

Flask Endpoint Design and Implementation Assignment for CS257
Author: Matvei Keshkekian

NAME: api.py - api endpoint exercise
SYNOPSIS: python3 api.py 
DESCRIPTION: 

'''
import argparse
import csv
import flask
import json
import sys


app = flask.Flask(__name__)

sources_file = '../data/sources.csv'
waves_file = '../data/waves.csv'

@app.route('/')
def hello():
    return 'Hello Tsunami researcher!'

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

@app.route('/tsunami/<country>/ids')
def get_tsunami_country(country):
    ''' Returrns all of the tsunami IDs in the territory of a country.'''
    tsunami_ids = []

    with open (sources_file) as f:
        reader = csv.reader(f)
        next(reader)
        for tsunami_row in reader:
            if tsunami_row[11].strip().lower() == country.lower():
                tsunami_ids.append(tsunami_row[0])

    return json.dumps({
        'country': country,
        'tsunami_ids': tsunami_ids })


@app.route('/tsunami/<country>/ids/years')
def get_tsunami_ids(country):
    '''Returns all of the tsunami ids in the terrritory of a country before or after certain year.'''
    before = flask.request.args.get('before', type=int)
    after = flask.request.args.get('after', type=int)

    if before is None and after is None:
        return 'Please supply ?before=YEAR and/or ?after=YEAR', 400
    
    tsunami_ids = []
    
    with open(sources_file) as f:
        reader = csv.reader(f)
        next(reader)
        for tsunami_row in reader:

            if tsunami_row[11].strip().lower() != country.lower():
                continue 

            try: 
                y = int(tsunami_row[1])
            except ValueError:
                continue

            if before is not None and y > before:
                continue
            if after is not None and y < after:
                continue   

            tsunami_ids.append(tsunami_row[0])

            # country = tsunami_row[11].strip()
            # if country not in tsunami_ids:
            #     tsunami_ids[country] = [tsunami_row[0]]
        
    
    return json.dumps({'country': country,
                    'before': before,
                    'after':  after,
                    'tsunami_ids': tsunami_ids})



@app.route('/tsunami/<country>/count/years')
def get_tsunami_num(country):
    ''' Returns the amount of tsunamis in the territory of a country between year X and Y, case-insensitively. '''
    before = flask.request.args.get('before', type=int)
    after = flask.request.args.get('after', type=int)

    if before is None and after is None:
        return 'Please supply ?before=YEAR and/or ?after=YEAR', 400
    
    tsunamis = 0
    country = country.strip().lower()

    with open(sources_file) as f:
        reader = csv.reader(f)
        next(reader)  
        for tsunami_row in reader:

            try:
                y = int(tsunami_row[1])
            except ValueError:
                continue

            if before is not None and y > before:
                continue
            if after is not None and y < after:
                continue  

            if tsunami_row[11].strip().lower() == country:
                tsunamis += 1

    return json.dumps({
        'country': country,
        'year1': after,
        'year2': before,
        'tsunami_count': tsunamis
    })


@app.route('/tsunami/<country>/damage')
def get_tsunami_damage(country):
    '''Returns the amount of millions of dollars damage caused by tsunamis in the territory of a country.'''
    dollars = 0

    with open(waves_file) as f:
        reader = csv.reader(f)
        next(reader)
        for tsunami_row in reader:
            if tsunami_row[6].strip().lower() == country.lower():

                dol = tsunami_row[24].strip()
                if not dol:
                    continue

                try:
                    dmg = float(dol.replace(',', ''))
                except ValueError:
                    continue

                dollars += dmg

    return json.dumps({'country': country, 
                    'damage_millions': dollars})
 

@app.route('/tsunami/years')
def get_tsunami_countries():
    '''Returns all of the countries that have had tsunamis either before or after certain year.'''
    before = flask.request.args.get('before', type=int)
    after = flask.request.args.get('after', type=int)

    if before is None and after is None:
        return 'Please supply ?before=YEAR and/or ?after=YEAR', 400
    
    countries = set()
    
    with open(sources_file) as f:
        reader = csv.reader(f)
        next(reader)
        for tsunami_row in reader:
            try:
                y = int(tsunami_row[1])
            except ValueError:
                continue

            if before is not None and y > before:
                continue
            if after  is not None and y < after:
                continue

            countries.add(tsunami_row[11].strip())

    return json.dumps({'before': before,
                    'after': after,
                    'countries': list(countries)})

   

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tsunami Flask API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

