import unittest
from configparser import ConfigParser
from unittest.mock import patch

from repository import Repository


class TestRepository(unittest.TestCase):
    def test_repository_with_valid_git_directory_path(self):
        repository = Repository(".", force=False)
        self.assertEqual(repository.worktree, ".")
        self.assertEqual(repository.gitdir, "./.git")
        self.assertEqual(type(repository.conf), ConfigParser)

    def test_repository_with_invalid_git_directory_path(self):
        with self.assertRaises(Exception) as ex:
            _ = Repository("./.git", force=False)
        self.assertEqual(str(ex.exception), "Not a Git repository ./.git")

    @patch("os.path.exists")
    def test_repository_with_configuration_file_missing(self, mock_exists):
        def miss_conf_on_purpose(filepath: str) -> bool:
            return False if filepath.endswith("config") else True

        mock_exists.side_effect = miss_conf_on_purpose

        with self.assertRaises(Exception) as ex:
            _ = Repository(".", force=False)
        self.assertEqual(str(ex.exception), "Configuration file missing ./.git/config")

    @patch("configparser.ConfigParser.get")
    def test_repository_with_configuration_file_missing(self, mock_get):
        def get_unsupported_version_on_purpose(*key_path: str) -> int:
            return 1 if key_path == ("core", "repositoryformatversion") else 0

        mock_get.side_effect = get_unsupported_version_on_purpose

        with self.assertRaises(Exception) as ex:
            _ = Repository(".", force=False)
        self.assertEqual(str(ex.exception), "Unsupported repositoryformatversion 1")


if __name__ == "__main__":
    _ = unittest.main()
