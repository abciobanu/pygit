import os
import unittest
from unittest.mock import patch

from repository import Repository, RepositoryHelpers


class TestRepositoryHelpers(unittest.TestCase):

    def test_get_gitdir_joined_file_path(self):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_joined_file_path(repository, "HEAD"),
            "./.git/HEAD",
        )

    def test_get_gitdir_dir_path_with_valid_path_without_mkdir(self):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_dir_path(repository, "refs", "heads"),
            "./.git/refs/heads",
        )

    @patch("os.makedirs")
    def test_get_gitdir_dir_path_with_valid_path_with_mkdir(self, mock_makedirs):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_dir_path(
                repository, "non_existent_dir", mkdir_if_absent=True
            ),
            "./.git/non_existent_dir",
        )
        mock_makedirs.assert_called_once_with("./.git/non_existent_dir")

    def test_get_gitdir_dir_path_with_valid_not_dir_path(self):
        repository = Repository(".", force=True)
        with self.assertRaises(Exception) as ex:
            _ = RepositoryHelpers.get_gitdir_dir_path(repository, "HEAD")
        self.assertEqual(str(ex.exception), "Not a directory ./.git/HEAD")

    def test_get_gitdir_dir_path_with_non_existing_path_without_mkdir(self):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_dir_path(repository, "non_existent_dir"), None
        )

    def test_get_gitdir_file_path_with_valid_path_without_mkdir(self):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_file_path(repository, "HEAD"), "./.git/HEAD"
        )

        self.assertEqual(
            RepositoryHelpers.get_gitdir_file_path(repository, "refs", "heads", "main"),
            "./.git/refs/heads/main",
        )

    @patch("os.makedirs")
    def test_get_gitdir_file_path_with_valid_path_with_mkdir(self, mock_makedirs):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_file_path(
                repository, "new_dir", "some_file", mkdir_if_absent=True
            ),
            "./.git/new_dir/some_file",
        )
        mock_makedirs.assert_called_once_with("./.git/new_dir")

    def test_get_gitdir_file_path_with_invalid_parent_dir(self):
        repository = Repository(".", force=True)
        self.assertEqual(
            RepositoryHelpers.get_gitdir_file_path(repository, "new_dir", "some_file"),
            None,
        )


if __name__ == "__main__":
    _ = unittest.main()
