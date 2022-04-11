import json

import inject
from flask import Blueprint, g, request, Response

from alice_app.business.oauth_service import OAuthService
from alice_app.business.smart_home_service import SmartHomeService

mod = Blueprint('smart_home', __name__)

oauth_service = inject.instance(OAuthService)
smart_home_service = inject.instance(SmartHomeService)


@mod.before_request
def add_is_authenticated():
    auth_header = request.headers.get('Authorization', '')
    parts = auth_header.split(' ')

    access_token = parts[1] if len(parts) == 2 else None
    if access_token is None:
        g.is_authenticated = False

    g.is_authenticated = oauth_service.check_access_token(access_token)
    g.access_token = access_token


@mod.route('/')
def index():
    return Response(status=200)


@mod.route('/user/devices')
def devices():
    if not g.is_authenticated:
        return Response(status=401, response="Invalid token")

    request_id = request.headers['X-Request-Id']
    res = smart_home_service.get_devices(request_id)
    return json.dumps(res)


@mod.route('/user/devices/query', methods=['POST'])
def query():
    if not g.is_authenticated:
        return Response(status=401, response="Invalid token")

    request_id = request.headers['X-Request-Id']
    data = request.json
    res = smart_home_service.query_devices(request_id, data)
    return json.dumps(res)


@mod.route('/user/devices/action', methods=['POST'])
def action():
    if not g.is_authenticated:
        return Response(status=401, response="Invalid token")

    request_id = request.headers['X-Request-Id']
    data = request.json
    res = smart_home_service.action_devices(request_id, data)
    return json.dumps(res)


@mod.route('/user/unlink', methods=['POST'])
def unlink():
    if not g.is_authenticated:
        return Response(status=401, response="Invalid token")

    oauth_service.unlink(g.access_token)

    return Response(status=200)
