import requests 
import os
from datetime import datetime
from pprint import pprint
import json
import pandas as pd
import shutil

thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\"

#http://IP_ADDRESS:PORT + [/HTTP_ROOT] + /api/v2?apikey=$apikey&cmd=$command

def download_plex_img(api_endpoint, addon):
    filedir = r"D:\plex_imgs\\"
    if not os.path.exists(filedir + addon + ".png"):
        req = api_endpoint + "pms_image_proxy&rating_key=" + addon
        r = requests.get(req, stream=True)
        if r.status_code == 200:
            with open(filedir + addon + ".png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)        

def plex_get_home_stats(api_endpoint, save_df):
    req = api_endpoint + "get_home_stats"
    req = requests.get(req)
    output = json.loads(req.content)
    df_list = []
    for o in output['response']['data']:
        #for each row, download the image associated with the movie item
        for orow in o['rows']:
            if "rating_key" in orow.keys():
                download_plex_img(api_endpoint, str(orow['rating_key']))
        df = pd.DataFrame(o['rows'])
        df['stat_id'] = o['stat_id']
        if "stat_type" in o.keys():
            df['stat_type'] = o['stat_type']
        df_list.append(df)   
    df = pd.concat(df_list)
    df.to_csv(save_df)

if __name__ == "__main__":
    start_time = datetime.now()
    #gather credentials
    secrets = r"D:\Secrets\plex.txt"
    with open(secrets) as f:
        cred_list = f.read().split()
    #create api_endpoint starting place
    api_endpoint = cred_list[0] + "/api/v2?apikey=" + cred_list[1] + "&cmd="

    #available requests
    response_data = ["get_users", "get_user_names", "get_library_names"]
    other = ["pms_image_proxy"]

    # req = api_endpoint + multrows[0]
    # output = json.loads(req.content)
    #output = output['response']['data']
    #output = output['response']['data'][0]['rows']
    plex_get_home_stats(api_endpoint, "get_home_stats.csv")
    #print(df.head())


    print("--- %s seconds ---" % (datetime.now() - start_time))