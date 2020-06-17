import os
import sys

BASE = os.path.dirname(os.path.realpath(sys.argv[0]))
RESOURCES = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "resources/")
src = ""

def init(config):
    global src
    src = os.path.join(RESOURCES,config['file'])

def get():
    global src
    return get_tweets(src)

def get_tweets(file_path):
    '''
    Get list of Tweets from file path
    :param file_path: file path where tweets are stored
    :return: list of tweets
    '''
    try:
        with open(file_path, 'r') as file:
            #Split tweets by ';'
            lines = file.read().split(";")
    except:
        raise Exception("File Error: Failed to read '%s'" % file_path)
    tweet_list = []
    for line in lines:
        #Remove newline characters from return key
        str = line.lstrip()
        if str is not "":
            tweet_list.append(str)
    return tweet_list

