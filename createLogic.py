import os
import subprocess
from github import Github
from time import sleep

class CreateProject():
    """ Class to automatically create a folder and upload to github """

    def __init__(self):
        self.proj_name = None
        self.description = None
        self.mode = None
        self.push = None
        self.github_repo = None

    def verify_github_key(self, auth_key):
        """ Verifies github auth key by logging in
            Returns an
        """
