# purpose: for all zipfiles in dir:
#   read shapefile
#   add year
#   transform CRS
#   save as geojson

# 2020-04-11
# richard.zijdeman@iisg.nl

# import libraries
import os
import geopandas
import zipfile
import shutil

# read zipfile
# nl17_unzipped = zipfile.ZipFile(data_path + 'nl_1917.zip').extractall()

# paths
nlgis_dir = '/Users/richardz/Dropbox/nlgis-json/'

# create temporary directory
temp_dir = 'temp-dir'
try:
    # Create target Directory
    os.mkdir(nlgis_dir + temp_dir)
    print("Directory" , nlgis_dir + temp_dir ,  "created.")
except FileExistsError:
    print("***Directory" , nlgis_dir + temp_dir ,  "already exists.***")

# create GeoJSON directory
geojson_dir = 'geojson-dir'
try:
    # Create target Directory
    os.mkdir(nlgis_dir + geojson_dir)
    print("Directory" , nlgis_dir + geojson_dir ,  "created.")
except FileExistsError:
    print("***Directory" , nlgis_dir + geojson_dir ,  "already exists.***")




# Create geojson
## Retrieve year from filename
for fname in os.listdir(nlgis_dir):
    if fname.endswith(".zip"):
        # get year from filename
        # split on '.' take first part; split on '-' take 2nd part
        year = fname.split('.')[0].split('_')[1]
        # unzip the file
        ftemp = zipfile.ZipFile(nlgis_dir+fname).extractall(nlgis_dir+temp_dir)
        print(year + '\n\tExtracted')

        #read the shapefile
        currentShape = geopandas.read_file(nlgis_dir+temp_dir+"/nl_"+year+".shp")

        #add column with year value to the shapefile
        currentShape['year'] = year
        print('\tYear column added')
        #change coordinate reference system of the shapefile
        currentShape = currentShape.to_crs("EPSG:4326")
        print('\tCRS set to WGS84')
        # write shapefile as GeoJSON
        currentShape.to_file(nlgis_dir+geojson_dir+"/nl_"+year+".geojson", driver='GeoJSON')
        print('\tGeoJSON written')
        # clean temporary directory after year-'run'
        # https://stackoverflow.com/questions/1995373/deleting-all-files-in-a-directory-with-python
        filelist = [ f for f in os.listdir(nlgis_dir+temp_dir) if f.startswith("nl_") ]
        for f in filelist:
            os.remove(os.path.join(nlgis_dir+temp_dir, f))

        continue
    else:
        continue

# after the final run, remove the  temp_dir altogether
os.rmdir(nlgis_dir+temp_dir)
print("Done!")
