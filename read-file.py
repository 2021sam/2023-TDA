import time, json
file_name = 'message4.json'

with open(file_name) as f:
    json_content = json.load(f)
    # print(json_content)
    print( len( json_content ))
    for e in json_content:
        print( e.keys() )
        if 'data' in e.keys():
            data = e['data'][0]
            print( data.keys() )
            time.sleep(3)
