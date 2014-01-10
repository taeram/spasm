Spasm
=====

Spasm is a spam management tool for [Mailgun](http://mailgun.com).

Spasm receives POSTed SPAM from Mailgun, allowing you to preview and
delete the SPAM messages without requiring the SPAM to be emailed, thus
protecting the email reputation of your domain.

Spasm also provides a wrapper around the Mailgun Routes API, allowing you to
blacklist email addresses by adding new Mailgun routes.

![spasm-screenshot](http://taeram.github.io/media/spasm-screenshot.png)

Requirements
============
You'll need the following:

* A [Heroku](https://www.heroku.com/) account, if you want to deploy to Heroku.
* A [Mailgun](http://mailgun.com) account
* [Python 2.7.3](http://www.python.org/)
* [pip](https://github.com/pypa/pip)
* [Virtualenv](https://github.com/pypa/virtualenv)

Setup
=====
Local development setup:
```bash
    # Clone the repo
    git clone git@github.com:taeram/spasm.git
    cd ./spasm

    # Setup and activate virtualenv
    virtualenv .venv
    source ./.venv/bin/activate

    # Install the pip requirements
    pip install -r requirements.txt

    # Create the development database (SQLite by default)
    python manage.py database create

    # Login to your Mailgun account, and setup a SPAM catchall route with the
    # following properties:
    #
    #    Priority: 0
    #    Expression: match_header('X-Mailgun-SFlag', 'Yes')
    #    Action: forward("https://your-domain.com/spam"), stop()
    #    Description: Spam Management
    #
    # This route tells Mailgun to forward anything detected as SPAM to Spasm

    # In your Mailgun account, grab your API Key for the next step. It should
    # look like 'key-abcd1234'

    # Start the application, prefixing with the required environment variables
    API_KEY="secret_api_key" MAILGUN_API_KEY="key-abcd1234" python server.py
```

Heroku setup:
```bash
    # Clone the repo
    git clone git@github.com:taeram/spasm.git
    cd ./spasm

    # Create your Heroku app, and add a database addon
    heroku apps:create
    heroku addons:add heroku-postgresql

    # Promote your postgres database (your URL name may differ)
    heroku pg:promote HEROKU_POSTGRESQL_RED_URL

    # Set an "API key" for authorization
    heroku config:set API_KEY="secret_api_key"

    # Get your API Key from your Mailgun account
    heroku config:set MAILGUN_API_KEY="key-abcd1234"

    # Set the flask environment
    heroku config:set FLASK_ENV=production

    # Push to Heroku
    git push heroku master

    # Create the production database
    heroku run python manage.py database create
```

Usage
=====

To view a list of SPAM messages forwarded to you by Mailgun, open your browser
and visit `http://your-domain.com/list/<secret_api_key>`, where `<secret_api_key>`
is the `API_KEY` you setup when you deployed the application.

Using the SPAM catchall route, Mailgun will POST spam messages to
`http://your-domain.com/spam`. SPAM messages will then then be stored in the Spasm
database.

To get a list of all SPAM messages:
```bash
curl http://your-domain.com/spam -H "Authorization: secret_api_key"
```

To get the full text of an individual SPAM message:
```bash
curl http://your-domain.com/spam/0a1b2c3c4d -H "Authorization: secret_api_key"
```

To delete an individual SPAM message:
```bash
curl -X DELETE http://your-domain.com/spam/0a1b2c3c4d -H "Authorization: secret_api_key"
```

To delete all SPAM messages:
```bash
curl -X DELETE http://your-domain.com/spam/ -H "Authorization: secret_api_key"
```

To list all Mailgun routes:
```bash
curl http://your-domain.com/spam/routes/ -H "Authorization: secret_api_key"
```

To list an individual Mailgun routes:
```bash
curl http://your-domain.com/spam/routes/9a8b7c6d -H "Authorization: secret_api_key"
```

To create a Mailgun route to blacklist an email address:
```bash
curl -X POST http://your-domain.com/spam/routes/9a8b7c6d -H "Authorization: secret_api_key" -F "local=steve&domain=example.com"
```

To blacklist an email address regex:
```bash
curl -X POST http://your-domain.com/spam/routes/9a8b7c6d -H "Authorization: secret_api_key" -F "local=barbara(.*)&domain=example.com"
```

To blacklist an email address, and add a description to the route:
```bash
curl -X POST http://your-domain.com/spam/routes/9a8b7c6d -H "Authorization: secret_api_key" -F "local=scooter&domain=example.com&description=ih8scooter"
```
