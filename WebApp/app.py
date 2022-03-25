from zipfile import ZipFile

from flask import Flask, render_template, request, send_file

from WebApp.CamelotKeyConverter import CamelotKeyConverter
from WebApp.YoutubeDownloader import Youtube_Downloader

app = Flask(__name__)


@app.route('/')
@app.route('/camelot')
def camelot_page():
    return render_template('camelot.html')


@app.route('/camelot', methods=['GET', 'POST'])
def camelot_upload_file():
    if request.method == "POST":
        f = request.files['file']
        if not f:
            return render_template('camelot.html')

        f.save(f.filename)

        converter = CamelotKeyConverter()
        converted_xml = converter.convertToCamelotKeys()

        with open("rekordbox_out.xml", "w") as out_file:
            out_file.write(converted_xml)

        if request.form['compressed_radio']:
            with ZipFile("rekordbox.zip", "w") as zipObj:
                zipObj.write("rekordbox_out.xml")

        return render_template('converted_xml.html', xml=converted_xml)


@app.route('/download_xml')
def download_rekordbox_xml():
    return send_file('rekordbox.xml', as_attachment=True)


@app.route('/download_compressed_xml')
def download_compressed_rekordbox_xml():
    return send_file('rekordbox.zip', as_attachment=True)


@app.route('/youtube_search')
def youtube_search_page():
    return render_template("youtube_search.html")


@app.route('/youtube_search', methods=['GET', 'POST'])
def download_mp3():
    if request.method == "POST":
        song_name = request.form['song-name']

        if request.form['remix_radio']:
            remix = request.form['remix_radio']
        else:
            remix = False

        downloader = Youtube_Downloader()

        # TODO: Make the file that is actually downloaded connected to the link that says click to download your song
        song_file = downloader.download_song(song_name, remix)
        return render_template('song_download.html')


@app.route('/song_download')
def download_song():
    # TODO: Find song that was downloaded then send it
    return send_file('Dance_With_Me_Tonight.mp3', as_attachment=True)


if __name__ == '__main__':
    app.run()
