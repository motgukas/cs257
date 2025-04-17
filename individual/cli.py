'''
cli.py

Command Line Interface (CLI) Assignmnet for CS257
Author: Matvei Keshkekian

NAME: cli.py - command-line interface exercise
SYNOPSIS: python3 cli.py country year1 year2
DESCRIPTION: Shows the amount of tsunamis in the terrority of a country between year X and Y, case-insensitively.

'''
import argparse
import csv


def get_parsed_arguments():
     
    parser = argparse.ArgumentParser(description='Report on the tsunamis in all of the countries.')
    parser.add_argument('country', metavar='country', help='the country whose amount of tsunamis you seek')
    parser.add_argument('year1', metavar='year1', type=int, help='the first year of the range')
    parser.add_argument('year2', metavar='year2', type=int, help='the last year of the range')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def get_tsunamis(country, year1, year2):

    tsunamis = 0

    with open('../data/sources.csv') as f:
        reader = csv.reader(f)
        next(reader)  #
        for tsunami_row in reader:
            if tsunami_row[11].lower() == country.lower():
                try:
                    year = int(tsunami_row[1])
                    if year1 <= year <= year2:
                        tsunamis += 1                
                except ValueError:
                    bad = tsunami_row[1]
                    print(f"Invalid year field “{bad}” for {country}, skipping row.")
                    continue

    return tsunamis

def main():
    arguments = get_parsed_arguments()

    if arguments.year1 > arguments.year2:
        print(f'Error: year1 ({arguments.year1}) must be less than or equal to year2 ({arguments.year2}).')
        return

    country = arguments.country
    # for country in arguments.country:
    tsunami = get_tsunamis(country, arguments.year1, arguments.year2)

    if tsunami:
        print(f'There were {tsunami} tsunami that affected {country} between the years {arguments.year1} and {arguments.year2}.')  
    else:
        print(f'I don\'t know what the amount of tsunamis that affected {country} between the years {arguments.year1} and {arguments.year2} is.')

if __name__ == '__main__':
    main()