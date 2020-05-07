#This code is courtesy of the blog post https://python.gotrained.com/youtube-api-extracting-comments/

import os
import pickle
import math

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import httplib2

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if credentials is None or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    elif credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(httplib2.Http())

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_videos(service, num_videos, **kwargs):
    final_results = []
    results = service.search().list(**kwargs).execute()

    i = 0
    num_pages = math.ceil(num_videos/5)
    while results and i < num_pages:
        final_results.extend(results['items'])

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break
    return final_results

def search_videos(service, num_videos, **kwargs):
    results = get_videos(service, num_videos, **kwargs)
    video_IDs = []
    n = min(len(results), num_videos)
    for i in range(n):
        item = results[i]
        video_ID = item['id']['videoId']
        video_IDs.append(video_ID)
    return video_IDs

def get_video_IDs():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    keyword = input('Enter keyword: ' )
#    num_videos = int(input('How many videos would you like to scrape? ' ))
    video_IDs = search_videos(service, num_videos=3, q=keyword, part='id,snippet', type='video', order='viewCount')
    return keyword, video_IDs
