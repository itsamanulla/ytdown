from flask import Flask, redirect, render_template, request, send_file, url_for,session
from pytube import YouTube

from io import BytesIO


app = Flask(__name__)
app.secret_key = "amanullahshaikh"

@app.route('/', methods =["GET", "POST"])
def home():
    if request.method == "POST":
        session["link"] = request.form.get("link")
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return "<h1>Can't find the video please check the url</h1>"
        return render_template('downloads.html',url=url)
    return render_template('index.html')

@app.route('/downloads', methods =["GET", "POST"])
def download():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name = url.title+".mp4", mimetype='video/mp4')
    return redirect(url_for('home'))

@app.route('/audio_download', methods =["GET", "POST"])
def audio_download():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        audio = url.streams.get_by_itag(itag)
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        # base = os.path.splitext(audio)
        # new_file = base + '.mp3'
        # os.rename(audio,new_file)
        return send_file(buffer,as_attachment=True,download_name=url.title+".mp3")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)