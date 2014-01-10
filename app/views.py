import os
from app import app
from flask import request, \
                  abort, \
                  render_template, \
                  send_from_directory
from database import db, \
                     Spam
from helpers import is_authenticated
import requests
import json

@app.route('/', methods=['GET'])
def index():
    return render_template('hello.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')

@app.route('/list/<api_key>', methods=['GET'])
def spam_list(api_key):
    if app.config['API_KEY'] != api_key:
        abort(403)

    emails = db.session.query(Spam).\
                order_by(Spam.created).\
                all()

    return render_template('spam_list.html', emails=emails, api_key=api_key)

@app.route('/spam/', methods=['GET', 'POST', 'DELETE'])
def spam():
    if request.method == 'GET':
        if not is_authenticated():
            return app.response_class(response='{"error": "Invalid API key"}', mimetype='application/json', status=403)

        spams = db.session.query(Spam).\
                   order_by(Spam.created).\
                   all()

        response = []
        for spam in spams:
            response.append(spam.toObject())

        return app.response_class(response=json.dumps(response), mimetype='application/json')

    elif request.method == 'POST':
        try:
            row = Spam(
                to_header=request.form['recipient'],
                from_header=request.form['sender'],
                subject_header=request.form['subject'],
                text_body=request.form['body-plain'],
                html_body=request.form['body-html'],
                spam_score=request.form['X-Mailgun-Sscore']
            )
            db.session.add(row)
            db.session.commit()
        except:
            print "Error saving Spam: %s" % json.dumps(request.form)

        return app.response_class(response='{"status": "ok"}', mimetype='application/json')

    elif request.method == 'DELETE':
        "Delete all rows from the db"
        db.session.query(Spam).delete()
        db.session.commit()

        return app.response_class(response='{"status": "ok"}', mimetype='application/json')

@app.route('/spam/<id>', methods=['GET', 'DELETE'])
def spam_item(id):
    if request.method == 'GET':
        "Get a single spam from the db"
        row = db.session.query(Spam).\
                        filter(Spam.id == id).\
                        first()

        if not row:
            return app.response_class(response='{"error": "Spam not found"}', mimetype='application/json', status=404)

        spam = row.toObject()
        spam['text_body'] = row.getTextBody()
        spam['html_body'] = row.getHtmlBody()

        return app.response_class(response=json.dumps(spam), mimetype='application/json')

    elif request.method == 'DELETE':
        "Delete a single spam from the db"
        row = db.session.query(Spam).\
                        filter(Spam.id == id).\
                        first()

        if not row:
            return app.response_class(response='{"error": "Spam not found"}', mimetype='application/json', status=404)

        db.session.delete(row);
        db.session.commit()

        return app.response_class(response='{"status": "ok"}', mimetype='application/json')

@app.route('/spam/routes/', methods=['GET', 'POST'])
def spam_filter():
    if not is_authenticated():
        return app.response_class(response='{"error": "Invalid API key"}', mimetype='application/json', status=403)

    url = "%s/routes" % app.config['MAILGUN_API_URL']
    auth = ('api', app.config['MAILGUN_API_KEY'])

    if request.method == 'GET':
        r = requests.get(url, auth=auth)
    elif request.method == 'POST':
        params = {
            "priority": 50,
            "expression": 'match_recipient("%s@%s")' % (request.form['local'], request.form['domain']),
            "action": "stop()"
        }

        if 'description' in request.form:
            params['description'] = request.form['description']

        r = requests.post(url, params=params, auth=auth)

    return app.response_class(response=r.text, mimetype='application/json', status=r.status_code)

@app.route('/spam/routes/<id>', methods=['GET', 'DELETE'])
def spam_filter_item(id):
    if not is_authenticated():
        return app.response_class(response='{"error": "Invalid API key"}', mimetype='application/json', status=403)

    url = "%s/routes/%s" % (app.config['MAILGUN_API_URL'], id)
    auth = ('api', app.config['MAILGUN_API_KEY'])

    if request.method == 'GET':
        r = requests.get(url, auth=auth)
    elif request.method == 'DELETE':
        r = requests.delete(url, auth=auth)

    return app.response_class(response=r.text, mimetype='application/json', status=r.status_code)
