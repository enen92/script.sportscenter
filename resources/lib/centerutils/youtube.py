# -*- coding: utf-8 -*-

import urllib, json,re


def return_youtubevideos(author):
    foundAll = False
    ind = 1
    videos = []
    while not foundAll:
        inp = urllib.urlopen('https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername='+author+'&key=AIzaSyAxaHJTQ5zgh86wk7geOwm-y0YyNMcEkSc')
        try:
            resp = json.load(inp)
            inp.close()
            playlist_id = resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            inp = urllib.urlopen('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='+playlist_id+'&key=AIzaSyAxaHJTQ5zgh86wk7geOwm-y0YyNMcEkSc&maxResults=50')
            resp = json.load(inp)
            inp.close()
            returnedVideos = resp["items"]
            for video in returnedVideos:
                videos.append( video ) 
            foundAll = True
        except:
            foundAll = False

    video_list = []
    if foundAll:
        for video in videos:
            video_id = video["snippet"]["resourceId"]["videoId"]
            video_title = video["snippet"]["title"]
            video_thumb = video["snippet"]["thumbnails"]["high"]["url"]
            if video_id:
                video_list.append([video_title,video_id,video_thumb])
    return video_list

