'''This version of the remove duplicate tool was built to be compatible on mac os. It is a work around that does not
use the Tkinter module'''
'''Csv files must be in the same folder, with a main spreadsheet named 'master.csv' '''
'''Run in Python3'''

'''Import modules.'''
import csv
import codecs #Fixes encoding issue with spreadsheet data
import os
import sys
import datetime

'''Initialize global variables for counting records/script statistics.'''
master_count = 0
duplicate_files_count = 0
file_paths = os.listdir('/Users/primaryuser/Desktop/RemoveDuplicateStaging') #directory to the folder holding all the csv files
duplicate_ids = [] #Initialize variable to store desired ids to check for duplicates.
duplicate_queries = []
output_count = 0
empty_query = 0
invalid_country = 0
passed_validation = 0
empty_coordinates = 0
duplicate_ids_output_count = 0
duplicate_queries_output_count = 0
today = datetime.date.today()
output_filename = 'output_' + str(today) + '.csv'
duplicate_output_filename = 'duplicate_ids_output_' + str(today) + '.csv'
sd_output_filename = 'invalid_subdivision_' + str(today) + '.csv'
uq_output_filename = 'empty_query_' + str(today) + '.csv'
latlong_output_filename = 'empty_latlong_' + str(today) + '.csv'
duplicate_queries_output_filename = 'duplicate_queries_output_' + str(today) + '.csv'

'''This function is a filter that returns false if the ticket does not meet the data requirements for the project.'''
def testInvalid(sd_code, user_query, lat, long, id): #accepts a dictionary reader object, which should be the master csv
    if id in duplicate_ids:
        duplicate_output_writer.writerow(row)
        global duplicate_ids_output_count
        duplicate_ids_output_count += 1
        return False
    elif user_query in duplicate_queries: #Checks if the user query of the current row is already in the output file
        duplicate_queries_output_writer.writerow(row)
        duplicate_queries.append(user_query)
        global duplicate_queries_output_count
        duplicate_queries_output_count += 1
        return False
    elif sd_code == "PR" or sd_code == "VI" or sd_code == "GU": #if the subdivision code is GU, PR, or VI
        #print('Failed subdivision code.')
        global invalid_country
        sd_output_writer.writerow(row)
        invalid_country += 1
        return False
    elif user_query in (None, ''): #If the user query cell is null/empty
        #print('Empty User Query.')
        uq_output_writer.writerow(row)
        global empty_query
        empty_query += 1
        return False
    elif lat in (None, '') or long in (None, ''): #If the suggested lat/long is empty
        global empty_coordinates
        latlong_output_writer.writerow(row)
        empty_coordinates += 1
        return False
    else:
        #print('Passed validation.')
        global passed_validation
        passed_validation += 1
        duplicate_queries.append(user_query)
        return True

