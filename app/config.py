import os

from dotenv import load_dotenv

ENV = os.getenv("ENV", "dev")
load_dotenv(f".env.{ENV}", override=True)

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "")
AWS_USER_POOL_ID = os.getenv("AWS_USER_POOL_ID", "")
AWS_USER_POOL_CLIENT_ID = os.getenv("AWS_USER_POOL_CLIENT_ID", "")


DATABASE_URI = "mysql://{user}:{password}@{host}/{dbname}?charset=utf8".format(
    **{
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "dbname": os.getenv("MYSQL_DATABASE", ""),
    }
)

docs_settings = {
    "title": "PythonAPIドキュメント",
    "description": "PythonAPIサーバーテンプレート",
    "version": ENV,
    "openapi_tags": [
        {"name": "auth", "description": "認証関連"},
    ],
}
