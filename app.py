import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import authorization

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@app.route('/')
def index():
    # TODO: If no auth token, then return the re-direct URL
    if not session.get("user"):
        return generate_redirect()
    return jsonify({"code": "AUTHORIZED", "message": "You are authorized"}), 200


def generate_redirect():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return jsonify({"code": "REDIRECT", "message": auth_url}), 200


@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    # TODO: Review and check the first condition about the state
    #if request.args.get('state') != session.get("state"):
    #    return jsonify({"code": "UNAUTHORIZED", "message": "You are unauthorized"}), 200
    if "error" in request.args:  # Authentication/Authorization failure
        return jsonify({"code": "AUTHORIZATION_FAILURE", "message": "Authentication/Authorization failure"}), 200
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return jsonify({"code": "GENERAL_ERROR", "message": result}), 200
        # TODO: Instead of handling sessions this way, please consider to use another mechanism for storing the JWT
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    # TODO: Instead of redirect to index again, should be redirected to /home, for example!
    return redirect(url_for("index"))


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


if __name__ == '__main__':
    app.run()
