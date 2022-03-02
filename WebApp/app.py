from flask import Flask, render_template, request

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
        converted_xml = converter.convertToCamelotKeys()  # TODO: MAKE THIS FORMATTED PROPERLY OR MAKE IT A FILE TO DOWNLAOD

        return render_template('converted_xml.html', xml=converted_xml)


# Camelot keys
# Modify that file
# present new file with the modifications


if __name__ == '__main__':
    app.run()
