from __future__ import print_function 
import sys
import boto3
import json
import decimal
import spotipy
import spotipy.util as util
import os
import requests
import nltk
import time



#This is the lambda copy

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

def get_tracks(album_list):
	track_list =[]
	for album_id in album_list:
		params= {'apikey': apikey,
		'album_id': album_id}
		request = requests.get("http://api.musixmatch.com/ws/1.1/album.tracks.get", params)
		response= json.loads(request.text)
		
		for track in response['message']['body']['track_list']:
				if track['track']['has_lyrics'] ==1:
					track_list.append((track['track']['track_name'], track['track']['artist_name'], track['track']['track_id']))
	return track_list

def get_lyrics(track_list):
	lyrics_list =[]
	for track_name, artist, track_id in track_list:
		params= {'apikey': apikey,
				'track_id': track_id}
		request = requests.get("http://api.musixmatch.com/ws/1.1/track.lyrics.get", params)
		response= json.loads(request.text)
		lyrics = response['message']['body']['lyrics']['lyrics_body']
		lyrics_list.append({'track_name':track_name, 'artist':artist, 'lyrics': lyrics[:-75]})
	return lyrics_list

def comprehend(lyrics_list):
	comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

	for song in lyrics_list:
		try:
			comprehend_key_phrases = comprehend.detect_key_phrases(Text= song['lyrics'], LanguageCode='en')
			tokens = []
			key_words=[]
			for phrase in comprehend_key_phrases['KeyPhrases']:
			  	text = phrase["Text"]
			  	tokens = nltk.word_tokenize(text)
			  	tagged = nltk.pos_tag(tokens)
			  	for word, pos in tagged:
			  		if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'VB']:
			  			if word.lower() not in key_words:
			  				key_words.append(word.lower())
			title = song['track_name']
			tokens = nltk.word_tokenize(title)
			tagged = nltk.pos_tag(tokens)
		  	for word, pos in tagged:
		  		if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'VB']:
		  			if word.lower() not in key_words:
		  				key_words.append(word.lower())
			song['key_words'] = key_words
		except:
			pass

########## Getting sentiment of the song #########
	# for song in lyrics_list:
	# 	comprehend_sentiment = comprehend.detect_sentiment(Text=song['lyrics'], LanguageCode='en')
	# 	sentiments ={}
	# 	sentiments['Mixed'] = comprehend_sentiment['SentimentScore']['Mixed']
	# 	sentiments['Positive'] = comprehend_sentiment['SentimentScore']['Positive']
	# 	sentiments['Neutral'] = comprehend_sentiment['SentimentScore']['Neutral']
	# 	sentiments['Negative'] = comprehend_sentiment['SentimentScore']['Negative']
	# 	song['sentiments'] = sentiments
	return json.dumps(lyrics_list)

def uploadToS3(lyrics_data):
	s3 = boto3.client('s3')
	s3.put_object(Body=lyrics_data, Bucket='get.lyrics.output.data', Key='lyricsData.json')

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
	track_list = get_tracks(album_list)
	lyrics_list = get_lyrics(track_list)
	lyrics_data = comprehend(lyrics_list)
	uploadToS3(lyrics_data)
	print('=========== SUCCESS ==============')