'''Get the master file (i.e. the file that needs its duplicates removed). Initialize output files'''
with codecs.open(os.path.expanduser('/Users/primaryuser/Desktop/RemoveDuplicateStaging/master.csv'),  'r', encoding='utf-8-sig') as master_csv, codecs.open(output_filename, 'w', encoding = 'utf-8-sig') as output_csv, codecs.open(duplicate_output_filename, 'w', encoding = 'utf-8-sig') as duplicate_output_csv:  # creates output csv file and Creates output csv file of duplicate ids, Open input file
    master_reader = csv.DictReader(master_csv)  # Save input file as a csv object
    fieldnames = master_reader.fieldnames  # Grabs fieldnames from master list
    fieldnames.append('Suggested Lat/Long') #Add a lat/long column
    print('master.csv filed opened.')
    for csv_file in file_paths:  # for every file in the project folder
        if 'csv' in csv_file:  # if the name of the file has 'csv' in it
            csv_path = '/Users/primaryuser/Desktop/RemoveDuplicateStaging/' + csv_file #Create file path name
            if csv_file != 'master.csv':
                duplicate_files_count += 1
                print(csv_path + ' opened.')

                '''Get all IDs from duplicate reference sheets'''
                with codecs.open(os.path.expanduser(csv_path), 'r', encoding='utf-8-sig') as ref_csv:  # Open input file
                    ref_reader = csv.DictReader(ref_csv)  # Save input file as a csv object
                    for row in ref_reader:  # For each row in the input file, add the value of each Id
                        duplicate_ids.append(row['Id'])  # Add the id of that row to the duplicate_ids list
    print('Duplicate Ids collected.')
    output_writer = csv.DictWriter(output_csv, fieldnames = fieldnames)  # Initialize DictWriter object
    duplicate_output_writer = csv.DictWriter(duplicate_output_csv, fieldnames = fieldnames)  # Initialize DictWriter object
    print('Output file created.')
    output_writer.writeheader()  # Add fieldnames as headers
    print('Field names added.')

    '''Create output files in order to sort tickets into individual files based on invalid criteria'''
    with codecs.open(output_filename, 'r', encoding = 'utf-8-sig') as output_csv_read, codecs.open(sd_output_filename, 'w', encoding = 'utf-8-sig') as sd_output_csv, codecs.open(uq_output_filename, 'w', encoding = 'utf-8-sig') as uq_output_csv, codecs.open(latlong_output_filename, 'w', encoding = 'utf-8-sig') as latlong_output_csv, codecs.open(duplicate_queries_output_filename, 'w', encoding = 'utf-8-sig') as duplicate_queries_output_csv:
        output_reader = csv.DictReader(output_csv_read)
        sd_output_writer = csv.DictWriter(sd_output_csv, fieldnames = fieldnames)
        uq_output_writer = csv.DictWriter(uq_output_csv, fieldnames = fieldnames)
        latlong_output_writer = csv.DictWriter(latlong_output_csv, fieldnames = fieldnames)
        duplicate_queries_output_writer = csv.DictWriter(duplicate_queries_output_csv, fieldnames = fieldnames)

        '''Begin sorting process'''
        for row in master_reader: # For each row in the master list
            master_count += 1
            if testInvalid(row['Subdivision Code'], row['User Query'], row['Suggested Lat'], row['Suggested Long'], row['Id']):
                decLat = float(row['Suggested Lat']) / 10000000 #Temp variable for formatting cordinate into decimal
                decLong = float(row['Suggested Long']) / 10000000
                formattedCoords = str(decLat) + ' ' + str(decLong) #Creates a lat/long coordinate pair
                row['Suggested Lat/Long'] = formattedCoords #Assign coordinate
                row['Suggested Lat'] = decLat #Overwrite lat into decimal lat
                row['Suggested Long'] = decLong #Overwrite long into decimal long
                row['User Query'] = row['User Query'].replace('\\n',' ') #Resolve spacing issues and removes '\n'
                row['User Query'] = row['User Query'].replace(' ,',',')
                row['User Query'] = row['User Query'].replace(',',', ')
                #If the current id is not in the duplicate list, write that row to output csv
                output_writer.writerow(row) #write the current row into output file
                output_count += 1

print('Process complete.')

'''Report statistics in console'''
print('\n    Report:')
print('Date: ' + str(today))
print('Duplicate reference files submitted: ' + str(duplicate_files_count))
print('Master sheet rows: ' + str(master_count))
print('Output sheet rows: '+ str(output_count))
print('Invalid subdivision codes (PR, GU, VI): ' + str(invalid_country))
print('Empty user query: ' + str(empty_query))
print('Empty coordinates: ' + str(empty_coordinates))
print('Duplicates Ids removed: ' + str(duplicate_ids_output_count))
print('Duplicates user queries removed: ' + str(duplicate_queries_output_count))

'''Write statistics to output report file'''
with codecs.open('output_report_' + str(today) + '.csv', 'w', encoding = 'utf-8-sig') as output_report:
    report_fieldnames = ['Raw Export', 'Tickets From Previous Requests', 'Invalid Subdivision', 'Empty User Query', 'Empty Coordinates', 'Duplicate User Query', 'Invalid Query', 'No Email', 'Final Output Total']
    output_report_writer = csv.DictWriter(output_report, fieldnames = report_fieldnames)
    output_report_writer.writeheader()
    output_report_writer.writerow({'Raw Export':master_count, 'Tickets From Previous Requests':duplicate_ids_output_count, 'Invalid Subdivision':invalid_country, 'Empty User Query':empty_query, 'Empty Coordinates':empty_coordinates, 'Duplicate User Query':duplicate_queries_output_count, 'Invalid Query':0, 'No Email':0, 'Final Output Total':0})
