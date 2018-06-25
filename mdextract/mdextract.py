'''
mdextract.py
Used to get metadata from PIL image files
'''

from PIL.ExifTags import TAGS, GPSTAGS

class Mdextract:

    def __init__(self, exif_data):
        self.exif_data = exif_data

    #Returns a list of the decoded EXIF data. Accepts a image object's .get_exif().items() list, and a 'True'/'False'
    #for an option to print the list.
    def list_tag_names(self, list, print_flag):
        tag_list = []
        for tag, value in list:
            decoded = TAGS.get(tag, tag)
            tag_list.append((tag, value, decoded))
            if print_flag:
                print(tag, value, decoded)
        return tag_list
    #Enables the user to obtain metadata by tag number. Tag number can be found using the list_tag_names() method.
    def get_by_tag_num(self, tag_number):
        return self.exif_data[tag_number]

    #Returns a dictionary of GPS coordinates. User can overwrite the default tag number for GPSInfo.
    #GPS coordinates are in degrees, minutes, seconds.
    #Exif stores coordinates as 'rational64u'. The format is as shown: (degreesNumerator, degreesDenominator), (minutesNumerator,
    #minutesDenominator), (secondsNumerator,secondsDenominator)
    def get_gps_info(self, tag = 34853):
        temp = self.get_by_tag_num(tag)
        GPSDict = {}
        for key in temp.keys():
            GPStag = GPSTAGS.get(key, key)
            GPSDict[GPStag] = self.exif_data[tag][key]
        return GPSDict

    #Accepts a GPS dictionary stored by Exif as 'rational64u'. Converts the given dictionary into degrees, minutes, seconds.
    #Returns two variables, GPSlong, and GPSlat.
    def convert_dms(self, GPSDict):
        longD = GPSDict['GPSLongitude'][0][0] / GPSDict['GPSLongitude'][0][1]
        longM = GPSDict['GPSLongitude'][1][0] / GPSDict['GPSLongitude'][1][1]
        longS = GPSDict['GPSLongitude'][2][0] / GPSDict['GPSLongitude'][2][1]

        latD = GPSDict['GPSLatitude'][0][0] / GPSDict['GPSLatitude'][0][1]
        latM = GPSDict['GPSLatitude'][1][0] / GPSDict['GPSLatitude'][1][1]
        latS = GPSDict['GPSLatitude'][2][0] / GPSDict['GPSLatitude'][2][1]

        '''To convert to a single decimal number: Degrees + minutes/60 + seconds/3600'''
        GPSLong = longD + (longM / 60.0) + (longS / 3600.0)
        GPSLat = latD + (latM / 60.0) + (latS / 3600.0)
        return GPSLat, -GPSLong

