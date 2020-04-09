from __future__ import print_function 
import sys
import boto3
import json
import decimal
import os
import requests
import nltk



#This is the lambda2 copy

#################################### FUNCTIONS ####################################


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
				if phrase["Score"] > 0.8:
				  	text = phrase["Text"]
				  	tokens = nltk.word_tokenize(text)
				  	tagged = nltk.pos_tag(tokens)
				  	for word, pos in tagged:
				  		if pos in ['NN', 'NNS', 'NNP', 'NNPS']:
				  			if word.lower() not in key_words:
				  				key_words.append(word.lower())
			title = song['track_name']
			tokens = nltk.word_tokenize(title)
			tagged = nltk.pos_tag(tokens)
		  	for word, pos in tagged:
		  		if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']:
		  			if word.lower() not in key_words:
		  				key_words.append(word.lower())
			song['key_words'] = key_words
		except:
			pass

########## Getting sentiment of the song (not using this) #########
	# for song in lyrics_list:
	# 	comprehend_sentiment = comprehend.detect_sentiment(Text=song['lyrics'], LanguageCode='en')
	# 	sentiments ={}
	# 	sentiments['Mixed'] = comprehend_sentiment['SentimentScore']['Mixed']
	# 	sentiments['Positive'] = comprehend_sentiment['SentimentScore']['Positive']
	# 	sentiments['Neutral'] = comprehend_sentiment['SentimentScore']['Neutral']
	# 	sentiments['Negative'] = comprehend_sentiment['SentimentScore']['Negative']
	# 	song['sentiments'] = sentiments
	return lyrics_list

def prepLyricsData(lyrics_data):
	output_file = open("/tmp/lyrics_data.json", "w+")
	count = 1
	for dic in lyrics_data:
	  	output_file.write("{\"index\":{\"_id\":\"" + str(count) + "\"}}\n")
	  	count += 1
	 	output_file.write(json.dumps(dic) + '\n')
	output_file.close()


def uploadToS3():
	s3 = boto3.client('s3')
	data = open("/tmp/lyrics_data.json", "r")
	s3.put_object(Body=data.read(), Bucket='get.lyrics.output.data', Key='lyricsData.json')

#################################### MAIN ####################################
def lambda_handler(event,context):
	global apikey
	apikey = "a13274c02a52c219a3cd7ca56f561091"


	album_list = json.loads(event['Records'][0]['Sns']['Message'])
	track_list = get_tracks(album_list)
	lyrics_list = get_lyrics(track_list)
	lyrics_data = comprehend(lyrics_list)
	prepLyricsData(lyrics_data)
	uploadToS3()
	print('=========== SUCCESS ==============')
