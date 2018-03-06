import argparse
# for python 3.x
import urllib.request

# for python 2.7
# import urllib2
import json
import time
import os
import subprocess
import datetime
import sys

clientID = "xjjsgz3mrmduq7241fuuk724nnmgcq"
checkTime = 5

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


def check_user(user):
    # 0:offline #1:online #2:error
    status = 0
    data = None
    url = "https://api.twitch.tv/kraken/streams/" + user

    # for python 3.x
    request = urllib.request.Request(url, headers={"Client-ID": clientID})
    opener = urllib.request.build_opener()
    contents = opener.open(request)
    data = json.load(contents)

    # for python 2.7
    # request = urllib2.Request(url, headers={"Client-ID": clientID})
    # contents = urllib2.urlopen(request).read()
    # data = json.loads(contents)
    
    if data["stream"] == None:
        status = 0
    else:
        status = 1

    return status, data


def check_followed():
    url = "https://api.twitch.tv/kraken/users/" + user + \
        "/follows/channels?oauth_token=4vr512upv97xdqfnpqa3sqe5o15vyl"


def check_loop(user):
    running = True
    while running:
        # user = "blusewilly_retry"
        status, data = check_user(user)
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
            # for python 3.x
            print(user, "offline, try after", checkTime,
                  "seconds"+printDot, end="\r")

            # for python 2.7
            # print(user, "offline, try after", checkTime,
            #       "seconds"+printDot+"      \r")
            time.sleep(checkTime)
        elif status == 1:
            # for python 3.x
            print(user, "streaming, start download!" + printDot, end="\n")

            # for python 2.7
            # print(user, "streaming, start download!" + printDot + "     \r")

            filename = user + "-" + datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss") + ".mp4"

            # print(filename)
            streamURL = "twitch.tv/" + user

            # Windows version.
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = location + "\\" + filename
            subprocess.call([dir_path+"\\Streamlink_for_Windows_Portable_v0.10.0"+'\\Streamlink.exe',
                             streamURL, 'best', '-o',  filename])

            # Linux version
            # filename = location + "/" + filename
            # subprocess.call(["streamlink",
            #                  streamURL, 'best', '-o',  filename])

            print("Download finished, start checking again. \n")
            time.sleep(checkTime)
        elif status == 2:
            print("The filepath or streamer name error, Please check. \n")
            running = False

print(sys.version)
user = parse_args().u
location = parse_args().f
check_loop(user)
