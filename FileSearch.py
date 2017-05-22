# -*- coding: cp1252 -*-

import codecs
from common import *
from py2casefold import casefold
import os


class FileReader:
    fileError = False
    fileReader = None

    def __init__(self, filename):
        try:
            self.fileReader = codecs.open(filename=filename, mode="r", encoding="cp1252")
        except IOError:
            self.fileError = True

    def get_new_line(self):
        if self.fileError or self.fileReader is None:
            return None
        try:
            new_line = self.fileReader.readline()
        except EOFError:
            return None
        else:
            return new_line

    def read(self):
        read_new_line = True
        while read_new_line:
            line = self.get_new_line()
            if line is None or line == u'':
                read_new_line = False
            else:
                yield line


class Line:
    line_dict = None

    def __init__(self, line):
        self.line_dict = {}
        fields = line.split("|")
        for field in fields:
            if field not in [u"", u"\r\n", u"\n"]:
                camp = u""
                valor = u""
                try:
                    items = field.split("=")
                    camp = items[0]
                    valor = items[1]
                except:
                    pass
                finally:
                    self.line_dict[camp] = valor


class Search:
    line_dict_list = []

    def __init__(self, file_name, item=None):
        self.line_dict_list = []
        file_reader = FileReader(file_name)
        read = file_reader.read()
        num_lines = 0
        for line in read:
            num_lines += 1
            obj_line = Line(line)
            line_dict = obj_line.line_dict
            if item is not None and item not in [u""]:
                found = False
                found_key_list = []
                for (key, value) in line_dict.items():
                    if casefold(unicode(item)) in casefold(unicode(value)) or \
                       casefold(unicode(item)) in casefold(unicode(value.replace(":", "_"))) or \
                       casefold(unicode(item)) in casefold(unicode(value.replace(":", "."))):
                        found = True
                        found_key_list.append(key)
                if found:
                   self.line_dict_list.append({"line_dict": line_dict, "found_key_list": found_key_list})


class ReadAllIds:
    id_list = []

    def __init__(self, file_name):
        self.id_list = []
        file_reader = FileReader(file_name)
        read = file_reader.read()
        for line in read:
            obj_line = Line(line)
            line_dict = obj_line.line_dict
            if "id" in line_dict:
                self.id_list.append(line_dict["id"])
            else:
                if "fkPadre" in line_dict:
                    self.id_list.append(line_dict["fkPadre"])
                else:
                    if "idContenido" in line_dict:
                        self.id_list.append(line_dict["idContenido"])


class ReadAll:
    dict_list = []

    def __init__(self, file_name):
        self.dict_list = []
        file_reader = FileReader(file_name)
        read = file_reader.read()
        for line in read:
            obj_line = Line(line)
            self.dict_list.append(obj_line.line_dict)


class SearchDir:
    dir_list = []

    def __init__(self, directori, item=None):
        self.dir_list = []
        item_sub = None
        item_point = None
        if item is not None:
            item_sub = item.replace(":", "_")
            item_point = item.replace(":", ".")
        num_lines = 0

        if os.path.exists(directori):
            for file in os.listdir(directori):
                pathfile = os.path.join(directori, file)
                if os.path.isdir(pathfile):
                    num_lines += 1
                    if item is None or file in [item_sub, item_point, item]:
                        self.dir_list.append(pathfile)
        '''
        for root, dirs, files in os.walk(directori):
            for dir in dirs:
                num_lines += 1
                if item is None or str(dir) in [item_sub, item_point, item]:
                    self.dir_list.append(os.path.join(root, dir))
        '''
