from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import glob

def DMS2Decimal(degree, min, sec, i):
    # Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
    DD = degree + (min/60.0) + (sec/3600.0)
    if i=='W':
        DD = DD * -1
    return DD

def readGPS(img):
    info = img._getexif()
    latitude = 0
    longitude = 0
    if info:
        for tag, value in info.items():
            name = TAGS.get(tag)
            if name == "GPSInfo":
                # calculate the latitude
                i = value[1]
                d=float(value[2][0][0])/float(value[2][0][1])
                m=float(value[2][1][0])/float(value[2][1][1])
                s=float(value[2][2][0])/float(value[2][2][1])
                latitude=DMS2Decimal(d,m,s,i)
                # calculate the longitude
                i = value[3]
                d=float(value[4][0][0])/float(value[4][0][1])
                m=float(value[4][1][0])/float(value[4][1][1])
                s=float(value[4][2][0])/float(value[4][2][1])
                longitude=DMS2Decimal(d,m,s,i)
    else:
        pass
    return latitude, longitude

def write2json(listGPS):
    print '{'
    print '\t\"geo\":['
    coord=listGPS.values()
    for gps in coord:
        print '\t{'
        print '\t\t\"lat\":',gps[0],','
        print '\t\t\"lng\":',gps[1]
        print '\t},'
    print '\t]'
    print '}'


if __name__=='__main__':

    files = glob.glob("D://your_directory/*.jpg")
    imagesGPS={}
    n = 0
    # read GPS from image and record the GPS location in a array
    for f in files:
        # print f
        image = Image.open(f)
        lat, lng = readGPS(image)
        if lat!=0 and lng!=0:  # remove the no GPS info pictures
            imagesGPS[n] = [lat, lng]
            n=n+1

    write2json(imagesGPS)
