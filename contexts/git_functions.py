from github import Github
from sciflow.localsettings import ghtoken


def addctxfile(path, message, file, repo="scidata", token=ghtoken):
    """
    Push file update to GitHub repo

    :param path: path to the file in the repo
    :param message: commit message
    :param file: the file contents
    :param repo: the repo name
    :param token: github user token

    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    """

    # get repo
    g = Github(token)
    repo = g.get_user().get_repo(repo)
    result = repo.create_file(path, message, file)
    return result
