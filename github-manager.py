"""
"""

import getpass
import os
import requests
import sys
import csv

HEADER_LIST = ['ID', 'Title', 'State', 'Created At', 'Updated At', 'Closed At', 'Assignee', 'Label']

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
        self._get_org_info()

        # get repo info
        self.issue_url=self.get_repository_info()

        # retrive issue list
        self.retrive_issue_list()

    def _request_handler(self, url):
        """
        use request module to call apis
        """

        # Make https secure call for authentication
        r = requests.get(url, auth=(self.username, self.password))
        return r

    def _authenticate_user(self):
        """
        authenticate user by accessing github username and password and
        see if the response is 200. If not, exit with error message.
        """

        response = self._request_handler(url='https://api.github.com')

        if response.status_code == 200:
            print("Authentication successful. Status: {0}".format(response.status_code))
            return True

        elif response.status_code == 401:
            print("Unauthorized access. Status: {0}".format(response.status_code))
            return False

    def _get_org_info(self):
        """
        get api directory for the selected organization
        """

        url='https://api.github.com/orgs/{0}'.format(self.org_name)
        repo_info = self._request_handler(url)
        org_url_directory = repo_info.json()
        self.repos_url = org_url_directory.get('repos_url')

    def get_repository_info(self):
        """
        get repo informationm
        """

        repo_info = self._request_handler(self.repos_url)
        repo_info_list = repo_info.json()
        for repo in repo_info_list:
            if repo.get('name') == self.repo_name:
                return repo.get('issues_url').replace('{/number}', '?per_page=1000')

    def retrive_issue_list(self):
        """
        get a list of issues
        """
        print("Retriving issue list using api: {0}".format(self.issue_url))
        repo_info = self._request_handler(self.issue_url)
        repo_info_list = repo_info.json()

        self._format_issues(repo_info_list)

    def _format_issues(self, repo_info_list):
        """
        """
        data_dict = dict()
        for cnt, issue in enumerate(repo_info_list):
            label_list = [label.get('name') for label in issue.get('labels')]
            data_dict[cnt] = [issue.get('number'),
                             issue.get('title'),
                             issue.get('state'),
                             issue.get('created_at'),
                             issue.get('updated_at'),
                             issue.get('closed_at'),
                             issue.get('assignee'),
                             label_list,]
        return data_dict

    def create_csv(self, data_dict):
        """
        """
        
#HEADER_LIST = ['ID', 'Title', 'State', 'Created At', 'Updated At', 'Closed At', 'Assignee', 'Label']
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
    org_name = input("Enter organization name: ")

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
