from PIL import Image
import os
import csv
import mdextract as md

'''Initialize spreadsheet, prepare columns (filename, latitude, longitude, time).'''
with open('photo_metadata.csv', 'w') as f:
    fieldNames = ['Name','Date', 'Time', 'Latitude', 'Longitude', 'Photo']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()

    '''For photo in the Big Bend file, get the metadata and convert GPS coordinates to minutes, degrees seconds'''
for photo in os.listdir('C:\\Users\\erg\\Desktop\\Python_Projects\\Big_Bend_Geotagged_Selected\\'):
        im = Image.open('C:\\Users\\erg\\Desktop\\Python_Projects\\Big_Bend_Geotagged_Selected\\' + photo)
        info = im._getexif()
        exiftrans = md.Mdextract(info)
        '''' Grab all EXIF tags. '''
        all_tags = exiftrans.list_tag_names(info.items(), False)
        '''Get timestamp, DateTimeOriginal 36867 and split'''
        dateTime = exiftrans.get_by_tag_num(36867)
        date, time = dateTime.split(' ')
        '''Get GPS info.'''
        gpsinfo = exiftrans.get_gps_info()
        '''Convert coordinates into dms'''
        lat, long = exiftrans.convert_dms(gpsinfo)
        writer.writerow({'Name': photo, 'Date': str(date), 'Time': time, 'Latitude': lat, 'Longitude': long, 'Photo': im})
