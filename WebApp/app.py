from flask import Flask, render_template, request, send_file

from WebApp.CamelotKeyConverter import CamelotKeyConverter

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_page():  # put application's code here
    return render_template('home.html')


@app.route('/camelot')
def camelot_page():
    return render_template('camelot.html')


@app.route('/camelot', methods=['GET', 'POST'])
def camelot_upload_file():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)

        converter = CamelotKeyConverter()
        converted_xml = converter.convertToCamelotKeys()
        with open("rekordbox_out.xml", "w") as out_file:
            out_file.write(converted_xml)

        return render_template('converted_xml.html', xml=converted_xml)


@app.route('/download')
def download_rekordbox_xml():
    return send_file('rekordbox.xml', as_attachment=True)





if __name__ == '__main__':
    app.run()
