import os
import json
import yaml
from datetime import date, datetime
from colorama import Fore, Style, init
import sys
from collections import OrderedDict
import argparse

# 実行しているPythonスクリプトの絶対パスを取得
script_path = os.path.abspath(__file__)

# 実行しているスクリプトのディレクトリを取得
script_dir = os.path.dirname(script_path)

# config.yaml のパスを結合
config_path = os.path.join(script_dir, 'config.yaml')

# tasks.json のパスを結合
task_json = os.path.join(script_dir, 'tasks.json')

# カスタムエンコーダを定義
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # ISO形式で日付を文字列に変換
        return super().default(obj)


init(autoreset=True)  # 自動的に色をリセット


def load_config():
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def load_tasks():
    if os.path.exists(task_json) and os.path.getsize(task_json) > 0:
        with open(task_json, 'r') as tasks_file:
            return json.load(tasks_file)
    return []  # tasks.jsonが存在しないか、空の場合は空のリストを返す


def save_tasks(tasks):
    # date型を文字列に変換するカスタムエンコーダー
    def custom_encoder(obj):
        if isinstance(obj, date):
            return obj.isoformat()  # 日付を "YYYY-MM-DD" 形式の文字列に変換
        raise TypeError(f"Type {type(obj)} not serializable")
    
    with open(task_json, 'w', encoding='utf-8') as tasks_file:
        json.dump(tasks, tasks_file, indent=2, ensure_ascii=False, default=custom_encoder)


def sync_project():
    config = load_config()
    project_dir = config.get('projects_dir')

    if not project_dir or not os.path.isdir(project_dir):
        print("Error: Invalid project directory in config.yaml")
        return

    # 既存のtasks.jsonをロード
    existing_tasks = {}
    if os.path.exists(task_json):
        with open(task_json, 'r', encoding='utf-8') as f:
            try:
                existing_tasks = {task['title']: task for task in json.load(f)}
            except json.JSONDecodeError:
                print("Error: tasks.json could not be parsed. Starting fresh.")

    new_tasks = []
    task_counter = len(existing_tasks)  # 既存タスクの数をカウント

    for subdir, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)

                # フロントマターの抽出
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if len(lines) < 2 or not lines[0].strip() == "---":
                    print(f"Skipping file (no frontmatter): {file_path}")
                    continue

                try:
                    # フロントマター部分の抽出
                    frontmatter_lines = []
                    for line in lines[1:]:
                        if line.strip() == "---":
                            break
                        frontmatter_lines.append(line)
                    
                    frontmatter_content = "".join(frontmatter_lines)
                    task_data = yaml.safe_load(frontmatter_content)

                    if task_data and 'tags' in task_data and 'Task' in task_data['tags']:
                        title = task_data.get('title', 'Untitled Task')
                        
                        # 既存のタスクか確認
                        if title in existing_tasks:
                            task = existing_tasks[title]
                            # print(f"Task already exists: {task['title']} (taskId: {task['taskId']})")
                            task['file'] = file_path
                        else:
                            # 新しいタスクとして追加
                            task_counter += 1
                            task_data['taskId'] = task_counter
                            task_data['file'] = file_path  # ファイルパスを格納
                            new_tasks.append(task_data)
                            # print(f"New task added: {task_data['title']} (taskId: {task_data['taskId']})")

                    else:
                        # print(f"No 'Task' tag in file: {file_path}")
                        pass

                except yaml.YAMLError as e:
                    pass
                    # print(f"YAML parsing error in {file_path}: {e}")
                except Exception as e:
                    pass
                    # print(f"Unexpected error processing {file_path}: {e}")

    # 既存タスクと新タスクを結合
    all_tasks = list(existing_tasks.values()) + new_tasks

    # JSONファイルに保存
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(all_tasks, f, ensure_ascii=False, indent=4, cls=DateEncoder) 

    print(f"Sync complete: {len(new_tasks)} new tasks found, total {len(all_tasks)} tasks.")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print(Fore.RED + "No tasks available." + Fore.RESET)
        return

    # タスクの表示準備
    shown_count = 0
    print(
        f"{Fore.GREEN}{'Task ID':<10}"  # Task IDヘッダー
        f"{'Title':<50}"               # タイトルヘッダー
        f"{'Project':<30}"           # ディレクトリヘッダー
        f"{'Status':<15}"              # ステータスヘッダー
        + Fore.RESET
    )
    print("-" * 105)  # セクションの区切り線

    for task in tasks:
        if task['status'] != 'Done':  # 完了済みのタスクを除外
            # ステータスに応じた色分け
            status_color = {
                'Not started': Fore.RED,
                'In progress': Fore.YELLOW,
                'Waiting': Fore.MAGENTA,
                'On hold': Fore.BLUE,
                'Done': Fore.GREEN,
            }.get(task['status'], Fore.WHITE)  # デフォルトは白

            # ディレクトリ名の抽出
            directory_name = os.path.basename(os.path.dirname(task['file']))

            # タスクの出力
            print(
                f"{Fore.GREEN}{task['taskId']:<10}"  # Task ID (緑)
                f"{Fore.WHITE}{task['title']:<50}"  # Title (白)
                f"{Fore.CYAN}{directory_name:<30}"  # Directory (青)
                f"{status_color}{task['status']:<15}"  # Status (色分け)
                + Fore.RESET
            )
            shown_count += 1

    # 合計タスク数の表示
    total_count = len(tasks)
    print(Fore.GREEN + "--")
    print(f"TODO: {shown_count} of {total_count} tasks shown" + Fore.RESET)



