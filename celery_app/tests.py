import os,json
with open(os.path.join(os.path.dirname(__file__),"city_code.json"),"r") as f:
    city_infos = json.load(f)
