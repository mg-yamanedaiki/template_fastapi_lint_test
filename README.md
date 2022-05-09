# atd_00_template_api_python

[DB構成](docs/db/README.md)

## Requirement

- Docker
- Docker Compose v2

## 環境構築

**※ 以下はリモートコンテナー利用の場合の手順です**

### DBセットアップ

```shell
poetry install # パッケージのインストール
poetry shell # 仮想環境に入る
inv migrate # マイグレーション実行
inv seed
inv test-init # 最初の一回だけでいいです
inv test # テスト実行
```

**以下のコマンドで使えるコマンドが見れます**

```shell
inv --list
```

※Python仮想環境内で実行してください

**RemoteContainer**

RemoteContainer を使用すれば EditorConfig などの拡張機能が自動でインストールされるので使用することをおすすめします。
RemoteContainer 拡張機能をインストールしていれば、VSCode を開いた時に以下のようなメッセージが表示されると思うので、`Reopen in Container`ボタンをクリックで使用できます。

```txt
Folder contains a Dev Container configuration file. Reopen folder to develop in a container (learn more).
```

その他にもコマンドパレットから`Reopen in Container`を選択することでも開くことができます。
