# ztask-cli

`ztask-cli` is a command-line tool for task management. It allows you to easily add, list, update, and delete tasks while syncing tasks using markdown files.

---

### Project Directory Structure

`ztask-cli` assumes a typical project directory structure like the one shown below. Each task is stored as a markdown file in the format `yyyymmddHHMMss.md`, and tasks are organized into separate directories for each project.

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

The file name format `yyyymmddHHMMss.md` reflects the unique ID based on the creation timestamp. Each task file also includes frontmatter at the beginning:

```yaml
---
title: Install ztask-cli tool
date: "yyyy-mm-dd"
id: yyyymmddHHMMss
status: "Not Started"
tags:
    - Task
---
```

---

## Installation

### Installing Python

To run `ztask-cli`, Python must be installed on your system. If Python is not already installed, follow the steps below to install it.

#### MacOS

1. Use Homebrew to install Python (if Homebrew is not installed, you can install it from the [official website](https://brew.sh/)):
    ```bash
    brew install python
    ```

2. Verify that Python has been installed correctly:
    ```bash
    python3 --version
    ```

#### Linux

1. Use `apt` to install Python (for Ubuntu or Debian-based distributions):
    ```bash
    sudo apt update
    sudo apt install python3
    ```

Let me know if you need further adjustments!

### Downloading ztask-cli
Download the latest stable version to your desktop or server.

#### MacOS

1. Clone the repository:
    ```bash
    git clone https://github.com/nakachan-ing/ztask-cli.git
    ```

2. Add the `ztask-cli` path to your environment variables (for `zsh` users):
    ```bash
    echo 'export PATH="$HOME/path/to/ztask-cli:$PATH"' >> ~/.zshrc
    ```

3. Reload the `zshrc` configuration to apply the changes:
    ```bash
    source ~/.zshrc
    ```

Now you can use the `ztask` command from your terminal.

---

### Setting up a Python Virtual Environment

If you want to use `ztask-cli` in a virtual environment, follow these steps to create the environment and install the required packages.

#### Creating a Virtual Environment

1. Create a virtual environment:
   Navigate to your project directory and create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
3. Install the required dependencies by creating a `requirements.txt` file:
    ```bash
    pip3 install -r requirements.txt
    ```
4. The `requirements.txt` file should contain the following:
    ```text
    colorama
    pyyaml
    argparse
    ```
5. Deactivate the virtual environment:
   Once your work is done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

---

### Configuration File

To use `ztask-cli`, you need a configuration file (`config.yaml`). The configuration includes the following items:

```yaml
projects_dir: "/path/to/your/projects_dir"
tasks_json: "/path/to/your/tasks.json"
```

---

### Usage

Here are the basic commands for `ztask-cli`:

#### 1. `ztask sync`
Sync tasks from markdown files. Use this command to get the latest task updates.

```bash
ztask sync
```

#### 2. `ztask list`
Display the current list of tasks.

```bash
ztask list
```

#### 3. `ztask status`
Update the status of a task by specifying the task ID and the new status.

```bash
ztask status <task_id> <new_status>
```

#### 4. `ztask delete`
Delete a task by specifying the task ID.

```bash
ztask delete <task_id>
```

---

### Example

Here’s an example of a typical workflow with `ztask-cli`:

1. Add a new task:
    ```bash
    ztask add "Complete project report"
    ```

2. Display the list of tasks:
    ```bash
    ztask list
    ```

3. Update the status of a task:
    ```bash
    ztask status 1 "In Progress"
    ```

4. Delete a task:
    ```bash
    ztask delete 1
    ```

---

### Contributing

We welcome contributions to `ztask-cli`! Whether it's fixing bugs, adding new features, or improving the documentation, feel free to submit a pull request.

---

### License

`ztask-cli` is licensed under the [MIT License](https://opensource.org/licenses/mit-license.php). 

--- 

Let me know if you'd like further refinements!