# -*- coding: utf-8 -*-

import urllib, json,re


def return_youtubevideos(author):
    foundAll = False
    ind = 1
    videos = []
    while not foundAll:
        inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?start-index={0}&max-results=20&alt=json&orderby=published&author={1}'.format( ind, author ) )
        try:
            resp = json.load(inp)
            inp.close()
            returnedVideos = resp['feed']['entry']
            for video in returnedVideos:
                videos.append( video ) 

            ind += 50
            if ( len( returnedVideos ) < 50 ):
                foundAll = True
        except:
            foundAll = True

    video_list = []
    for video in videos:
        video_id = re.compile('v=(.+?)&').findall(video['link'][0]['href'])
        if video_id:
            video_list.append([video['title']['$t'],video_id[0],video['media$group']['media$thumbnail'][0]['url']])
    return video_list

