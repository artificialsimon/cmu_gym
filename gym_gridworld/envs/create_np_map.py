import os
import pickle
import numpy as np
from mapquery import terrain_request
from pathlib import Path

# map = pickle.load(open('050070.dict','rb'))
# top_left = (50,70)
# #make the volume
# vol = np.zeros((5,20,20))
# feature_value_map = {} #{[alt,feature]:value}
# value_feature_map = {} #{value:(alt,feature)}
# index = 1
# #alt_index = {0:1,1:1,2:1,3:1,4:1}
# for xy, feat in map.items():
#     if feat not in list(feature_value_map.keys()):
#         feature_value_map[feat] = index#alt_index[feat[0]]
#         value_feature_map[index] = feat
#         index+=1#alt_index[feat[0]] += 1
#
#     vol[feat[0],xy[0]-top_left[0],xy[1]-top_left[1]] = feature_value_map[feat]
#
#

def get_feature_value_maps(x,y,map):
    '''This will create, load, and expand a feature-> value dictionary and
    a value-> feature dictionary.
    Will return 2 dictionaries.'''
    feature_value_map = {}
    value_feature_map = {}
    #first check for existing feature maps
    feature_to_value = Path('features/features_to_values.dict')
    value_to_feature = Path('features/values_to_features.dict')

    if feature_to_value.is_file():
        feature_value_map = pickle.load(open(feature_to_value,'rb'))
    if value_to_feature.is_file():
        value_feature_map = pickle.load(open(value_to_feature, 'rb'))


    return (feature_value_map, value_feature_map)

def convert_map_to_volume_dict(x,y,map):
    return_dict = {}
    top_left = (x,y)
    feature_value_map = {}
    vol = np.zeros((5, 20, 20))
    flat = np.zeros((20,20))
    #load value maps: feature -> value and value -> feature
    #feature_value_map = {} #{[alt,feature]:value}
    #value_feature_map = {} #{value:(alt,feature)}
    feature_value_map,value_feature_map = get_feature_value_maps(x,y,map)
    value = 1
    for xy, feat in map.items():
        if feat[1] not in list(feature_value_map.keys()):
            feature_value_map[feat[1]] = {'val':value,'alt':feat[0]}
            value_feature_map[value] = {'feature':feat[1], 'alt':feat[0]}
            value += 1
        flat[xy[1]-top_left[1],xy[0]-top_left[0]] = feature_value_map[feat[1]]['val']
        #now, go through the layers and project the object downwards
        for i in range(feat[0],-1,-1):
            vol[i,xy[1]-top_left[1],xy[0]-top_left[0]] = feature_value_map[feat[1]]['val']

    # index = 1
    # alt_index = {0:1,1:1,2:1,3:1,4:1}
    # for xy, feat in map.items():
    #     if feat[1] not in list(feature_value_map.keys()):
    #         #the two maps should have an altitude index. {feature: {alt: value}} or {alt : {value : feature}}
    #         feature_value_map[feat[1]] = {feat[0]:alt_index[feat[0]]}
    #         #feature_value_map[feat] = alt_index[feat[0]]
    #         value_feature_map[feat[0]] = {alt_index[feat[0]]:feat[1]}
    #         #value_feature_map[alt_index[feat[0]]] = feat
    #         alt_index[feat[0]] += 1
    #
    #     vol[feat[0],xy[1]-top_left[1],xy[0]-top_left[0]] = feature_value_map[feat[1]][feat[0]]




    return_dict['feature_value_map'] = feature_value_map
    return_dict['value_feature_map'] = value_feature_map
    #save before returning
    #todo fix value_feature_map and feature_maps -> they should be the same (except inside out)
    print("saving value/feature maps")
    with open('features/features_to_values.dict', 'wb') as handle:
        pickle.dump(feature_value_map, handle)
    with open('features/values_to_features.dict', 'wb') as handle:
        pickle.dump(value_feature_map,handle)

    return_dict['vol'] = vol
    return_dict['flat'] = flat



    value = max(list(value_feature_map.keys())) + 1
    feature_value_map['hiker'] = {'val': value}
    value_feature_map[value] = {'feature': 'hiker'}
    value += 1
    #reserve spots for the drone at different altitudes
    feature_value_map['drone'] = {'val': value}
    value_feature_map[value] = {'feature': 'drone'}


    # for i in range(len(vol)):
    #     key_string = i#'alt{}'.format(i)
    #     if key_string not in return_dict:
    #         return_dict[key_string] = {}
    #         return_dict[key_string]['map'] = vol[i]
    #
    #     #what features are at that altitude?
    #     current_features = []
    #     for value,feature in value_feature_map.items():
    #         if feature[0] == i:
    #             current_features.append(feature[1])
    #
    #     current_features.append('drone')
    #     if i == 0:
    #         current_features.append('hiker')
    #
    #     for current_feature in current_features:
    #         return_dict[key_string][current_feature] = np.zeros((20,20))
    #
    #     non_zeros = np.transpose(vol[i].nonzero())
    #     for non_zero in non_zeros:
    #         feature = value_feature_map[vol[i][non_zero[0]][non_zero[1]]][1]
    #         #return_dict[key_string][feature][non_zero[0][non_zero[1]]] = 1.0
    #         return_dict[key_string][feature][non_zero[0],non_zero[1]] = 1.0
    #         #buil

    return return_dict


def map_to_volume_dict(x=0,y=0,width=5,height=5):
    #does the map already exist in the maps/ folder?
    return_dict = {}
    filename = '{}{}.mp'.format(x,y)
    maps = []
    map = 0
    for files in os.listdir('maps'):
        if files.endswith(".mp"):
            maps.append(files)
    #loops through because I'll need the actual map
    for files in maps:
        if filename == files:
            print("loading existing map.")
            map = pickle.load(open('maps/' + filename,'rb'))
    if not map:
        print("generating map")
        map = terrain_request(x,y,width,height)

        #store it for future use
        print("saving map.")
        with open('maps/' + filename, 'wb') as handle:
            pickle.dump(map, handle)
    #convert_map_to_volume_dict(x,y,map)
    return convert_map_to_volume_dict(x,y,map)

 #   return return_dict



#sample code
#a = map_to_volume_dict(70,50,20,20)
# f,v = get_feature_value_maps(300,200,a) #300,200
#print('complete.')