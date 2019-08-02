import os
import subprocess
from github import Github, GithubException
from time import sleep

class CreateProject():
    """ Class to automatically create a folder and upload to github """

    def __init__(self):
        self.proj_name = None
        self.description = None
        self.private_mode = None
        self.upload = None
        self.github_obj = None
        self.directory = os.getcwd()
        self.open_project = None

    def login_successful(self, username, password):
        """ Verifies github auth key by logging in
            Returns True if successful else False
        """
        try:
            self.github_obj = Github(username.strip(), password.strip())
            return True
        except GithubException:
            return False

    def setup_project(self, proj_name, description="", mode="PRIVATE", upload=False, directory=os.getcwd(), open_project=True):
        """
        Takes in the project name, description, mode (private or public),
        a boolean variable upload (True=upload to github, False=otherwise),
        and the directory
        """
        self.proj_name = proj_name.strip()
        self.description = description.strip()
        self.private_mode = True if mode.upper() == "PRIVATE" else False
        self.upload = upload
        self.directory = directory.strip()
        self.open_project = open_project

        self.create_directory()

    def create_directory(self):
        """ Creates a directory based on proj_name """
        if self.proj_name:
            os.chdir(self.directory)
            os.mkdir(self.proj_name)
            os.chdir(f"./{self.proj_name}")
            if self.upload:
                self.setup_github_repo()
            if self.open_project:
                subprocess.call("code .", shell=True)

    def setup_github_repo(self):
        """ Sets up a github repository for the project using the PyGithub
            module:
            1) Adds a readme
            2) Adds project description
            3) Configures the mode: Public or Private
        """
        self.git_command(f'echo {self.description} >> README.md')
        self.git_command("git init")

        repo = self.github_obj.get_user().create_repo(
            name=self.proj_name,
            private=self.private_mode,
            description=self.description
        )
        url = repo.html_url
        self.git_command(f"git remote add origin {url}")
        self.git_command("git add .")
        self.git_command('git commit -m "Initial Commit"')
        self.git_command("git push -u origin master")
        self.git_command(f"start /max {url}")

    def git_command(self, command):
        """ Helper method that executes commands in bash shell """
        subprocess.run(command, shell=True)
