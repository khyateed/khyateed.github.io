from __future__ import print_function 
import sys
import boto3
import json
import decimal
import spotipy
import spotipy.util as util
import os
import requests
import time



#This is the lambda1 copy

#################################### FUNCTIONS ####################################
def refreshTheToken(refreshToken, table):

    clientIdClientSecret = 'Basic ZGMyZDE3YWYyODdhNDRkMDliNTBiZGViYmY4OGY1ODY6MDdjZmZmMWQ1MTdmNDE1OGI2YzMwYTUwNjUzN2NmNTI='
    data = {'grant_type': 'refresh_token', 'refresh_token': refreshToken}

    headers = {'Authorization': clientIdClientSecret}
    p = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)

    spotifyToken = p.json()
    table.put_item(Item={'spotify': 'prod', 'expiresAt': int(time.time()) + 3200, 'accessToken': spotifyToken['access_token']})


def get_top_artists(token):
	artist_list=[]
	sp = spotipy.Spotify(auth=token)
	response = sp.current_user_top_artists(limit=10)
	for artist in response['items']:
		artist_list.append(artist['name'])
	return artist_list

def get_artist_ids(artist_list):
	artist_ids = []
	for artist_name in artist_list:
		params= {'apikey': apikey,
			'q_artist': artist_name}
		request = requests.get("http://api.musixmatch.com/ws/1.1/artist.search", params)
		response= json.loads(request.text)
		artist_ids.append(response['message']['body']['artist_list'][0]['artist']['artist_id'])
	return artist_ids

def get_album_ids(artist_ids):
	album_list=[]
	for artist_id in artist_ids:
		params= {'apikey': apikey,
		'artist_id': artist_id}
		request = requests.get("http://api.musixmatch.com/ws/1.1/artist.albums.get", params)
		response= json.loads(request.text)
		for album in response['message']['body']['album_list']:
			album_list.append(  album['album']['album_id'])
	return album_list

def publishSNS(album_list):
	sns = boto3.client('sns')
	sns.publish(TopicArn='arn:aws:sns:us-east-1:552556060587:album_id_list', Message=str(album_list))

	#################################### MAIN ####################################
def lambda_handler(event,context):
	global apikey
	apikey = event['apikey']
	refreshToken = "AQDLLZ8OxvzgVewckp_Z6nYnWXWKoO2PV4sDc4qg4lKY5fkKSjlSesgAl1HwbAm01x6FlA8mn4x9uS-AeXeySlCcDNG6B3NIlmrmZ-GQPUEhrC2KnVSVNesvs0-NgrTSltxIjA"
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('SpotifyState')
	tableToken = table.get_item(Key={'spotify': 'prod'})
	expiresAt = tableToken['Item']['expiresAt']
	if expiresAt <= time.time():
		refreshTheToken(refreshToken, table)
		print('================refreshed the token=============')
		refreshedTableToken = table.get_item(Key={'spotify': 'prod'})
		token = refreshedTableToken['Item']['accessToken']
	else:
		print('================did NOT refresh the token=============')
		token = tableToken['Item']['accessToken']

	artist_list = get_top_artists(token)
	artist_ids = get_artist_ids(artist_list)
	album_list = get_album_ids(artist_ids)
	publishSNS(album_list)
	print('=========== SUCCESS ==============')


