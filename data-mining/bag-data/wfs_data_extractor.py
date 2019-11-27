import os
import pandas as pd
import geopandas as gpd


def extract(status, data_dir='data/'):
    status_values = {'used': 'Pand in gebruik',
                     'used_not_measured': 'Pand in gebruik (niet ingemeten)',
                     'demolition_permit_granted': 'Sloopvergunning verleend',
                     'construction_started': 'Bouw gestart',
                     'construction_permit_granted': 'Bouwvergunning verleend',
                     'vacant': 'Pand buiten gebruik'}

    print(status_values[status])
    gdata = gpd.GeoDataFrame()
    file_list = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    for f in file_list:
        print(f)
        data = gpd.read_file(data_dir+f)
        if len(data.index) > 0:
            data = data[data['status'] == status_values[status]]
            gdata = pd.concat([gdata, data])

    return gdata


def write_shapefile(dataframe, filename, data_dir='data/shapefiles/'):
    if len(dataframe) == 0:
        print('dataframe is empty, nothing to write')
    else:
        dataframe.to_file(driver='ESRI Shapefile', filename=data_dir+filename)


gf = extract('demolition_permit_granted', data_dir='data/bag_pand_save/')
print(len(gf))
print(gf)
write_shapefile(gf, 'demolition_permit_granted')
