import geopandas as gpd
import pandas as pd
from zipfile import ZipFile
import glob
import os

with ZipFile("/home/ec2-user/basins_num.zip", 'r') as zObject:
    # Extracting all the members of the zip
    # into a specific location.
    zObject.extractall(
        path="/home/ec2-user/contain_zip")

dir = "/home/ec2-user/contain_zip/content/basins/"

dir_gpkg = "/tdxhydro/*.*"

for file in glob.glob(dir_gpkg):
  num = file[-18:-8]
  points_dir = dir+num+".csv"
  points = pd.read_csv(points_dir)
  gdf = gpd.GeoDataFrame(points, geometry = gpd.points_from_xy(points['Lon'], points['Lat']))
  gdf = gdf.set_crs('EPSG:4326')
  gdf.reset_index(drop=True, inplace=True)
  geopackage = gpd.read_file(file)
  intersections = gpd.sjoin(gpd, geopackage, predicate='intersects')
  #this is the name of the csv that will be produced - idk what directory you will want it save to
  intersections.to_csv(f"{num}_with_stream.csv")