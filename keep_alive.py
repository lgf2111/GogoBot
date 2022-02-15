from flask import Flask, redirect
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return redirect('https://gogoanime.film/')

def run():
  app.run()

def keep_alive():
  t = Thread(target=run)
  t.start()