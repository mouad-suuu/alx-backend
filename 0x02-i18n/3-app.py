#!/usr/bin/env python3
"""
3-app Module

Flask app with Babel setup for handling localization. The Babel extension is configured to support English and French languages, with English as the default. This module uses the _ function (alias for gettext) to fetch localized text based on the user's locale. It helps in rendering templates with language-specific content.

The locale is determined dynamically based on the client's request headers, prioritizing the languages configured in the app.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _   # _ is an alias for gettext, used for fetching localized text

app = Flask(__name__)
babel = Babel(app)

class Config:
    """Configuration class for Flask app with localization settings."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

@babel.localeselector
def get_locale():
    """Select the best matching language from client request."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Home page route using localized text for title and header."""
    return render_template('3-index.html', title=_('home_title'), header=_('home_header'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
