import argparse
import json
import time
import os
import subprocess
import datetime
import sys
import codecs
import requests
from sys import platform

clientID = "xjjsgz3mrmduq7241fuuk724nnmgcq"
checkTime = 5

userName = ""
dot = 0
printDot = "."


def parse_args():
    desc = ("It will auto download stream when streamer start stream")
    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u", help="type username twitch.tv/username")
    parser.add_argument("-f", help="the folder where stream downloaded")
    args = parser.parse_args()
    return args


def get_id(user):
    status = 0
    data = None
    url = "https://api.twitch.tv/helix/users?login=" + user
    # for python 2.7
    request = requests.get(url, headers={"Client-ID": clientID})
    contents = request.json()
    id = None
    try:
        id = contents['data'][0]['id']
    except:
        print "get user error"
    return id


def check_user(user):
    # 0:offline #1:online #2:error
    status = 0
    data = None
    url = "https://api.twitch.tv/helix/streams?user_id=" + user
    contents = ''
    # for python 2.7
    try:
        request = requests.get(url, headers={"Client-ID": clientID})
        contents = request.json()
        if contents["data"] == []:
            status = 0
        else:
            status = 1
    except requests.ConnectionError as e:
        status = 0

    return status, contents


def check_followed():
    url = "https://api.twitch.tv/kraken/users/" + user + \
        "/follows/channels?oauth_token=4vr512upv97xdqfnpqa3sqe5o15vyl"


def check_loop(user):
    running = True
    while running:
        # user = "blusewilly_retry"
        status, data = check_user(user)
        global userName
        global dot
        global printDot

        # check foloder avilibile
        if(os.path.exists(location)):
            if(os.path.isdir(location) != True):
                status = 2
        else:
            status = 2

        if dot == 0:
            dot = dot + 1
        elif dot < 3 and dot != 0:
            printDot = printDot + "."
            dot = dot + 1
        else:
            dot = 0
            printDot = "."

        if status == 0:
            # for python 2.7
            print(userName + " offline, try after " +
                  str(checkTime) + " seconds" + printDot)
            time.sleep(checkTime)
        elif status == 1:
            # for python 2.7
            print(userName + " streaming, start download!")
            filename = userName + "-" + \
                datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss") + ".mp4"
            # print(filename)
            streamURL = "twitch.tv/" + userName

            if platform == "win32":
                # Windows version.
                print("windows mode")
                dir_path = os.path.dirname(os.path.realpath(__file__))
                filename = location + "\\" + filename
                subprocess.call([dir_path+"\\Streamlink_for_Windows_Portable_v1.0.0"+'\\Streamlink.exe',
                                 streamURL, 'best', '-o',  filename])

            elif platform == "linux" or platform == "linux2":
                # Linux version
                print("linux mode")
                filename = location + "/" + filename
                subprocess.call(["streamlink",
                                 streamURL, 'best', '-o',  filename])

            print("Download finished, start checking again. \n")
            time.sleep(checkTime)
        elif status == 2:
            print("The filepath or streamer name error, Please check. \n")
            running = False


print("Python version = ", sys.version_info[0])

user = parse_args().u
location = parse_args().f

# user = "zrush"
# location = "Z:\Stream"

if user == None:
    print("please '-u User' to input streamer")
elif location == None:
    print("please '-f Folder' to input downaload folder")
else:
    userName = user
    user_id = get_id(user)
    if user_id != None:
        check_loop(user_id)
    else:
        print("get user error")
