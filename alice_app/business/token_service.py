import inject

from alice_app.dao.token.token_dao import TokenDao
from alice_app.domain.token import Token


class TokenService:
    token_dao = inject.attr(TokenDao)

    def get_by_login(self, login: str) -> Token:
        return self.token_dao.get_by_login(login)

    def get_by_access_token(self, access_token: str) -> Token:
        return self.token_dao.get_by_access_token(access_token)

    def get_by_refresh_token(self, refresh_token: str) -> Token:
        return self.token_dao.get_by_refresh_token(refresh_token)

    def save(self, token: Token) -> int:
        if token.id == 0:
            return self.token_dao.insert(token)

        return self.token_dao.update(token)

    def delete_by_access_token(self, access_token: str):
        token = self.token_dao.get_by_access_token(access_token)
        if token is None:
            return

        self.token_dao.delete(token.id)
