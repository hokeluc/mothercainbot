# Internal packages
import lyricsgenius
import random
import tweepy
import os

# Global vars
genius = lyricsgenius.Genius(os.environ['GENIUSAPIKEY'])
all_songs = ["Age of Delilah", "A House In Nebraska", "A long, unfortunate while (demo)", "American Teenager", "Antlers", "Bruises", "Casings", "Crush", "Crying During Sex", "Dog Days", "Dust Bowl (Demo)", "Everytime - Spotify Singles", "Family Tree (Intro)", "Family Tree", "Gibson Girl", "God's Country", "Golden Age", "Growing Pains", "Half-Cocked", "Hard Times", "Head in the Wall", "Inbred", "Knuckle Velvet", "Lilies", "Michelle Pfeiffer", "Misuse Oh", "Ptolemaea", "Strangers", "Sun Bleached Flies", "Sunday Morning", "Thoroughfare", "Two-Headed Mother", "Unpunishable", "Western Nights", "Waco, Texas (Demo)"]

# Determine a random song, return full lyrics string and song name
def get_raw_lyrics():
    genius_client_access_token = (os.environ['GENIUSCAT'])
    # Create genius object
    genius = lyricsgenius.Genius(genius_client_access_token)
    random_song_title = random.choice(all_songs)
    lyrics = genius.search_song(random_song_title, "Ethel Cain").lyrics
    song = random_song_title.upper()
    return lyrics, song

# Split full lyrics string 
def get_tweet_from(lyrics, tweet):
    # Splits string into array
    lines = lyrics.split('\n')
    # Delimitator to remove miscellaneous characters
    for index in range(len(lines)):
        if lines[index] == "" or "[" in lines[index]:
            lines[index] = "XXX"
    lines = [i for i in lines if i != "XXX"]
    # Finds random two lines from lyrics
    random_num = random.randrange(0, len(lines)-1)
    tweet = lines[random_num] + "\n" + lines[random_num+1]
    # Replaces more miscellaneous characters
    misc_chars = ["\\", "Embed", "You might also like", "Outro:", "You might also likeOutro:", "Pre-chorus:", "See Ethel Cain LiveGet tickets as low as $65", "See Ethel Cain Live", "Get tickets as low as $", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Verse", "Pre-Chorus", "Chorus"]
    for i in misc_chars:
        tweet = tweet.replace(i,"")
    print(tweet)
    # Returns tweet
    return tweet

# Lambda-required function definition
def handler(event, context):
    tweet =""
    api = tweepy.Client(bearer_token= os.environ['TBEARERTOKEN'], consumer_key=os.environ['TCONSUMERKEY'], consumer_secret=os.environ['TCONSUMERSECRET'], access_token=os.environ['TACCESSTOKEN'], access_token_secret=os.environ['TACCESSSECRET'], return_type=tweepy.Response, wait_on_rate_limit=False)
    lyrics, song = get_raw_lyrics()
    tweet = get_tweet_from(lyrics, tweet)
    # Posts tweet
    status = api.create_tweet(text=tweet, place_id=song)