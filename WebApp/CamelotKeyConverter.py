# Anthony Maringo Alm4cu
import os


class CamelotKeyConverter:
    camelot_conversions = {'A': '11B', 'Ab': '4B', 'G#': '4B', 'Am': '8A', 'B': '1B', 'Bb': '6B', 'Bbm': '3A',
                           'A#m': '3A',
                           'Bm': '10A', 'C': '8B', 'C#m': '12A', 'Dbm': '12A', 'Cm': '5A', 'D': '10B', 'Db': '3B',
                           'Dm': '7A', 'E': '12B', 'Eb': '5B', 'D#': '5B', 'Ebm': '2A', 'Em': '9A', 'F': '7B',
                           'F#m': '11A',
                           'Fm': '4A', 'G': '9B', 'G#m': '1A', 'Abm': '1A', 'Gb': '2B', 'F#': '2B', 'Gm': '6A'}

    REKORDBOX_XML = os.getcwd() + "/rekordbox.xml"

    def convertToCamelotKeys(self):
        """
        Go through the recordbox.xml and convert any found keys to camelot keys

        """

        xml = self.get_xml()

        for key in self.camelot_conversions.keys():
            old = "Tonality=\"" + key + "\" "
            new = "Tonality=\"" + self.camelot_conversions[key] + "\" "

            xml = xml.replace(old, new)
        return xml

    def get_xml(self):
        with open(self.REKORDBOX_XML, 'r') as f:
            data = f.read()
        return data
