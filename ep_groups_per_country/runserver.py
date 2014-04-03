#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


###########################################################################
#####   Views
###########################################################################


@app.route('/')
def index():
    return render_template("index.html")


###########################################################################
#####   Main
###########################################################################


if __name__ == '__main__':
    app.run(debug=True)
