import json
from urlparse import urlparse
import urllib
import urllib2
import json
import ast
import requests
import warnings
from googleapiclient.discovery import build

warnings.filterwarnings("ignore")

class YoutubeAPI:
    youtube_key = "AIzaSyDQVlmu0vVKoKP_4dKfmOFhif8XBEDXJ14"

    apis = {
        'videos.list': 'https://www.googleapis.com/youtube/v3/videos',
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
        'activities': 'https://www.googleapis.com/youtube/v3/activities',
    }
    page_info = {}
    def __init__(self, params):
        self.youtube_key = "AIzaSyDQVlmu0vVKoKP_4dKfmOFhif8XBEDXJ14"

    def get_video_info(self, video_id):

        api_url = self.get_api('videos.list')
        params = {
            'id': video_id,
            'key': self.youtube_key,
            'part': 'id, snippet, contentDetails, player, statistics, status'
        }
        apiData = self.api_get(api_url, params)

        return self.decode_single(apiData)

    def search(self, q, max_results=10):

        params = {
            'q': q,
            'part': 'id, snippet',
            'maxResults': max_results
        }

        return self.search_advanced(params)

    def search_videos(self, q, max_results=10, order=None):

        params = {
            'q': q,
            'type': 'video',
            'part': 'id, snippet',
            'maxResults': max_results
        }
        if order is not None:
            params['order'] = order

        return self.search_advanced(params)

    def search_advanced(self, params, page_info=False):

        api_url = self.get_api('search.list')
        if params is None or 'q' not in params:
            raise ValueError('at least the Search query must be supplied')

        api_data = self.api_get(api_url, params)
        if page_info:
            return {
                'results': self.decode_list(api_data),
                'info': self.page_info
            }
        else:
            return self.decode_list(api_data)

    def paginate_results(self, params, token=None):

        if token is not None:
            params['pageToken'] = token
        if params:
            return self.search_advanced(params, True)

    def get_channel_by_name(self, username, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'forUsername': username,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)

    def get_channel_by_id(self, id, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'id': id,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)

    def get_api(self, name):
        return self.apis[name]

    def decode_single(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array[0]

    def decode_list(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            self.page_info = {
                'resultsPerPage': res_obj['pageInfo']['resultsPerPage'],
                'totalResults': res_obj['pageInfo']['totalResults'],
                'kind': res_obj['kind'],
                'etag': res_obj['etag'],
                'prevPageToken': None,
                'nextPageToken': None
            }
            if 'prevPageToken' in res_obj:
                self.page_info['prevPageToken'] = res_obj['prevPageToken']
            if 'nextPageToken' in res_obj:
                self.page_info['nextPageToken'] = res_obj['nextPageToken']

            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array

    def api_get(self, url, params):

        params['key'] = self.youtube_key

        f = urllib2.urlopen(url + "?" + urllib.urlencode(params))
        data = f.read()
        f.close()

        return data
# ------------------------------------------------------------------------------------------------
print '\nYoutube API v3'

text = raw_input("Please enter what you need to search: ")
# text = 'IOT Greenhouse (Embedded Project)'
# service = build("customsearch", "v1",developerKey="AIzaSyDxpJfGwM9KzeTFlKa-_Z-wEgI1sKMcKKo")
youtube = YoutubeAPI('key:AIzaSyDQVlmu0vVKoKP_4dKfmOFhif8XBEDXJ14')

params = {
    'q': text,
    'type': 'video',
    'part': 'id, snippet',
    'maxResults': 50
}   

page_tokens = []
search = youtube.paginate_results(params, None)
page_tokens.append(search['info']['nextPageToken'])
search = youtube.paginate_results(params, page_tokens[0])

# print search

Y = search['results']
length = len(Y)

channel_ID = ''
video_ID =''
Channel_TITLE =''
# for x in xrange(1,length):
for x in xrange(1,10):    
    X = Y[x]
    try:
        print '-----------------------------------------------------------------'
        print 'video ID    : ' + X["id"]["videoId"]
        print 'Title       : ' + X['snippet']['title'].encode('ascii', 'ignore')
        print 'cahnelTitle : ' + X['snippet']['channelTitle'].encode('ascii', 'ignore')
        print 'ChanelID    : ' + X['snippet']['channelId'] + '\n'

        # channel_ID = X['snippet']['channelId']
        video_id=X["id"]["videoId"].encode('ascii', 'ignore')
        Channel_TITLE = X['snippet']['channelTitle'].encode('ascii', 'ignore').encode('ascii', 'ignore')
        # VIDEO INFO-----------------------------------------------------------------------------------------------
        info = youtube.get_video_info(video_id)
        print 'Title       : '+info['snippet']['localized']['title'].encode('ascii', 'ignore')
        print 'Description : '+info['snippet']['localized']['description'].encode('ascii', 'ignore')
        # GET ALL THE COMMENTS-------------------------------------------------------------------------------------
        print '\nComments : \n'
        try:
            # url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=ow1IkOC8fyY&key=AIzaSyDQVlmu0vVKoKP_4dKfmOFhif8XBEDXJ14&maxResults=20'    
            url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='+video_id+'&key=AIzaSyDQVlmu0vVKoKP_4dKfmOFhif8XBEDXJ14&maxResults=20'    
            flag = 0
            resp = requests.get(url)
            data = resp.json() 
            for x in xrange(1,10):
                print 'Comments '+str(x)+' : '+data['items'][x]['snippet']['topLevelComment']['snippet']['textDisplay'].encode('ascii', 'ignore')
        except:
            pass
        # # GET THE PROFILE-------------------------------------------------------------------------------------
        print '\nRelated googleplus accounts : \n'
        try:
            # print '\n'+Channel_TITLE+'\n'
            googleplusURL = 'https://content.googleapis.com/plus/v1/people?query='+Channel_TITLE+'&key=AIzaSyAyYNHFXt6EHanIqxgZZw4jTpV-2G60mLI'
            profile_list = requests.get(googleplusURL)
            data = profile_list.json()
            x=0
            for x in xrange(1,10):
                print 'Account '+str(x)+' : '+data['items'][x]['url'].encode('ascii', 'ignore')
            pass
        except Exception, e:
            pass
            # print e
        # ----------------------------------------------------------------------------------------------------
    except Exception, e:
        print e

# -----------------------------------------------------------------------------------------
# Channel_TITLE = 'Akila wickey'
# print Channel_TITLE
# res = service.cse().list(
#       q=Channel_TITLE, #Search words
#       cx='001132580745589424302:jbscnf14_dw',  #CSE Key
#       lr='lang_pt', #Search language
#     ).execute()

# # print res

# for x in xrange(1,10):
#     X = res['items'][x]
#     print X['displayLink']
#     pass
# -------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------


# print type(data) 
# video = youtube.get_video_info(video_id)
# print video
# chanel = youtube.get_channel_by_id(channel_ID)
# print chanel