def update_task_status(task_id, new_status):
    """タスクのステータスを更新し、tasks.jsonとMarkdownファイルを修正"""
    # 有効なステータスを定義
    valid_statuses = ["Not started", "In progress", "Waiting", "Done", "On hold"]
    
    if new_status not in valid_statuses:
        print(Fore.RED + f"Invalid status: {new_status}. Valid statuses are: {', '.join(valid_statuses)}")
        return

    tasks = load_tasks()
    task_found = False

    for task in tasks:
        if task["taskId"] == int(task_id):
            task_found = True
            old_status = task["status"]
            task["status"] = new_status
            print(Fore.CYAN + f"Task {task_id} status updated from '{old_status}' to '{new_status}'.")

            # Markdownファイルの更新
            markdown_file_path = task["file"]
            update_markdown_status(markdown_file_path, new_status)
            break

    if not task_found:
        print(Fore.RED + f"Task with ID {task_id} not found.")
        return

    # tasks.jsonを保存
    save_tasks(tasks)


def update_markdown_status(file_path, new_status):
    """Markdownファイルのステータスを更新"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(file_path, "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith("status:"):
                    file.write(f"status: {new_status}\n")
                else:
                    file.write(line)
        print(Fore.GREEN + f"Updated status in Markdown file: {file_path}")

    except FileNotFoundError:
        print(Fore.RED + f"Markdown file not found: {file_path}")
    except Exception as e:
        print(Fore.RED + f"Error updating Markdown file: {e}")


def list_subdirectories(directory):
    """指定されたディレクトリ内のサブディレクトリをリストアップする"""
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]


def select_subdirectory(subdirectories):
    """サブディレクトリをユーザーに選択させる"""
    print(Fore.CYAN + "Select a subdirectory:")
    for idx, subdir in enumerate(subdirectories, start=1):
        print(f"{idx}. {subdir}")
    
    while True:
        try:
            choice = int(input(Fore.YELLOW + "Enter the number of your choice: ")) - 1
            if 0 <= choice < len(subdirectories):
                return subdirectories[choice]
            else:
                print(Fore.RED + "Invalid choice. Please select a valid number.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")


def generate_task_id(tasks):
    """新しい taskId を生成する関数"""
    if not tasks:
        return 1  # タスクがない場合は 1 からスタート
    return max(task['taskId'] for task in tasks) + 1


def add_task(title):
    config = load_config()
    project_dir = config.get('projects_dir')

    if not project_dir or not os.path.isdir(project_dir):
        print(Fore.RED + "Error: Invalid project directory in config.yaml")
        return

    # プロジェクトディレクトリ内のサブディレクトリをリストアップ
    subdirectories = list_subdirectories(project_dir)
    if not subdirectories:
        print(Fore.RED + "Error: No subdirectories found in the project directory.")
        return

    # ユーザーにサブディレクトリを選択させる
    selected_dir = select_subdirectory(subdirectories)
    task_dir = os.path.join(project_dir, selected_dir)

    # タスクのIDとして現在の日時を使用 (yyyymmddHHMMss形式)
    file_id = int(datetime.now().strftime('%Y%m%d%H%M%S'))

    # タスクのフロントマターを作成
    frontmatter = {
        'title': title,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'id': file_id,
        'status': 'Not started',
        'tags': ['Task']
    }

    # 選択されたサブディレクトリにMarkdownファイルを保存
    task_file_path = os.path.join(task_dir, f"{file_id}.md")

    with open(task_file_path, 'w', encoding='utf-8') as task_file:
        task_file.write('---\n')
        yaml.dump(frontmatter, task_file, default_flow_style=False, allow_unicode=True)
        task_file.write('---\n\n')

    # 新しいタスクをtasks.jsonに追加
    tasks = load_tasks()
    # 新しい taskId を生成
    task_id = generate_task_id(tasks)
    new_task = {
        'title': title,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'id': file_id,
        'status': "Not started",
        'tags': "Task",
        'taskId': task_id,
        'file_path': task_file_path
    }
    tasks.append(new_task)

    save_tasks(tasks)

    print(Fore.GREEN + f"New task added: {title} (taskId: {task_id})")
    print(f"Markdown file created at: {task_file_path}")
    print(f"Task added to tasks.json")


def delete_task(task_id):
    """
    指定された taskId に基づき、Markdownファイルと tasks.json からタスクを削除する。
    """
    config = load_config()
    project_dir = config.get('projects_dir')
    tasks_file=config.get('tasks_json')

    if not project_dir or not os.path.isdir(project_dir):
        print(Fore.RED + "Error: Invalid project directory in config.yaml")
        return

    # tasks.json のパスを取得
    # tasks_file = os.path.join(project_dir, 'tasks.json')
    if not os.path.exists(tasks_file):
        print(Fore.RED + "Error: tasks.json not found.")
        return

    # tasks.json を読み込む
    with open(tasks_file, 'r', encoding='utf-8') as file:
        tasks = json.load(file)

    # taskId に該当するタスクを探す
    task_to_delete = next((task for task in tasks if task['taskId'] == int(task_id)), None)

    if not task_to_delete:
        print(Fore.RED + f"Error: Task with taskId {task_id} not found.")
        return

    # Markdown ファイルを削除
    file_path = task_to_delete.get('file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        print(Fore.GREEN + f"Markdown file deleted: {file_path}")
    else:
        print(Fore.YELLOW + f"Warning: Markdown file not found for taskId {task_id}.")

    # tasks.json からタスクを削除
    updated_tasks = [task for task in tasks if task['taskId'] != int(task_id)]
    with open(tasks_file, 'w', encoding='utf-8') as file:
        json.dump(updated_tasks, file, indent=4, ensure_ascii=False)

    print(Fore.GREEN + f"Task with taskId {task_id} deleted from tasks.json.")


def main():
    parser = argparse.ArgumentParser(description="Task management CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # ztask sync コマンド
    sync_parser = subparsers.add_parser("sync", help="Sync tasks from markdown files")

    # ztask list コマンド
    subparsers.add_parser("list", help="List all tasks")

    # ztask add コマンド
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task_title", help="Title of the task to add")

    # ztask status コマンド
    status_parser = subparsers.add_parser("status", help="Update the status of a task")
    status_parser.add_argument("task_id", help="ID of the task to update")
    status_parser.add_argument("new_status", help="New status of the task")

    # ztask delete コマンド
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="ID of the task to delete")

    # 引数を解析
    args = parser.parse_args()

    # コマンドに応じた処理を呼び出し
    if args.command == "sync":
        sync_project()
    elif args.command == "list":
        list_tasks()
    elif args.command == "add":
        add_task(args.task_title)
    elif args.command == "status":
        update_task_status(args.task_id, args.new_status)
    elif args.command == "delete":
        delete_task(args.task_id)
    else:
        print(Fore.RED + f"Unknown command: {args.command}")


if __name__ == '__main__':
    main()