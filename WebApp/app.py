from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_page():  # put application's code here
    return render_template('home.html')


@app.route('/camelot')
def camelot_page():
    return render_template('camelot.html')


@app.route('/camelot_upload', methods=['GET', 'POST'])
def camelot_upload_file():
    if request.method == "POST":
        f = request.files['file']
        f.save(f.filename)
        return 'file uploaded successfully'


# Camelot keys
# We need to be able to upload a file
# Modify that file
# present new file with the modifications


if __name__ == '__main__':
    app.run()
