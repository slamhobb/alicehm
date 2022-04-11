from alice_app import create_app
from alice_app.dao.base_dao import BaseDao

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")


def init_db():
    with app.app_context():
        dao = BaseDao()
        with app.open_resource('schema.sql', mode='r') as f:
            dao.executescript(f.read())
