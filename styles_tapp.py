import os
import json
import requests
import itertools
import singer


def mainData(i):
    url = "https://fixd-vehicles-api.herokuapp.com/api/styles?page=" + str(i)

    payload = {}
    headers = {
        'Authorization': 'Bearer TpWjxqm5ev9nlXjbFxPTqw'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    x = response.json()
    return x['data'], x['status']

def getAllData():
    i = 1
    d = []
    keyList = ['make_name', 'model_name', 'year', 'trim','cylinder', 'squish_vins']
    while i:
        data, status = mainData(i)
        #print(len(data))
        if status == 'NONE_FOUND':
            break
        for j in range(0, len(data)):
            tempDict = {your_key: data[j][your_key] for your_key in keyList}
            #print(tempDict)
            for k in range(len(tempDict['squish_vins'])):
                temp = {your_key: data[j][your_key] for your_key in keyList[:-1]}

                temp['sq_vins'] = tempDict['squish_vins'][k]

                d.append(temp)
            #print(d)
        #print("checking for page iteration: ", i)
        i += 1
    #print(len(d))

    return singer.write_records(stream_name="styles",records=d)


if __name__ == "__main__":
    schema = {'properties': {
        'make_name': {'type': ['string','null']},
        'model_name': {'type': ['string','null']},
        'year': {'type': ['integer','null']},
        'trim': {'type': ['string','null']},
        'cylinder' : {'type':['integer','null']},
        'sq_vins': {'type': ['string','null']}}}
    singer.write_schema(stream_name="styles", schema=schema, key_properties=[])
    d = getAllData()
    #print(d)
    #print("Came out of the loop")
    #fullDict=list(itertools.chain(*d))
    #print(len(fullDict))
    #print(fullDict)


