from wfs_data_loader import get_total_features,get_features

url = "https://geodata.nationaalgeoregister.nl/bag/wfs/v2_0"
bounding_box = '60000,430000,95000,460000'

get_one_params = {'request': 'GetFeature',
                  'service': 'WFS',
                  'version': '2.0.0',
                  'typeName': 'bag:pand',
                  'outputFormat': 'json',
                  'count': 1,
                  'startIndex': 0,
                  'bbox': bounding_box}

total_features = get_total_features(url, get_one_params)
print(total_features)

#TEST
#start_index = 693
start_index = 0

get_bulk_params = {'request': 'GetFeature',
                  'service': 'WFS',
                  'version': '2.0.0',
                  'typeName': 'bag:pand',
                  'outputFormat': 'json',
                  'count': 1000,
                  'startIndex': start_index,
                  'bbox': bounding_box}

get_features(url, get_bulk_params, total_features)

