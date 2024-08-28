import configparser
import os


class Repository(object):
    """A git repository"""

    def __init__(self, path: str, force: bool = False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        # Check if the path is a valid git directory path
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)

        # Read the configuration file from the git directory
        self.conf = configparser.ConfigParser()
        conf_file_path = RepositoryHelpers.get_gitdir_joined_file_path(self, "config")
        if conf_file_path and os.path.exists(conf_file_path):
            _ = self.conf.read([conf_file_path])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            version = int(self.conf.get("core", "repositoryformatversion"))
            if version != 0:
                raise Exception("Unsupported repositoryformatversion %s" % version)


class RepositoryHelpers(object):
    """Helper functions for repository operations"""

    @staticmethod
    def get_gitdir_joined_file_path(repo: Repository, *path: str) -> str:
        """Get the path of a file in the git directory (no checks)"""
        return str(os.path.join(repo.gitdir, *path))

    @staticmethod
    def get_gitdir_dir_path(
        repo: Repository, *path: str, mkdir_if_absent: bool = False
    ) -> str | None:
        """Get the path of a directory in the git directory (and create it if absent)"""
        joined_path = RepositoryHelpers.get_gitdir_joined_file_path(repo, *path)
        if os.path.exists(joined_path):
            if os.path.isdir(joined_path):
                return joined_path
            raise Exception("Not a directory %s" % joined_path)

        if mkdir_if_absent:
            os.makedirs(joined_path)
            return joined_path

        return None

    @staticmethod
    def get_gitdir_file_path(
        repo: Repository, *path: str, mkdir_if_absent: bool = False
    ) -> str | None:
        """Get the path of a file in the git directory (and create its parent directory if absent)"""
        parent_dir_path = path[:-1]
        parent_dir = RepositoryHelpers.get_gitdir_dir_path(
            repo, *parent_dir_path, mkdir_if_absent=mkdir_if_absent
        )

        if parent_dir:
            return RepositoryHelpers.get_gitdir_file_path(repo, *path)
