from youtubesearchpython import VideosSearch
from os import path
import pafy
import asyncio
loop = asyncio.get_event_loop()
#Pafy

def url_stream(url: str):
    video = pafy.new(url)
    videos = video.getbest().url
    return videos

# THUMBNAIL AND TITLE
def thumbnail(query: str):
    search = VideosSearch(query, limit = 1).result()["result"][0]["thumbnails"][0]["url"]
    search = search.split("?")[0]
    return search

def title(query: str):
    search = VideosSearch(query, limit = 1).result()["result"][0]["title"]
    return search

#Youtube Search and Download
def ytsearch(query: str):
    search = VideosSearch(query, limit = 2)
    link = search.result()["result"][0]["link"]
    x = url_stream(link)
    return x 

#User Input

async def user_input(input):
    """ retrieve user input """
    if ' ' in input or '\n' in input:
       return str(input.split(maxsplit=1)[1].strip())
    return ''

# loop
async def streamloop(query):
    video = await loop.run_in_executor(None, ytsearch, query)
    return video
