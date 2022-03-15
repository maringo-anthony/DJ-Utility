# Anthony Maringo Alm4cu
import os
import subprocess
import time


class MP3Processor:

    def getSongMetaData(self, songs):
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
