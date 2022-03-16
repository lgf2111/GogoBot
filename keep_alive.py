from flask import Flask, redirect
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return redirect('https://gogoanime.gg/')


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()
