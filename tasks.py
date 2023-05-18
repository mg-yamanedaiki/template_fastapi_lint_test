# type: ignore

import subprocess
import sys
from typing import Union

from invoke import task


@task
def serve(c, port=8000, prod=False, path="app.main:app"):
    """サーバーを起動"""
    if prod:
        run(
            [
                f"gunicorn {path}",
                "-w 4",
                "-k app.worker.Worker",
                f"-b 0.0.0.0:{port}",
            ]
        )
    else:
        run(
            [
                f"uvicorn {path} --port {port}",
                "--reload --reload-dir app",
                "--log-config logging.yml",
                "--host 0.0.0.0",
            ]
        )


@task
def migrate(c):
    """テーブルを作成"""
    run("alembic upgrade head")


@task
def seed(c):
    """データを作成"""
    from db.seeds import database

    database.run()
    command = 'echo "\e[1;92m$(figlet success)\e[0m"'  # noqa: W605
    run(command, out=False)


@task
def er_update(c):
    """ER図を更新"""
    run("tbls doc -f")


@task
def db_refresh(c, yes=False, migrate_=False, seed_=False):
    """DBの初期化(リセット)"""
    if not yes:
        print("これを実行するとDBの情報が削除されます。")
        if "y" != input("本当によろしいですか?(y/n)"):
            return
    login_cmd = "mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD"
    run(f'echo "drop database $MYSQL_DATABASE;" | {login_cmd}')
    run(f'echo "create database $MYSQL_DATABASE;" | {login_cmd}')

    if migrate_:
        migrate(c)

    if seed_:
        seed(c)


@task
def lint(c, path="app"):
    """コードチェック"""
    run(f"poetry run mypy {path}")


@task
def clear(c, all=False, mypy=False, pytest=False):
    """キャッシュを削除"""
    caches = ["__pycache__"]
    mypy_cache_name = ".mypy_cache"
    pytest_cache_name = ".pytest_cache"
    if all:
        caches.append(mypy_cache_name)
        caches.append(pytest_cache_name)
    elif mypy:
        caches.append(mypy_cache_name)
    elif pytest:
        caches.append(pytest_cache_name)

    run(f'find . | grep -E "({"|".join(caches)}$)" | xargs rm -rf')


@task
def test(
    c,
    all=False,
    file="tests/app/",
    verbose=False,
    duration=False,
    coverage=False,
):
    """テストを実行"""
    cmd = [
        "ENV=test",
        "poetry run pytest",
        file,
        "--log-cli-level=DEBUG",
    ]
    if all or duration:
        cmd.append("--durations=0 -vv")
    if all or coverage:
        cmd.append("--cov=app --cov-report=term-missing")
    if all or verbose:
        cmd.append("--verbose")

    run(cmd)


@task
def test_init(c):
    """テスト用DBの初期化(リセット)"""
    TEST_DB_NAME = "atd_00_template_api_python_test"

    login_cmd = "mysql -h $MYSQL_HOST -u root -p$MYSQL_PASSWORD"
    run(f'echo "drop database {TEST_DB_NAME};" | {login_cmd}', ignore=True)
    print("[Can't drop database]←のエラーが出ても気にしなくて大丈夫です")
    run(f'echo "create database {TEST_DB_NAME};" | {login_cmd}')

    run("ENV=test inv migrate")


def run(cmd: Union[str, list], out: bool = True, ignore: bool = False) -> None:
    cmd_type = type(cmd)

    inner_cmd = ""
    if cmd_type is str:
        inner_cmd = str(cmd)
    elif cmd_type is list:
        inner_cmd = " ".join(cmd)
    else:
        raise Exception("引数cmdの型は[str|list]です")

    if out:
        print(f"\033[32mrun cmd\033[0m: {inner_cmd}")

    result = subprocess.run(inner_cmd, shell=True)

    if ignore:
        return
    if result.returncode != 0:
        sys.exit(result.returncode)
