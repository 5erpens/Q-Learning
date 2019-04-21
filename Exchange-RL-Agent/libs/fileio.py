import os
from sys import platform as _platform
# noinspection PyCompatibility
from pathlib import PureWindowsPath
from libs.Singleton import Singleton


@Singleton
class fileio:

    def __init__(self, File_Name=None):
        self._file_name = File_Name

    def set_File_Name(self, file_name):
        self._file_name = file_name

    def write_file(self, input):
        text_file = open(self._file_name, "a")
        text_file.write(input)
        text_file.close()

    def write_overwrite(self, input):
        text_file = open(self._file_name, "a")
        text_file.write(input)
        text_file.close()

    def file_flush(self):
        open(self._file_name, "w").close()

    def read_file(self):
        return open(self._file_name, 'r')

    def create_folder(self, name, sub_directory):
        if sub_directory is not None:
            directory_list = [self._file_name, sub_directory, "/", name]
            directory = "".join(directory_list)
            if not os.path.exists(self.path(directory_list)):
                os.makedirs(directory)
        else:
            directory_list = [self._file_name, "", "/", name]
            directory = "".join(directory_list)
            if not os.path.exists(self.path(directory_list)):
                os.makedirs(directory)

        return self.path(directory + "/")

    @staticmethod
    def path(string):
        if _platform == "win32" or _platform == "win64":
            return str(PureWindowsPath(string))
        else:
            return string

    def root_path(self, string):
        rootdir = os.getcwd().split("Exchange-RL-Agent")
        return rootdir[0] + "Exchange-RL-Agent" + self.path(string)
