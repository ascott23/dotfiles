import requests as reqs
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC
from bs4 import BeautifulSoup
import argparse as ap
from os import listdir
from os.path import isfile, isdir, abspath, splitext, join

AUTH_KEY = "kcm1_iIKT15a-3suMhFvfy3UnxLzWtyl3eN2Ki3kErEuLCYZRnBeLrig7Y3wCmIH"
BASE_URL = "https://api.genius.com"

# Create the request headers, they don't change between reqs
HEADERS = {"Authorization": "Bearer " + AUTH_KEY}

# A dict of artists
artists = {}

TITLE = 'TIT2'
ARTIST = 'TPE1'

class Artist(object):
   """
   A class to hold an artist
   """

   def __init__(self, name, id=0):
      self.name = name
      self.id = id
      self.songs = {}
      self.url = "https://genius.com/artists/" + self.name

   def addSong(self, song):
      """
      Adds a song to the artists dict of songs
      """
      self.songs[song.name] = song

class Song(object):
   """
   A wrapper class for a song to store the relevant information
   """

   def __init__(self, name, id=0, artist=None, lyrics_url=""):
      self.name = name
      self.id = id
      self.lyrics_url = lyrics_url

      if artist:
         # The artist exists, so add myself to its songs
         self.addArtist(artist)

   def addArtist(self, artist):
      """
      Adds the given artist to the song
      """
      self.artist = artist
      self.artist.addSong(self)


def artistFromJSON(json):
   """
   Returns an artist class specified by the given json.
   If the artist has already been created, return it, otherwise create a new one
   """
   name = json['name']
   if not name in artists:
      # The artist doesn't exist yet
      artists[name] = Artist(name, json['id'])

   return artists[name]

def songFromJSON(json):
   """
   Creates and returns a song from a song json
   """
   return Song(json['title'],
               json['id'],
               artistFromJSON(json['primary_artist']),
               json['url'])

def getSearchRequest(search_term, page=None):
   """
   Generates and returns a request for the specified search term, and if applicable, page
   """
   # Create the payload params
   payload = {"q": search_term}

   # Only add the page param if it's specified
   if page:
      payload["page"] = page

   return reqs.get("https://api.genius.com/search",
                   params=payload,
                   headers=HEADERS)

def searchForSong(song_name, artist_name=None):
   """
   Attempts to populate a song class for the specified
   """
   # Create the search request
   try:
      search_term = "{} by {}".format(song_name, artist_name) if artist_name else song_name

      request = getSearchRequest(search_term)

      req_json = request.json()

   except Exception as err:
      print("Got an error when searching for {}\nError: {}".format(song_name, err))
      return None

   if req_json['meta']['status'] != 200:
      # Got an error in the response
      print("The request for {} returned an error number {}.".format(song_name, req_json['meta']['status']))

      if 'message' in req_json['meta']:
         # Theres a message attached, output it
         print("With error msg: {}".format(req_json['meta']['message']))

      return None

   # The JSON response is good at this point
   hits = req_json['response']['hits']

   if hits == []:
      # Hits is an empty list :(
      print("The search for {} returned no hits.".format(song_name))
      return None

   # There's results
   song_info = None
   if artist_name:
      # Loop through the results to find the one corresponding to the artist
      for hit in hits:
         if hit['result']['primary_artist']['name'] == artist_name:
            song_info = hit['result']
            break
   else:
      # Theres no artist_name so just go with the first result
      song_info = hits[0]['result']

   if song_info:
      # We got a result
      return songFromJSON(song_info)

   # Didn't find any song_info
   return None

def scrapeLyrics(song):
   """
   Takes a song class and returns the lyrics corresponding to it
   """
   # Check if the song exists
   if song == None:
      return

   try:
      # Attempt to get the lyrics page
      page = reqs.get(song.lyrics_url)

      # Parse the html
      html = BeautifulSoup(page.text, "html.parser")

      # Remove script tags that they put in the middle of the lyrics
      [h.extract() for h in html('script')]
      lyrics = html.find("lyrics").get_text()

      return lyrics
   except Exception as err:
      print("Encountered an error while scraping lyrics for {}.\nError: {}".format(song.name, err))
      return ""

def addLyrics(path):
   """
   Add's the lyrics for the provided file path
   """
   # Create the tags if needed
   try:
      tags = ID3(path)
   except ID3NoHeaderError:
      tags = ID3()

   # Remove lyrics if they already exist
   if len(tags.getall(u"USLT")) != 0:
       tags.delall(u"USLT")

   song = searchForSong(tags[TITLE],
                        tags[ARTIST] if tags[ARTIST] != "" else None)

   if song == None:
      print("Couldn't find the song for the path:\n{}".format(path))
      return

   lyrics = scrapeLyrics(song)

   tags[u"USLT"] = (USLT(encoding=3, lang='ENG', text=lyrics))

   tags.save(path)
   print("Done: {}".format(path))


def main(files):
   for file in files:
      file = abspath(file)

   for file in files:
      try:
         # Only works with mp3 currently
         if isfile(file) and splitext(file)[1] == '.mp3':
            addLyrics(file)

         # Work recursively
         elif isdir(file):
            files.extend([join(file, i) for i in listdir(file)])

      except Exception as err:
         print("Encountered an error while attempting to process {}.\nError: ".format(file, err))

if __name__ == "__main__":
   parser = ap.ArgumentParser(description='List files to add lyrics to.')

   parser.add_argument('-i', '--in', nargs='+', help="The files or folders to run on.", dest="in_files")

   args = parser.parse_args()

   main(args.in_files)
