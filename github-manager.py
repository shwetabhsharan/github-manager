"""
Module to create csv for list of issues for a repository
Usage: python3 github-manager.py
After executing, you will see the following

======github to csv exporter======
Enter your github username: shwetabhs
Password: 
Enter org name: SS-priv
Enter repository name: himalayan_pink

Enter the above values and it will print a list of issues present

TODO: create csv
"""
import getpass
import os
import requests
import sys

class GithubManager(object):

    def __init__(self, username, password, org_name, repo_name):
        """
        constructor
        """

        self.username=username
        self.password=password
        self.org_name=org_name
        self.repo_name=repo_name

    def controller(self):
        """
        main controller
        """

        # authenticate user
        auth_status = self._authenticate_user()

        # If authentication fails, exit.
        if not auth_status:
            sys.exit(1)

        # get org info, returns a list of urls, extract org url
        self.get_org_info()

        # get repo info
        self.issue_url=self.get_repository_info()

        # retrive issue list
        self.retrive_issue_list()

    def request_handler(self, url):
        """
        use request module to call apis
        """

        # Make https secure call for authentication
        r = requests.get(url, auth=(self.username, self.password))
        return r

    def _authenticate_user(self):
        """
        """

        response = self.request_handler(url='https://api.github.com')

        if response.status_code == 200:
            print("Authentication successful. Status: {0}".format(response.status_code))
            return True

        elif response.status_code == 401:
            print("Unauthorized access. Status: {0}".format(response.status_code))
            return False

    def get_org_info(self):
        """
        """

        url='https://api.github.com/orgs/{0}'.format(self.org_name)
        repo_info = self.request_handler(url)
        org_url_directory = repo_info.json()
        self.repos_url = org_url_directory.get('repos_url')

    def get_repository_info(self):
        """
        """

        repo_info = self.request_handler(self.repos_url)
        repo_info_list = repo_info.json()
        for repo in repo_info_list:
            if repo.get('name') == self.repo_name:
                return repo.get('issues_url').replace('{/number}', '')

    def retrive_issue_list(self):
        """
        """
        print("Retriving issue list using api: {0}".format(self.issue_url))
        repo_info = self.request_handler(self.issue_url)
        repo_info_list = repo_info.json()
        print(repo_info_list)

if __name__ == "__main__":

    # Clear screen
    os.system('clear')
    print("======github to csv exporter======")

    # Get input from user

    # Enter github username
    username = input("Enter your github username: ")

    # Enter password
    password = getpass.getpass()

    # Enter org name
    org_name = input("Enter org name: ")

    # Enter repository name
    repo_name = input("Enter repository name: ")

    # If empty, exit
    if not username or not password:
        print("Error: Empty username and password. Exiting.")
        sys.exit(1)

    # If empty, exit
    if not org_name or not repo_name:
        print("Error: Empty organization and repository name. Exiting.")
        sys.exit(1)

    # authenticate and print list of issues
    obj = GithubManager(username, password, org_name, repo_name)
    obj.controller()
