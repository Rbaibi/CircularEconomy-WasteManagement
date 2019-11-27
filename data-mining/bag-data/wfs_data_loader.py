import pandas as pd
import geopandas as gpd
import requests
import json


def get_total_features(url, params):
    r = requests.get(url=url, params=params)
    data = r.json()
    for key, _ in data.items():
        print(key)
    return data['totalFeatures']


def get_features(url, params, total_features, data_dir='data/'):
    batch_size = params['count']
    start_index = params['startIndex']

    niter = total_features // batch_size
    print('number of iterations:{}'.format(niter))

    for i in range(start_index, niter + 1):
        print('iteration {}'.format(i))
        # retrieve data
        r = requests.get(url=url, params=params)
        data = r.json()

        # write data to file
        filename = 'data_' + str(i) + '.json'

        print('writing file to:{}{}'.format(data_dir, filename))
        with open(data_dir + filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        start_index += batch_size
        params['startIndex'] = start_index
