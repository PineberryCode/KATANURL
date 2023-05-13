import random
import string
import json
import os
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
shortened_urls = {}

def generate_short_url(length=7):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

def generate_customized_url(change_URL):
    changed_URL = "".join(change_URL)
    return changed_URL

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url'].strip() #long_url is the link of the input Example -> http://anywebpage.com
        change_URL = request.form.get('change_URL','').strip()
        if change_URL:
            short_url = generate_customized_url(change_URL)
        else:
            short_url = generate_short_url()
            while short_url in shortened_urls:
                short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        with open("src/urls.json", "w") as u: #w = write
            json.dump(shortened_urls, u)
        shortened_URL = f"{request.url_root}{short_url}" #{request.url_root} = http://IPWebPage or domain
        return render_template("view/redirect.html", shortened_URL=shortened_URL)
    return render_template("view/welcome.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

@app.after_request
def add_header(response):
    """
    Caché
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Cache-control"] = 'public, max-age=0'
    return response

    
if __name__ == "__main__":
    if not os.path.exists("src/urls.json"):
        with open("src/urls.json", "w") as o: # The urls into file urls.json will open. r = read
            shortened_urls = {}
            json.dump(shortened_urls, o)
    else:
        with open("src/urls.json", "r") as o:
            shortened_urls = json.load(o)
    app.run(host="0.0.0.0", port=5000, debug=True)
