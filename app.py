from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        quality = request.form.get('quality')

        if quality == "audio":
            ydl_format = "bestaudio"
        elif quality == "480":
            ydl_format = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        elif quality == "720":
            ydl_format = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality == "1080":
            ydl_format = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        else:
            ydl_format = "best"

        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': ydl_format,
            'merge_output_format': 'mp4'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = os.path.basename(filename)

            return f"""
            <h2>✅ Download Ready!</h2>
            <a href="/download/{filename}">Download "{filename}"</a><br><br>
            <a href="/">Download another video</a>
            """
        except Exception as e:
            return f"""
            <h2>❌ Error Occurred</h2>
            <p>{str(e)}</p>
            <a href="/">Try Again</a>
            """

    return render_template('index.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0',port=5000)
