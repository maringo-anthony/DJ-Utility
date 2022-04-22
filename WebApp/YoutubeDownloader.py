# Anthony Maringo Alm4cu
import os

from pytube import Search


class Youtube_Downloader:

    def search_song(self, song_name, remix):
        video_to_download = None

        if remix:  # TODO: Figure out why this isnt giving the videos with most views like i would expect
            search_results = Search(str(song_name + " remix")).results[:20]
            search_results = list(filter(lambda x: "remix" in x.title, search_results))
            search_results.sort(key=lambda x: x.views, reverse=True)

            print(search_results[0].views)

            if search_results[0].views > 2000000:  # Only download remixes if they have 2mil+ views
                return search_results.pop()

        search_results = Search(str(song_name)).results[:20]

        for yt in search_results:
            if "Official Audio" in yt.title:  # Opt for the official audio over other sources
                video_to_download = yt
                break
            elif not video_to_download and yt.length < 900:  # Make sure we are not defaulting to a +15 min song
                video_to_download = yt

        return video_to_download

    def download_song(self, song_name, remix=False):

        video = self.search_song(song_name, remix)

        # Extract only audio
        video_to_download = video.streams.filter(only_audio=True).first()

        # Download the file
        out_file = video_to_download.download(output_path=os.getcwd())

        # Save the file
        base, ext = os.path.splitext(out_file)

        if remix:
            new_file = base + '-remix.mp3'
        else:
            new_file = base + '.mp3'
        print("NEW FILE NAME: " + new_file)

        os.rename(out_file, new_file)

        return new_file
