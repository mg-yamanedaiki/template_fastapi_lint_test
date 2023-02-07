from uvicorn.workers import UvicornWorker


class Worker(UvicornWorker):
    CONFIG_KWARGS = {"log_config": "logging.yml"}
