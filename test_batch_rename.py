import unittest
import unittest.mock
import batch_rename
import os
import time


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['TZ'] = 'UTC'
        time.tzset()

    def test_datetime_formatting_is_iso8601_without_ms(self):
        self.assertEqual(batch_rename.format_datetime(0), "1970-01-01T00:00:00")
        self.assertEqual(batch_rename.format_datetime(946684800), "2000-01-01T00:00:00")

    @unittest.mock.patch('os.listdir')
    @unittest.mock.patch('os.path.isfile')
    def test_getting_files_in_folder(self, isfile, listdir):
        isfile.return_value = True
        listdir.return_value = ["file1.txt", "file2.txt"]

        files = batch_rename.get_files('test_dir')
        self.assertEqual(files, ["file1.txt", "file2.txt"])

    @unittest.mock.patch('os.listdir')
    @unittest.mock.patch('os.path.isfile')
    def test_getting_only_files_not_sub_directories(self, isfile, listdir):
        isfile.return_value = False
        listdir.return_value = ["file1.txt", "file2.txt"]

        files = batch_rename.get_files('test_dir')
        self.assertEqual(files, [])


    def test_ensuring_destination_directory_exists(self):
        pass


    def test_creating_destination_directory(self):
        pass


if __name__ == '__main__':
    unittest.main()
