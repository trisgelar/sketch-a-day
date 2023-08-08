"""
Toot from sketch-a-day
"""
from time import sleep
import tomllib
#import tomli as tomllib # tomllib will be in Python 3.11's standard library only
from mastodon import Mastodon

with open("/home/villares/api_tokens", "rb") as f:
    api_tokens = tomllib.load(f)
    
access_token = api_tokens['pynews']['access_token']
masto_instance = 'pynews.com.br'
mastodon = Mastodon(access_token=access_token, api_base_url=masto_instance)

def mime_type(file):
    if file is None:
        return None
    ff = str(file).split('.')[-1].lower()
    if ff == 'jpg':
        return 'image/jpeg'
    return f'image/{ff}'

def toot( 
         post_text,
         image_file=None, description=None,
         visibility="public", language='pt'):
    
    if image_file:
        media = mastodon.media_post(
            image_file, mime_type=mime_type(image_file),
            description=description, focus=None,
            #file_name=None, thumbnail=None,
            #thumbnail_mime_type=None, synchronous=False
            )
        sleep(1)
        media_ids = [media["id"]]
    else:
        media_ids=[]
    mastodon.status_post(post_text, in_reply_to_id=None, media_ids=media_ids, language=language, visibility="public")
