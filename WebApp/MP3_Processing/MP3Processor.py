# Anthony Maringo Alm4cu
import json
import os
import subprocess
import time
import urllib.request

import acoustid
import chromaprint


def getSongMetaData(song):
    """
    Get the meta data for a songs and move it to /Users/anthonymaringo/cleaned_up_music

    :param song: string file names in the form songName.mp3
    """

    dirName = os.path.dirname(__file__)

    scriptFile = os.path.join(dirName, 'beetsMetaDataScript.exp')

    songFile = os.path.join(dirName, "../" + song)

    command = [scriptFile, songFile]
    subprocess.call(command)


def getSongsMetaData(self, songs):
    """
    Get the meta data for a list of songs and move them to /Users/anthonymaringo/cleaned_up_music

    :param songs: list of file names in the form songName.mp3
    """

    requests_sent = 0
    for song in songs:
        dirName = os.path.dirname(__file__)

        scriptFile = os.path.join(dirName, 'beetsMetaDataScript.exp')

        songFile = os.path.join(dirName, "../Music to process/" + song)

        command = [scriptFile, songFile]
        subprocess.call(command)

        # Make sure we don't send more than 3 requests per second
        requests_sent += 1
        if requests_sent == 3:
            requests_sent = 0
            time.sleep(.5)


def getAPIKey():
    dirName = os.path.dirname(__file__)

    with open(os.path.join(dirName, 'API_KEY.TXT'), 'r') as f:
        key = f.readline().rstrip()

    return key


def newAttemptAtMetaData(song):
    dirName = os.path.dirname(__file__)
    file = os.path.join(dirName, song)

    API_KEY = getAPIKey()
    # todo: figure out finger printing to get the meta data from acousticid via the url request
    duration, fp_encoded = acoustid.fingerprint_file(file)
    fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
    print(fingerprint)


    candidates = acoustid.match(API_KEY, file)  # returns a generator of candidates



    best_score, best_acoustId, best_title, best_artist = next(candidates)

    metadata = {}
    with urllib.request.urlopen("https://acousticbrainz.org/api/v1/" + best_acoustId + "/low-level") as url:
        data = json.loads(url.read().decode())
        metadata = data['metadata']

    return metadata


newAttemptAtMetaData('riptide.mp3')
