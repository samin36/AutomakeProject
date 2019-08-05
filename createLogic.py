import os
import subprocess
from github import Github, GithubException
import platform

class CreateProject():
    """ Class to automatically create a folder and upload to github """

    def __init__(self):
        self.proj_name = None
        self.readme = None
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
            self.github_obj.get_user().id
            print([key for key in self.github_obj.get_user().get_keys()])
            return True
        except GithubException:
            return False

    def setup_project(self, proj_name, readme="", mode="PRIVATE", upload=False, directory=os.getcwd(), open_project=True):
        """
        Takes in the project name, readme, mode (private or public),
        a boolean variable upload (True=upload to github, False=otherwise),
        and the directory.

        It return a tuple of the message and error code depending on whether the
        directory is succesfully created and project is pushed to Github
        -> Success returns: (success_msg, 0)
        -> Failure returns: (fial_msg, 1)

        """
        self.proj_name = proj_name.strip()
        self.readme = readme.strip()
        self.private_mode = True if mode.upper() == "PRIVATE" else False
        self.upload = upload
        self.directory = directory.strip()
        self.open_project = open_project

        try:
            self.create_directory()
            return ("Project created successfully!", 0)
        except OSError as e:
            return ("Please make sure the directory path is correct", 1)

    def create_directory(self):
        """ Creates a directory based on proj_name """
        if self.proj_name:
            os.chdir(self.directory)
            os.mkdir(self.proj_name)
            os.chdir(f"./{self.proj_name}")

            if self.upload:
                self.setup_github_repo()
            if self.open_project:
                result = subprocess.call("code .", shell=True)
                if result == 1:
                    if platform.system() == 'Windows':
                        subprocess.call("explorer .", shell=True)
                    elif platform.system() == 'Darwin':
                        #Darwin == Mac OS
                        subprocess.call("open .", shell=True)

    def verify_directory(self):
        """ Verifies directory before creating the project """
        return os.path.isdir(self.directory)


    def setup_github_repo(self):
        """ Sets up a github repository for the project using the PyGithub
            module:
            1) Adds a readme
            2) Adds project readme
            3) Configures the mode: Public or Private
        """
        self.readme = self.readme.replace("\n", " & echo ")
        self.git_command(f'(echo {self.readme}) >> README.md')
        self.git_command("git init")

        repo = self.github_obj.get_user().create_repo(
            name=self.proj_name,
            private=self.private_mode,
        )
        url = repo.html_url
        self.git_command(f"git remote add origin {url}")
        self.git_command("git add .")
        self.git_command('git commit -m "Initial Commit"')
        self.git_command("git push -u origin master")
        self.git_command(f"start /max {url}")

    def git_command(self, command):
        """ Helper method that executes commands in bash shell """
        return subprocess.run(command, shell=True)
