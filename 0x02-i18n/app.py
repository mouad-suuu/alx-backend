#!/usr/bin/env python3
"""
8-app Module

Flask app with Babel setup, locale selection based on user preferences,
template parametrization, URL parameter locale support, user login emulation,
timezone inference, and current time display.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, get_timezone

import pytz
from datetime import datetime

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Retrieve user information based on user ID."""
    return users.get(user_id)


@app.before_request
def before_request():
    """Set the logged-in user globally on flask.g."""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """Determine the best match for the supported languages."""
    if 'locale' in request.args and \
            request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']
    elif g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    elif request.accept_languages.best_match(app.config['LANGUAGES']):
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Determine the best match for the supported timezones."""
    if 'timezone' in request.args:
        try:
            pytz.timezone(request.args['timezone'])
            return request.args['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Route to render index.html."""
    current_time = datetime.now(pytz.timezone(get_timezone())).strftime('%b %d, %Y, %I:%M:%S %p')
    return render_template('index.html', title=_('home_title'),
                           header=_('home_header'), current_time=current_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
