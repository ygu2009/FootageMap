from PIL import Image
from PIL.ExifTags import TAGS
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
                # print d, m, s, i, latitude

                # calculate the longitude
                i = value[3]
                d=float(value[4][0][0])/float(value[4][0][1])
                m=float(value[4][1][0])/float(value[4][1][1])
                s=float(value[4][2][0])/float(value[4][2][1])
                longitude=DMS2Decimal(d,m,s,i)
                # print d, m, s, i, longitude
    else:
        pass

    return latitude, longitude

def write2json(listGPS):
    w2file = open("./myData.json", "w")

    w2file.write('{\n')
    w2file.write('\t\"geo\":[\n')
    for ii in range(listGPS.__len__()-1):
        w2file.write('\t{\n')
        w2file.write('\t\t\"lat\": %f,\n' % listGPS[ii][0])
        w2file.write('\t\t\"lng\": %f\n' % listGPS[ii][1])
        w2file.write('\t},')

    # for the last location
    w2file.write('\t{\n')
    w2file.write('\t\t\"lat\": %f,\n' % listGPS[listGPS.__len__()-1][0])
    w2file.write('\t\t\"lng\": %f\n' % listGPS[listGPS.__len__()-1][1])
    w2file.write('\t}\n')

    w2file.write('\t]\n')
    w2file.write('}\n')

    w2file.close()


if __name__=='__main__':

    files = glob.glob("C://Users/Yingying/PycharmProjects/FootageMap/test/*.jpg")
    # files = glob.glob("D://entertainment/big/*.jpg")
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

    # combine the closed image
    imagesGPScc = []
    lat_p, lng_p = 0,0
    for item in imagesGPS.values():
        if abs(item[0]-lat_p)>0.01 or abs(item[1]-lng_p)>0.01:
            imagesGPScc.append([item[0], item[1]])

    write2json(imagesGPScc)