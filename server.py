#! /opt/app-root/bin/python3
import plate
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route('/')
def index():
    output = plate.main()
    return output

if __name__ == '__main__':
  app.run(host='aro-plate.b9ad.pro-us-east-1.openshiftapps.com',debug=True)
