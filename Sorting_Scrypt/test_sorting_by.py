import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from sortinng_by_files import create_category_directory, move_file, create_others_directory, get_file_extension, get_category_for_extension, sort_and_move_file, sort_files

class TestFileSorter(unittest.TestCase):

    @patch('os.makedirs')
    def test_create_category_directory(self, mock_makedirs):
        """
        Function: create_category
        Params: mock_makedirs (MagicMock)
        Brief: Test directory creation.
        """
        source_dir = '/test/source'
        category = 'docs'
        mock_makedirs.return_value = None
        result = create_category_directory(source_dir, category)
        self.assertIsNotNone(result)
        self.assertTrue(mock_makedirs.called)

    @patch('shutil.move')
    def test_move_file(self, mock_move):
        """
        Function: move_file
        Params: mock_move (MagicMock)
        Brief: Test file movement.
        """
        file = '/test/source/test_file.txt'
        category_dir = '/test/source/docs'
        mock_move.return_value = None
        move_file(file, category_dir)
        mock_move.assert_called_once_with(file, os.path.join(category_dir, 'test_file.txt'))

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_create_others_directory(self, mock_makedirs, mock_exists):
        """
        Function: create_others
        Params: mock_makedirs (MagicMock), mock_exists (MagicMock)
        Brief: Test 'others' directory.
        """
        source_dir = '/test/source'
        mock_exists.return_value = False
        result = create_others_directory(source_dir)
        mock_makedirs.assert_called_once_with('/test/source/others')
        self.assertEqual(result, '/test/source/others')

    def test_get_file_extension(self):
        """
        Function: file_extension
        Brief: Test file extension.
        """
        filename = 'test_file.txt'
        extension = get_file_extension(filename)
        self.assertEqual(extension, '.txt')

    def test_get_category_for_extension(self):
        """
        Function: file_category
        Brief: Test file category.
        """
        file_extension = '.mp4'
        category = get_category_for_extension(file_extension)
        self.assertEqual(category, 'videos')

    @patch('sortinng_by_files.move_file')
    @patch('sortinng_by_files.create_category_directory')
    def test_sort_and_move_file(self, mock_create_dir, mock_move):
        """
        Function: sort_move_file
        Params: mock_create_dir (MagicMock), mock_move (MagicMock)
        Brief: Test file sorting.
        """
        source_dir = '/test/source'
        others_dir = '/test/source/others'
        file_path = '/test/source/test_video.mp4'
        
        mock_create_dir.return_value = '/test/source/videos'
        sort_and_move_file(file_path, source_dir, others_dir)
        mock_move.assert_called_once_with(file_path, '/test/source/videos/test_video.mp4')

    @patch('os.listdir')
    @patch('sortinng_by_files.sort_and_move_file')
    def test_sort_files(self, mock_sort_and_move, mock_listdir):
        """
        Function: sort_files
        Params: mock_sort_and_move (MagicMock), mock_listdir (MagicMock)
        Brief: Test file sorting.
        """
        source_dir = '/test/source'
        mock_listdir.return_value = ['test_video.mp4', 'test_file.txt']
        mock_sort_and_move.return_value = None
        sort_files(source_dir)
        mock_sort_and_move.assert_any_call('/test/source/test_video.mp4', source_dir, '/test/source/others')
        mock_sort_and_move.assert_any_call('/test/source/test_file.txt', source_dir, '/test/source/others')

if __name__ == '__main__':
    unittest.main()