from flask import render_template, jsonify, url_for
from app import app
import json

def grab_cat(cat):
    conn, cur = pp.connect() # connect to the database and return the connection and cursor
    email_list = es.get_mail()
    for email in email_list:
    	pp.add_email(cur, email)
    conn.commit()
    json_dict = pp.all_cats_to_json(conn) # make a json string from it
    json_dict["data"] = [child for child in json_dict['data'] if (child['name'] == cat)][0]
    json_dict["data"]["children"] = [email for email in json_dict["data"]["children"] if (len(str(email['body'])) < 10000)]
    for i in range(len(json_dict["data"]["children"])):
        json_dict["data"]["children"][i]["body"] = "\'".join(json_dict["data"]["children"][i]["body"].split("=E2=80=99"))
        json_dict["data"]["children"][i]["name"] = "\'".join(json_dict["data"]["children"][i]["name"].split("=E2=80=99"))
    pp.close_conn(conn, cur) # close the connection, but don't change things
    return json_dict # return the json, which will be accessible from the url/data

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Olin'}
    return render_template('index.html', title='Home', user=user)

from app import postgres_parser as pp # anything that is imported from this file needs to be app.<name>
from app import email_scraper as es

@app.route('/food')
def food():
    return jsonify(grab_cat("Food"))

@app.route('/event')
def event():
    return jsonify(grab_cat("Event"))

@app.route('/lost')
def lost():
    return jsonify(grab_cat("Lost"))

@app.route('/other')
def other():
    return jsonify(grab_cat("Other"))
