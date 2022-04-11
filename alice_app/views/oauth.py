import inject
from flask import Blueprint, request, render_template, redirect, jsonify
from alice_app.business.oauth_service import OAuthService

mod = Blueprint('oauth', __name__)

oauth_service = inject.instance(OAuthService)


@mod.route('/')
def index():
    response_type = request.args.get('response_type', '')
    client_id = request.args.get('client_id', '')
    redirect_uri = request.args.get('redirect_uri', '')
    scope = request.args.get('scope', '')
    state = request.args.get('state', '')

    return render_template(
        'oauth/index.html',
        response_type=response_type, client_id=client_id, redirect_uri=redirect_uri, scope=scope, state=state)


@mod.route('/authorization', methods=['POST'])
def authorization():
    login = request.form['login']
    password = request.form['password']
    response_type = request.form.get('response_type', '')
    client_id = request.form.get('client_id', '')
    redirect_uri = request.form.get('redirect_uri', '')
    scope = request.form.get('scope', '')
    state = request.form.get('state', '')

    auth_code = oauth_service.authorization(login, password, response_type, client_id, redirect_uri)
    if auth_code is None:
        return redirect(f'{redirect_uri}?error=invalid_request&state={state}')

    return redirect(f'{redirect_uri}?code={auth_code}&state={state}')


@mod.route('/token', methods=['POST'])
def get_token():
    grant_type = request.form.get('grant_type', '')
    code = request.form.get('code', '')
    refresh_token = request.form.get('refresh_token', '')
    redirect_uri = request.form.get('redirect_uri', '')
    client_id = request.form.get('client_id', '')
    client_secret = request.form.get('client_secret', '')

    access_token, refresh_token = oauth_service.grant_token(
        grant_type, code, refresh_token, client_id, client_secret, redirect_uri)
    if access_token is None:
        return jsonify(error="unauthorized_client")

    return jsonify(
        access_token=access_token,
        token_type="Bearer",
        expires_in=600,
        refresh_token=refresh_token
    )
