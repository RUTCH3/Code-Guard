from datetime import datetime
from typing import List
import json
import click
import os
from Classes import Repository, File, Commit
import shutil


class CLI:
    @staticmethod
    def load_repo():
        if os.path.exists('repo.json'):
            with open('repo.json', 'r') as f:
                data = json.load(f)
                return Repository(data['name_repo'])
        return None

    @staticmethod
    def save_repo(repo: Repository):
        if repo is not None:
            with open('repo.json', 'w') as f:
                json.dump({'name_repo': repo.name_repo,
                           'list_commits': [CLI.commit_to_dict(commit) for commit in repo.list_commits]}, f)

    @staticmethod
    @click.command()
    @click.option("--name", prompt="Enter command (e.g., wit init, wit add<file_name>)", help="The command to execute.")
    def get_command(name: str):
        if name == "wit init":
            CLI.wit_init()
        elif name.startswith("wit add"):
            files_name = name.split("wit add", 1)[1].strip()
            list_files = files_name.split()
            CLI.wit_add(list_files)
        elif name.startswith("wit commit -m"):
            message = name.split("wit add -m", 1)[0].strip()
            CLI.wit_commit(message)
        else:
            click.echo("This command is not valid.")

    @staticmethod
    def wit_init():
        if not os.path.exists(".wit"):
            os.mkdir(".wit")
            click.echo("Hello, the directory created successfully!")
            CLI.create_repo()
        else:
            click.echo("The directory '.wit' already exists.")

    @staticmethod
    def create_repo():
        repo_name = click.prompt("Enter the repository name", type=str)
        repo = Repository(repo_name)
        CLI.save_repo(repo)
        repo_path = os.path.join(".wit", repo_name)
        if not os.path.exists(repo_path):
            os.mkdir(repo_path)
            click.echo(f"Repository '{repo_name}' created successfully!")
        else:
            click.echo(f"The repository '{repo_name}' already exists.")
        stage = os.path.join(repo_path, "Staging")
        click.echo(stage)
        if not os.path.exists(stage):
            os.mkdir(stage)
            click.echo("Directory Staging created successfully.")
        commit = os.path.join(repo_path, "Commited")
        click.echo(commit)
        if not os.path.exists(commit):
            os.mkdir(commit)
            click.echo("Directory Commited created successfully.")

    @staticmethod
    def wit_add(files: List[str]):
        """Add the selected files to the staging list.
        and copy them to directory named 'Staging'."""
        repo = CLI.load_repo()
        if repo is None:
            raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")
        if files[0] == "":
            raise Exception("Command not valid.")
        else:
            try:
                CLI.copy_files(os.getcwd(), f'.wit/{str(repo.name_repo)}/Staging', files)
                for file in os.listdir(os.getcwd()):
                    new_file = File(file, f'.wit/{str(repo.name_repo)}/Staging')
                    repo.staging.append(new_file)
                    print(new_file)
                for _ in repo.staging:
                    print(_)
            except Exception as e:
                click.echo(f"This files already exists.{e}")

    @staticmethod
    def copy_files(source_dir, dest_dir, files: List[str]):
        if not os.path.exists(source_dir):
            raise Exception("Source directory does not exist.")

        try:
            if not os.path.exists(dest_dir):
                raise Exception("Error: Repository is not initialized. Please run 'wit init' first.")
        except Exception as e:
            click.echo(e)

        if files[0] == '.':
            for filename in os.listdir(source_dir):
                full_file_name = os.path.join(source_dir, filename)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, dest_dir)
        else:
            for filename in os.listdir(source_dir):
                full_file_name = os.path.join(source_dir, filename)
                if os.path.isfile(full_file_name) and os.path.basename(full_file_name) in files:
                    shutil.copy(full_file_name, dest_dir)

    @staticmethod
    def wit_commit(message=""):
        try:
            repo = CLI.load_repo()
            staged = f'.wit/{str(repo.name_repo)}/Staging/'
            list_files = os.listdir(staged)
            new_commit = Commit(message, list_files)
            repo.list_commits.append(new_commit)

            repo_path = f'.wit/{str(repo.name_repo)}/Commited'
            date_dir = os.path.join(repo_path, f"{datetime.now().strftime("%d_%m_%Y")}")

            click.echo(date_dir)

            if not os.path.exists(date_dir):
                os.mkdir(date_dir)
                click.echo("Directory date created successfully.")
                click.echo(date_dir)

            id_commit = os.path.join(date_dir, str(new_commit.commit_id))
            if not os.path.exists(id_commit):
                os.mkdir(id_commit)
                click.echo(f"Directory id {id_commit} created successfully.")
            CLI.copy_files(staged, id_commit, list_files)
            CLI.save_repo(repo)

        except Exception as e:
            click.echo(e)

    @staticmethod
    def commit_to_dict(commit: Commit):
        return {
            'commit_id': commit.commit_id,
            'message': commit.message,
            'date': commit.date,
            'list_files': [file.name for file in commit.list_files]
        }

    @staticmethod
    def wit_status():
        pass

    @staticmethod
    def wit_log():
        pass

    @staticmethod
    def wit_checkout(id_repo):
        pass


if __name__ == "__main__":
    CLI.get_command()
