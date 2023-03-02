"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import pymongo

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', 200, type=int)
    begin_date = request.args.get('begin_date', '2021-01-01T00:00', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    
    open_time = acp_times.open_time(km, brevet_dist_km, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    app.logger.debug("DID IT HAPPEN???")
    close_time = acp_times.close_time(km, brevet_dist_km, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_store_data")
def _store_data():
    """
    Stores brevet data into a mongodb
    """
    client = pymongo.MongoClient(CONFIG.MONGO_URL, username = CONFIG.USERNAME, password = CONFIG.PASSWORD)
    db = client["brevet_times_db"]
    time_table = db["time_table"]
    race_info = db["race_info"]
    km = request.args.get('km', None, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', '-1', type=str)
    begin_date = request.args.get('begin_date', '-1', type=str)
    id = request.args.get('id', -1, type=int)
    close_time = request.args.get('close_time', '-1', type=str)
    open_time = request.args.get('open_time', '-1', type=str)

    if begin_date != '-1':
        app.logger.debug("Here we go")
        race_info.replace_one({},{"begin_date": begin_date, "brevet_dist_km": brevet_dist_km})    
    else:
        time_table.update_one({"id": id}, {"$set": {"km": km, "close_time": close_time, "open_time": open_time}}, upsert=True)
    
    result = {"msg":"Successfully inserted row {}".format(id)}
    return flask.jsonify(result=result)

@app.route("/_get_data")
def _get_data():
    """
    Retrieves data from a mongodb
    """
    client = pymongo.MongoClient(CONFIG.MONGO_URL, username = CONFIG.USERNAME, password = CONFIG.PASSWORD)
    db = client["brevet_times_db"]
    time_table = db["time_table"]
    race_info = db["race_info"]
    result = -1

    is_form_data = request.args.get("is_form_data", -1, type=int)
    if (is_form_data == 1):
        id = request.args.get("id", -1, type=int)
        result = time_table.find_one({"id": id}, {"_id": 0})
    elif (is_form_data == 0):
        app.logger.debug("Am I ever here??")
        result = race_info.find_one({}, {"_id": 0})
    app.logger.debug(result)
    return flask.jsonify(result=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
