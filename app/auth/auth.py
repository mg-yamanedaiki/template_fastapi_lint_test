from app import config
from cognito_pyauth import Auth, Config

auth = Auth(
    Config(
        region=config.AWS_DEFAULT_REGION,
        pool_id=config.AWS_USER_POOL_ID,
        client_id=config.AWS_USER_POOL_CLIENT_ID,
    )
)
