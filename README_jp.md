# ztask-cil

`ztask-cil` は、タスク管理を行うためのコマンドラインツールです。簡単にタスクを追加、一覧、更新、削除でき、マークダウンファイルを使用してタスクを同期します。
### プロジェクトディレクトリ構造

`ztask-cil` は、以下のような一般的な階層構造を持つプロジェクトディレクトリを前提としています。各タスクは、`yyyymmddHHMMss.md` という形式のマークダウンファイルとして保存され、プロジェクトごとにディレクトリが分けられています。

```bash
project_directory/
├── project_1/
│   ├── 20250122102434.md
│   ├── 20250122104555.md
│   └── 20250122104635.md
├── project_2/
│   ├── 20250117173019.md
│   ├── 20250117173521.md
│   └── 20250117173634.md
├── project_3/
│   ├── 20250120044018.md
│   └── 20250120045013.md
└── independent_tasks/
    ├── 20250121222746.md
    └── 20250122123059.md
```
ファイル名は`yyyymmddHHMMss.md`の形式で、作成日時が反映されたユニークなIDとなります。また、各タスクファイルの冒頭にはフロントマターが含まれています。
```yaml
---
title: Install ztask-cil tool
date: "yyyy-mm-dd"
id: yyyymmddHHMMss
status: "Not Started"
tags:
    - Task
---
```


## インストール

### Pythonのインストール
`ztask-cil` を実行するには、Pythonがインストールされている必要があります。Pythonがインストールされていない場合は、以下の手順でインストールできます。

#### MacOS
1. Homebrewを使ってPythonをインストールする（Homebrewがインストールされていない場合は、[公式サイト](https://brew.sh/)からインストールできます）：
    ```bash
    brew install python
    ```

2. インストール後、Pythonが正しくインストールされたことを確認します：
    ```bash
    python3 --version
    ```

#### Linux
1. `apt` を使用してインストール（UbuntuやDebianベースのディストリビューションの場合）：
    ```bash
    sudo apt update
    sudo apt install python3
    ```

   ```

### ztask-cliのダウンロード
最新の安定版をデスクトップまたはサーバーにダウンロードしてください。

#### MacOS

1. リポジトリをクローンします：
    ```bash
    git clone https://github.com/nakachan-ing/ztask-cil.git
    ```

2. `ztask-cil` のパスを環境変数に追加します（`zsh` を使用している場合）：
    ```bash
    echo 'export PATH="$HOME/path/to/ztask-cil:$PATH"' >> ~/.zshrc  # zshの場合
    ```

3. 設定を反映させるために、以下のコマンドで `zshrc` を再読み込みします：
    ```bash
    source ~/.zshrc
    ```

これで、`ztask` コマンドがターミナルで使用できるようになります。

### Pythonの仮想環境の設定

`ztask-cil` を仮想環境で使用する場合は、以下の手順を実行して仮想環境を作成し、必要なパッケージをインストールします。

#### 仮想環境の作成

1. 仮想環境の作成
   プロジェクトディレクトリに移動し、仮想環境を作成します：
   ```bash
   python3 -m venv venv
   ```
2. 仮想環境の有効化
    ```bash
    source venv/bin/activate
    ```
3. 依存パッケージをインストールするための `requirements.txt` を作成します：
    ```bash
    pip3 install -r requirements.txt
    ```
4. `requirements.txt` の内容は以下の通りです：
    ```text
    colorama
    pyyaml
    argparse
    ```
5. 仮想環境の無効化
   作業が終わったら仮想環境を無効化します
   ```bash
   deactivate

## 設定ファイル

`ztask-cil` を使用するには、設定ファイル（`config.yaml`）が必要です。設定項目は以下となります。

```yaml
projects_dir: "/path/to/your/projects_dir"
tasks_json: "/path/to/your/tasks.json"
```

## 使用例

`ztask-cil` の基本的なコマンドは以下の通りです。

### 1. `ztask sync`
マークダウンファイルからタスクを同期します。タスクの最新情報を取得するために使用します。

```bash
ztask sync
```

### 2. ztask list
現在のタスクを一覧表示します。

```bash
ztask list
```

### 3. ztask status
タスクのステータスを更新します。タスクIDと新しいステータスを指定します。

```bash
ztask status <task_id> <new_status>
```

### 4. ztask detele
タスクを削除します。削除したいタスクのIDを指定します。

```bash
ztask delete <task_id>
```

## Example
タスクの追加から削除までの一連の操作の例です。

1. タスクの追加:
```bash
ztask add "Complete project report"
```

2. タスクの一覧表示:
```bash
ztask list
```

3. タスクのステータス更新:
```bash
ztask status 1 "In Progress"
```

4. タスクの削除:
```bash
ztask delete 1
```

## Contributing
`ztask-cil`に貢献したい場合、プルリクエストを歓迎します！バグ修正、新機能の追加、ドキュメントの改善など、何でもお待ちしています。


## License
`ztask-cil`は[MIT License](https://opensource.org/licenses/mit-license.php)の下でライセンスされています。

