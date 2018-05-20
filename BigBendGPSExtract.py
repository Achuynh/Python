from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import csv


'''Initialize spreadsheet, prepare columns (filename, latitude, longitude, time).'''
with open('photo_metadata.csv', 'wb') as f:
    fieldNames = ['Name','Date', 'Time', 'Latitude', 'Longitude', 'Photo']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()

    '''For photo in the Big Bend file, get the metadata and convert GPS coordinates to minutes, degrees seconds'''
    for photo in os.listdir('C:\Users\erg\Desktop\Python_Projects\Big_Bend_Geotagged_All\\'):
        im = Image.open('C:\Users\erg\Desktop\Python_Projects\Big_Bend_Geotagged_All\\' + photo)
        info = im._getexif()

        '''Initialize variables for metadata'''
        GPSDict = {}
        dateTime = ''
        date = ''
        time = ''
        resolutionX = 0
        resolutionY = 0

        '''' Grab all EXIF tags. '''
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            '''Get timestamp, DateTimeOriginal 36867 and split'''
            dateTime = info[36867]
            date, time = dateTime.split(' ')
            '''If the tag is GPS information, convert to DMS format'''
            if decoded == 'GPSInfo':
                print decoded, tag, value, photo
                for key in info[tag].keys():
                    GPStag = GPSTAGS.get(key, key)
                    GPSDict[GPStag] = info[tag][key]
                '''GPS coordinates are in degrees, minutes, seconds.
                Exif stores coordinates as 'rational64u'. The format is as shown: (degreesNumerator, degreesDenominator), (minutesNumerator,
                minutesDenominator), (secondsNumerator,secondsDenominator)'''

                longD = GPSDict['GPSLongitude'][0][0] / GPSDict['GPSLongitude'][0][1]
                longM = GPSDict['GPSLongitude'][1][0] / GPSDict['GPSLongitude'][1][1]
                longS = GPSDict['GPSLongitude'][2][0] / GPSDict['GPSLongitude'][2][1]

                latD = GPSDict['GPSLatitude'][0][0] / GPSDict['GPSLatitude'][0][1]
                latM = GPSDict['GPSLatitude'][1][0] / GPSDict['GPSLatitude'][1][1]
                latS = GPSDict['GPSLatitude'][2][0] / GPSDict['GPSLatitude'][2][1]

                '''To convert to a single decimal number: Degrees + minutes/60 + seconds/3600'''
                GPSLong = longD + (longM / 60.0) + (longS / 3600.0)
                GPSLat = latD + (latM / 60.0) + (latS / 3600.0)

                '''Write to spreadsheet'''
                writer.writerow({'Name': photo, 'Date': date, 'Time': time, 'Latitude': GPSLat, 'Longitude': -GPSLong, 'Photo': im})

