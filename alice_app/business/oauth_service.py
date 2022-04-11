import inject
import string
import random

from alice_app import config
from alice_app.business.token_service import TokenService
from alice_app.domain.token import Token


class OAuthService:
    login_by_code_cache = dict()
    token_service = inject.attr(TokenService)

    def authorization(self, login: str, password: str, response_type: str,
                      client_id: str, redirect_uri: str) -> str:
        if client_id != config.CLIENT_ID or\
                redirect_uri != config.REDIRECT_URI:
            return None

        if login != config.LOGIN or\
                password != config.PASSWORD:
            return None

        if response_type == 'code':
            code = self._generate_code()
            self.login_by_code_cache[code] = login
            return code

        return None

    def grant_token(self, grant_type: str, code: str, refresh_token: str,
                    client_id: str, client_secret: str, redirect_uri: str) -> (str, str):
        if client_id != config.CLIENT_ID:
            return None

        if grant_type == 'authorization_code':
            return self._create_token_by_code(code) if redirect_uri == config.REDIRECT_URI else None

        if grant_type == 'refresh_token':
            return self._refresh_token(refresh_token) if client_secret == config.CLIENT_SECRET else None

        return None, None

    def check_access_token(self, access_token: str) -> str:
        token = self.token_service.get_by_access_token(access_token)
        return token is not None

    def unlink(self, access_token: str):
        self.token_service.delete_by_access_token(access_token)

    @staticmethod
    def _generate_code() -> str:
        return ''.join(random.choice(string.digits + string.ascii_letters) for i in range(20))

    def _create_token_by_code(self, code: str) -> (str, str):
        login = self.login_by_code_cache.pop(code, None)
        if login is None:
            return None, None

        access_token = self._generate_code()
        refresh_token = self._generate_code()

        token = self.token_service.get_by_login(login)
        if token is None:
            token = Token(0, login, access_token, refresh_token)
        else:
            token.access_token = access_token
            token.refresh_token = refresh_token

        self.token_service.save(token)

        return access_token, refresh_token

    def _refresh_token(self, refresh_token: str) -> (str, str):
        token = self.token_service.get_by_refresh_token(refresh_token)
        if token is not None:
            token.access_token = self._generate_code()
            token.refresh_token = self._generate_code()

            self.token_service.save(token)

            return token.access_token, token.refresh_token

        return None, None
