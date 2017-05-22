# -*- coding: cp1252 -*-

# from Tkinter import *
from common import *
from FileSearch import Search, SearchDir, ReadAllIds, ReadAll
import os
import threading
import requests

import Tkinter as tk
import tkFileDialog
from FileCompare import diff_files

MAX_WINDOWS_NUMBER = 10


class Main:

    result_list = []
    master = None


    documentos_found_list = []
    documentos_not_found_list = []
    componentes_found_list = []
    componentes_not_found_list = []
    multimedias_found_list = []
    multimedias_not_found_list = []
    textos_found_list = []
    textos_not_found_list = []
    check = {}

    directory_field = INITIAL_DIR

    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master, width=200)

        self.frame1 = tk.Frame(self.frame)
        self.field1 = tk.StringVar()
        self.field1_frame = tk.Frame(self.frame1)
        self.field1_label = tk.Label(self.field1_frame, text="Search:")
        self.field1_label.pack(side="left")
        self.field1_entry = tk.Entry(self.field1_frame, textvariable=self.field1, width=75)
        self.field1_entry.pack(side="right")
        self.field1_frame.pack(side="left")

        self.button_search_all = tk.Button(self.frame1, text='Search All', width=15, command=self.search_all)
        self.button_search_all.pack(side="left")
        self.button_categorias = tk.Button(self.frame1, text='Categorias', width=15, command=self.search_categorias)
        self.button_categorias.pack(side="left")
        self.button_componentes = tk.Button(self.frame1, text='Componentes', width=15, command=self.search_componentes)
        self.button_componentes.pack(side="left")
        self.button_contenidos = tk.Button(self.frame1, text='Contenidos', width=15, command=self.search_contenidos)
        self.button_contenidos.pack(side="left")
        self.button_contienes = tk.Button(self.frame1, text='Contienes', width=15, command=self.search_contienes)
        self.button_contienes.pack(side="left")
        self.button_documentos = tk.Button(self.frame1, text='Documentos', width=15, command=self.search_documentos)
        self.button_documentos.pack(side="left")
        self.button_enlaces = tk.Button(self.frame1, text='Enlaces', width=15, command=self.search_enlaces)
        self.button_enlaces.pack(side="left")
        self.button_metadatos = tk.Button(self.frame1, text='Metadatos', width=15, command=self.search_metadatos)
        self.button_metadatos.pack(side="left")
        self.button_files_doc = tk.Button(self.frame1, text='Files Doc', width=15, command=self.search_files_doc)
        self.button_files_doc.pack(side="left")
        self.button_files_comp = tk.Button(self.frame1, text='Files Comp', width=15, command=self.search_files_comp)
        self.button_files_comp.pack(side="left")
        self.frame1.pack(side="top")

        self.frame2 = tk.Frame(self.frame)
        self.button_diff = tk.Button(self.frame2, text='Diff All', width=10, command=self.diff_all)
        self.button_diff.pack(side="left")
        self.button_check_all = tk.Button(self.frame2, text='Check All', width=10, command=self.check_all)
        self.button_check_all.pack(side="left")
        self.button_matching_files = tk.Button(self.frame2, text='Files', width=10, command=self.matching_files)
        self.button_matching_files.pack(side="left")
        self.button_matching_directories = tk.Button(self.frame2, text='Dirs', width=10, command=self.matching_directories)
        self.button_matching_directories.pack(side="left")
        self.message_label = tk.Label(self.frame2, width=30)
        self.message_label.pack(side="left")
        self.button_close_all = tk.Button(self.frame2, text='Close All', width=15, command=self.close_all)
        self.button_close_all.pack(side="left")
        self.button_multimedias = tk.Button(self.frame2, text='Multimedias', width=15, command=self.search_multimedias)
        self.button_multimedias.pack(side="left")
        self.button_nodosmenu = tk.Button(self.frame2, text=u'Nodos Menú', width=15, command=self.search_nodosmenu)
        self.button_nodosmenu.pack(side="left")
        self.button_paginas = tk.Button(self.frame2, text=u'Páginas', width=15, command=self.search_paginas)
        self.button_paginas.pack(side="left")
        self.button_textos = tk.Button(self.frame2, text='Textos', width=15, command=self.search_textos)
        self.button_textos.pack(side="left")
        self.button_traducciones = tk.Button(self.frame2, text='Traducciones', width=15, command=self.search_traducciones)
        self.button_traducciones.pack(side="left")
        self.button_vistas = tk.Button(self.frame2, text='Vistas', width=15, command=self.search_vistas)
        self.button_vistas.pack(side="left")
        self.button_files_img = tk.Button(self.frame2, text='Files Img', width=15, command=self.search_files_img)
        self.button_files_img.pack(side="left")
        self.button_files_texto = tk.Button(self.frame2, text='Files Texto', width=15, command=self.search_files_texto)
        self.button_files_texto.pack(side="left")
        self.frame2.pack(side="right")

        self.frame.pack()

        self.frame3 = tk.Frame(self.master, width=200)
        self.button_plantillas = tk.Button(self.frame3, text='Plantillas', width=15, command=self.search_plantillas)
        self.button_plantillas.pack(side="left")
        self.button_zonas = tk.Button(self.frame3, text='Zonas', width=15, command=self.search_zonas)
        self.button_zonas.pack(side="left")
        self.directory_field_frame = tk.Frame(self.frame3)
        self.directory_field_label = tk.Label(self.directory_field_frame, text="Directory:")
        self.directory_field_label.pack(side="left")
        self.directory_field_entry = tk.Label(self.directory_field_frame, text=self.directory_field, width=75)
        self.directory_field_entry.pack(side="right")
        self.directory_field_frame.pack(side="left")
        self.dialog_directory = TkDirectoryDialog(self.frame3, self)
        self.dialog_directory.pack(side="right")
        self.frame3.pack(side="bottom")

    def show_matching(self, item_list, file_name, parent_dir, template_text):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ResultMatching(self.newWindow, "\n".join(item_list), template_text % (len(item_list), parent_dir, file_name))
        self.result_list.append(self.newWindow)

    def show_dir(self, dir):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ResultDir(self.newWindow, dir)
        self.result_list.append(self.newWindow)

    def show_line(self, line_dict, title):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Result(self.newWindow, line_dict=line_dict, title=title)
        self.result_list.append(self.newWindow)

    def show_check(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = ResultCheck(self.newWindow, self.check)
        self.result_list.append(self.newWindow)

    def show_diff(self):
        for (file_name, joined_diff) in self.diff_dict.items():
            self.newWindow = tk.Toplevel(self.master)
            self.app = ResultDiff(self.newWindow, file_name, joined_diff)
            self.result_list.append(self.newWindow)

    def match_dirs_files(self, file_name, parent_dir):
        found_list = []
        not_found_list = []
        dict_list = (ReadAll(os.path.join(self.directory_field, file_name))).dict_list
        for dict_item in dict_list:
            item = ""
            if "id" in dict_item:
                item = dict_item["id"]
            else:
                if "fkPadre" in dict_item:
                    item = dict_item["fkPadre"]
                else:
                    if "idContenido" in dict_item:
                        item = dict_item["idContenido"]

            item_tipo = item + (" # " + dict_item["tipo"] if "tipo" in dict_item else "")

            item1 = item.replace(":", "_")
            item2 = item.replace(":", ".")
            path = os.path.join(os.path.join(self.directory_field, parent_dir), item1)
            if os.path.exists(path):
                if self.has_translations(path):
                    found_list.append(item_tipo + " (%dt)" % self.translation_count(path))
                else:
                    found_list.append(item_tipo)
            else:
                path = os.path.join(os.path.join(self.directory_field, parent_dir), item2)
                if os.path.exists(path):
                    if self.has_translations(path):
                        found_list.append(item_tipo + " (%dt)" % self.translation_count(path))
                    else:
                        found_list.append(item_tipo)
                else:
                    not_found_list.append(item_tipo)
        return found_list, not_found_list

    def process_dir_files(self, file_name, parent_dir):
        found_list, not_found_list = self.match_dirs_files(os.path.join(self.directory_field, file_name), parent_dir)
        if parent_dir == DOC_DIR:
            self.documentos_found_list = found_list
            self.documentos_not_found_list = not_found_list
        elif parent_dir == COMP_DIR:
            self.componentes_found_list = found_list
            self.componentes_not_found_list = not_found_list
        elif parent_dir == IMG_DIR:
            self.multimedias_found_list = found_list
            self.multimedias_not_found_list = not_found_list
        elif parent_dir == TEXTO_DIR:
            self.textos_found_list = found_list
            self.textos_not_found_list = not_found_list

    def matching_directories(self):
        self.message_label["text"] = "Matching..."
        self.message_label.update()

        text_found = "(%d) DIR MATCH %s ON FILE %s"
        text_not_found = "(%d) DIR NOT MATCH %s ON FILE %s"

        thread_list = []
        thread_list.append(threading.Thread(target=self.process_dir_files, args=(DOCUMENTOS_FILE, DOC_DIR,)))
        thread_list.append(threading.Thread(target=self.process_dir_files, args=(COMPONENTES_FILE, COMP_DIR,)))
        thread_list.append(threading.Thread(target=self.process_dir_files, args=(MULTIMEDIAS_FILE, IMG_DIR,)))
        thread_list.append(threading.Thread(target=self.process_dir_files, args=(TEXTOS_FILE, TEXTO_DIR,)))

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        if len(self.documentos_found_list) > 0:
            self.show_matching(self.documentos_found_list, DOCUMENTOS_FILE, DOC_DIR, text_found)
        if len(self.documentos_not_found_list) > 0:
            self.show_matching(self.documentos_not_found_list, DOCUMENTOS_FILE, DOC_DIR, text_not_found)

        if len(self.componentes_found_list) > 0:
            self.show_matching(self.componentes_found_list, COMPONENTES_FILE, COMP_DIR, text_found)
        if len(self.componentes_not_found_list) > 0:
            self.show_matching(self.componentes_not_found_list, COMPONENTES_FILE, COMP_DIR, text_not_found)

        if len(self.multimedias_found_list) > 0:
            self.show_matching(self.multimedias_found_list, MULTIMEDIAS_FILE, IMG_DIR, text_found)
        if len(self.multimedias_not_found_list) > 0:
            self.show_matching(self.multimedias_not_found_list, MULTIMEDIAS_FILE, IMG_DIR, text_not_found)

        if len(self.textos_found_list) > 0:
            self.show_matching(self.textos_found_list, TEXTOS_FILE, TEXTO_DIR, text_found)
        if len(self.textos_not_found_list) > 0:
            self.show_matching(self.textos_not_found_list, TEXTOS_FILE, TEXTO_DIR, text_not_found)

        self.message_label["text"] = ""
        self.message_label.update()

    def match_files_dirs(self, file_name, parent_dir):
        found_list = []
        not_found_list = []

        id_list = (ReadAllIds(os.path.join(self.directory_field, file_name))).id_list
        for id in id_list:
            item1 = id.replace(":", "_")
            item2 = id.replace(":", ".")
            if item1 not in id_list:
                id_list.append(item1)
            if item2 not in id_list:
                id_list.append(item2)

        dir_list = (SearchDir(os.path.join(self.directory_field, parent_dir), item=None)).dir_list
        for dir in dir_list:
            (head, item) = os.path.split(dir)
            if item not in ["img", "doc", "comp", "texto", "EN", "CA", "ES"]:
                if item in id_list:
                    if self.has_translations(dir):
                        found_list.append(item + " (%dt)" % self.translation_count(dir))
                    else:
                        found_list.append(item)
                else:
                    if self.has_translations(dir):
                        not_found_list.append(item + " (%dt)" % self.translation_count(dir))
                    else:
                        not_found_list.append(item)
        return found_list, not_found_list

    def process_files_dirs(self, file_name, parent_dir):
        found_list, not_found_list = self.match_files_dirs(file_name, parent_dir)
        if parent_dir == DOC_DIR:
            self.documentos_found_list = found_list
            self.documentos_not_found_list = not_found_list
        elif parent_dir == COMP_DIR:
            self.componentes_found_list = found_list
            self.componentes_not_found_list = not_found_list
        elif parent_dir == IMG_DIR:
            self.multimedias_found_list = found_list
            self.multimedias_not_found_list = not_found_list
        elif parent_dir == TEXTO_DIR:
            self.textos_found_list = found_list
            self.textos_not_found_list = not_found_list

    def matching_files(self):
        text_found = "(%d) FILE MATCH %s - %s"
        text_not_found = "(%d) FILE NOT MATCH %s - %s"

        self.message_label["text"] = "Matching..."
        self.message_label.update()

        thread_list = []
        thread_list.append(threading.Thread(target=self.process_files_dirs, args=(DOCUMENTOS_FILE, DOC_DIR,)))
        thread_list.append(threading.Thread(target=self.process_files_dirs, args=(COMPONENTES_FILE, COMP_DIR,)))
        thread_list.append(threading.Thread(target=self.process_files_dirs, args=(MULTIMEDIAS_FILE, IMG_DIR,)))
        thread_list.append(threading.Thread(target=self.process_files_dirs, args=(TEXTOS_FILE, TEXTO_DIR,)))

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        if len(self.documentos_found_list) > 0:
            self.show_matching(self.documentos_found_list, DOCUMENTOS_FILE, DOC_DIR, text_found)
        if len(self.documentos_not_found_list) > 0:
            self.show_matching(self.documentos_not_found_list, DOCUMENTOS_FILE, DOC_DIR, text_not_found)

        if len(self.componentes_found_list) > 0:
            self.show_matching(self.componentes_found_list, COMPONENTES_FILE, COMP_DIR, text_found)
        if len(self.componentes_not_found_list) > 0:
            self.show_matching(self.componentes_not_found_list, COMPONENTES_FILE, COMP_DIR, text_not_found)

        if len(self.multimedias_found_list) > 0:
            self.show_matching(self.multimedias_found_list, MULTIMEDIAS_FILE, IMG_DIR, text_found)
        if len(self.multimedias_not_found_list) > 0:
            self.show_matching(self.multimedias_not_found_list, MULTIMEDIAS_FILE, IMG_DIR, text_not_found)

        if len(self.textos_found_list) > 0:
            self.show_matching(self.textos_found_list, TEXTOS_FILE, TEXTO_DIR, text_found)
        if len(self.textos_not_found_list) > 0:
            self.show_matching(self.textos_not_found_list, TEXTOS_FILE, TEXTO_DIR, text_not_found)

        self.message_label["text"] = ""
        self.message_label.update()

    def file_count(self, file_name):
        id_list = (ReadAllIds(file_name)).id_list
        return len(id_list)

    def has_translations(self, dir_name):
        has_translations = False
        subdir_list = (SearchDir(dir_name, item=None)).dir_list
        for subdir in subdir_list:
            (head, item) = os.path.split(subdir)
            if item in ["EN", "CA", "ES"]:
                has_translations = True
                break
        return has_translations

    def translation_count(self, dir_name):
        count = 0
        subdir_list = (SearchDir(dir_name, item=None)).dir_list
        for subdir in subdir_list:
            (head, item) = os.path.split(subdir)
            if item in ["EN", "CA", "ES"]:
                count += 1
        return count

    def directori_count(self, parent_dir):
        count = 0
        translations = 0
        dir_list = (SearchDir(parent_dir, item=None)).dir_list
        for dir_item in dir_list:
            count += 1
            translations += self.translation_count(dir_item)
        return count, translations

    def count_files_dirs(self, file_name, parent_dir=None):
        file_count = self.file_count(os.path.join(self.directory_field, file_name))
        directori_count = 0
        translations_count = 0
        if parent_dir is not None:
            directori_count, translations_count = self.directori_count(os.path.join(self.directory_field, parent_dir))
        self.check[file_name] = {"file_count": file_count, "directori_count": directori_count, "translations_count": translations_count}

    def diff_file(self, file_name):
        file_preview = os.path.join(self.directory_field, "PREVIEW", file_name)
        file_view = os.path.join(self.directory_field, "VIEW", file_name)
        if os.path.exists(file_preview) and os.path.exists(file_view):
            diff = diff_files(file_preview, file_view)
            joined_diff = "".join(diff)
            self.diff_dict[file_name] = joined_diff
            f = open(os.path.join(self.directory_field, "diff_" + file_name), 'w')
            f.write(joined_diff)
            f.close()

    def diff_all(self):
        self.message_label["text"] = "Diff PREVIEW - VIEW... (1/3)"
        self.message_label.update()

        self.diff_dict = {}

        thread_list = []
        thread_list.append(threading.Thread(target=self.diff_file, args=(COMPONENTES_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(DOCUMENTOS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(MULTIMEDIAS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(TEXTOS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(PLANTILLAS_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        self.message_label["text"] = "Diff PREVIEW - VIEW... (2/3)"
        self.message_label.update()

        thread_list = []
        thread_list.append(threading.Thread(target=self.diff_file, args=(CATEGORIAS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(CONTENIDOS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(CONTIENES_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(METADATOS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(ZONAS_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        self.message_label["text"] = "Diff PREVIEW - VIEW... (3/3)"
        self.message_label.update()

        thread_list = []
        thread_list.append(threading.Thread(target=self.diff_file, args=(NODOSMENU_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(PAGINAS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(TRADUCCIONES_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(VISTAS_FILE,)))
        thread_list.append(threading.Thread(target=self.diff_file, args=(ENLACES_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        self.show_diff()

        self.message_label["text"] = ""
        self.message_label.update()

    def check_all(self):
        self.message_label["text"] = "Checking..."
        self.message_label.update()

        self.check = {}

        thread_list = []
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(DOCUMENTOS_FILE, DOC_DIR,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(COMPONENTES_FILE, COMP_DIR,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(MULTIMEDIAS_FILE, IMG_DIR,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(TEXTOS_FILE, TEXTO_DIR,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(PLANTILLAS_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        thread_list = []
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(CATEGORIAS_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(CONTENIDOS_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(CONTIENES_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(METADATOS_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(ZONAS_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        thread_list = []
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(NODOSMENU_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(PAGINAS_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(TRADUCCIONES_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(VISTAS_FILE,)))
        thread_list.append(threading.Thread(target=self.count_files_dirs, args=(ENLACES_FILE,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        self.show_check()

        self.message_label["text"] = ""
        self.message_label.update()

    def search_files(self, directori):
        item = self.field1.get()

        self.message_label["text"] = "Searching..."
        self.message_label.update()

        results = SearchDir(directori, item=item)
        result_number = 0
        for dir in results.dir_list:
            result_number += 1
            if result_number <= MAX_WINDOWS_NUMBER:
                self.show_dir(dir)

        self.message_label["text"] = ""
        self.message_label.update()

    def search_files_doc(self):
        self.search_files(os.path.join(self.directory_field, DOC_DIR))

    def search_files_comp(self):
        self.search_files(os.path.join(self.directory_field, COMP_DIR))

    def search_files_img(self):
        self.search_files(os.path.join(self.directory_field, IMG_DIR))

    def search_files_texto(self):
        self.search_files(os.path.join(self.directory_field, TEXTO_DIR))

    def close_all(self):
        for result in self.result_list:
            result.destroy()

    def search_file(self, file, title):
        item = self.field1.get()
        results = Search(os.path.join(self.directory_field, file), item=item)
        result_number = 0
        for line_dict in results.line_dict_list:
            result_number += 1
            if result_number <= MAX_WINDOWS_NUMBER:
                self.show_line(line_dict, title)

    def search_categorias(self):
        self.search_file(CATEGORIAS_FILE, u"CATEGORIA")

    def search_plantillas(self):
        self.search_file(PLANTILLAS_FILE, u"PLANTILLA")

    def search_componentes(self):
        self.search_file(COMPONENTES_FILE, u"COMPONENTE")

    def search_contenidos(self):
        self.search_file(CONTENIDOS_FILE, u"CONTENIDO")

    def search_contienes(self):
        self.search_file(CONTIENES_FILE, u"CONTIENE")

    def search_documentos(self):
        self.search_file(DOCUMENTOS_FILE, u"DOCUMENTO")

    def search_enlaces(self):
        self.search_file(ENLACES_FILE, u"ENLACES")

    def search_metadatos(self):
        self.search_file(METADATOS_FILE, u"METADATO")

    def search_multimedias(self):
        self.search_file(MULTIMEDIAS_FILE, u"MULTIMEDIA")

    def search_zonas(self):
        self.search_file(ZONAS_FILE, u"ZONA")

    def search_nodosmenu(self):
        self.search_file(NODOSMENU_FILE, u"NODO MENÚ")

    def search_paginas(self):
        self.search_file(PAGINAS_FILE, u"PÁGINA")

    def search_textos(self):
        self.search_file(TEXTOS_FILE, u"TEXTO")

    def search_traducciones(self):
        self.search_file(TRADUCCIONES_FILE, u"TRADUCCIÓN")

    def search_vistas(self):
        self.search_file(VISTAS_FILE, u"VISTA")

    def search_all(self):
        self.message_label["text"] = "Searching..."
        self.message_label.update()

        item = self.field1.get()
        self.button_zonas["text"] = "Zonas (%d)" % len((Search(os.path.join(self.directory_field, ZONAS_FILE), item=item)).line_dict_list)
        self.button_plantillas["text"] = "Plantillas (%d)" % len((Search(os.path.join(self.directory_field, PLANTILLAS_FILE), item=item)).line_dict_list)
        self.button_categorias["text"] = "Categorias (%d)" % len((Search(os.path.join(self.directory_field, CATEGORIAS_FILE), item=item)).line_dict_list)
        self.button_componentes["text"] = "Componentes (%d)" % len((Search(os.path.join(self.directory_field, COMPONENTES_FILE), item=item)).line_dict_list)
        self.button_contenidos["text"] = "Contenidos (%d)" % len((Search(os.path.join(self.directory_field, CONTENIDOS_FILE), item=item)).line_dict_list)
        self.button_contienes["text"] = "Contienes (%d)" % len((Search(os.path.join(self.directory_field, CONTIENES_FILE), item=item)).line_dict_list)
        self.button_documentos["text"] = "Documentos (%d)" % len((Search(os.path.join(self.directory_field, DOCUMENTOS_FILE), item=item)).line_dict_list)
        self.button_enlaces["text"] = "Enlaces (%d)" % len((Search(os.path.join(self.directory_field, ENLACES_FILE), item=item)).line_dict_list)
        self.button_metadatos["text"] = "Metadatos (%d)" % len((Search(os.path.join(self.directory_field, METADATOS_FILE), item=item)).line_dict_list)
        self.button_multimedias["text"] = "Multimedias (%d)" % len((Search(os.path.join(self.directory_field, MULTIMEDIAS_FILE), item=item)).line_dict_list)
        self.button_nodosmenu["text"] = u"Nodos Menú (%d)" % len((Search(os.path.join(self.directory_field, NODOSMENU_FILE), item=item)).line_dict_list)
        self.button_paginas["text"] = u"Páginas (%d)" % len((Search(os.path.join(self.directory_field, PAGINAS_FILE), item=item)).line_dict_list)
        self.button_textos["text"] = "Textos (%d)" % len((Search(os.path.join(self.directory_field, TEXTOS_FILE), item=item)).line_dict_list)
        self.button_traducciones["text"] = "Traducciones (%d)" % len((Search(os.path.join(self.directory_field, TRADUCCIONES_FILE), item=item)).line_dict_list)
        self.button_vistas["text"] = "Vistas (%d)" % len((Search(os.path.join(self.directory_field, VISTAS_FILE), item=item)).line_dict_list)
        self.button_files_doc["text"] = "Files Doc (%d)" % len((SearchDir(os.path.join(self.directory_field, DOC_DIR), item=item)).dir_list)
        self.button_files_comp["text"] = "Files Comp (%d)" % len((SearchDir(os.path.join(self.directory_field, COMP_DIR), item=item)).dir_list)
        self.button_files_img["text"] = "Files Img (%d)" % len((SearchDir(os.path.join(self.directory_field, IMG_DIR), item=item)).dir_list)
        self.button_files_texto["text"] = "Files Texto (%d)" % len((SearchDir(os.path.join(self.directory_field, TEXTO_DIR), item=item)).dir_list)

        self.message_label["text"] = ""
        self.message_label.update()


class Result:
    def __init__(self, master, line_dict, title=u"Result"):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(self.frame, text=title, width=120, bg="lightblue")
        self.label.pack()

        self.item_id = ""
        self.imagen = ""
        self.texto = ""
        self.traduccion = ""

        self.session = None

        for (key, value) in line_dict["line_dict"].items():
            frame = tk.Frame(self.frame)

            label = tk.Label(frame, text=key + u":", width=20, anchor=tk.E)
            label.pack(side="left")

            if value != "" and key in ["itemId", "imagen", "texto", "traduccion"]:
                if key == "itemId":
                    self.item_id = value
                    button_usr = tk.Button(frame, text='BEX USR', width=10, command=self.check_bex_user_item)
                    button_usr.pack(side="right")
                    button_tst = tk.Button(frame, text='BEX TST', width=10, command=self.check_bex_test_item)
                    button_tst.pack(side="right")
                if key == "imagen":
                    self.imagen = value
                    button_usr = tk.Button(frame, text='BEX USR', width=10, command=self.check_bex_user_imagen)
                    button_usr.pack(side="right")
                    button_tst = tk.Button(frame, text='BEX TST', width=10, command=self.check_bex_test_imagen)
                    button_tst.pack(side="right")
                if key == "texto":
                    self.texto = value
                    button_usr = tk.Button(frame, text='BEX USR', width=10, command=self.check_bex_user_texto)
                    button_usr.pack(side="right")
                    button_tst = tk.Button(frame, text='BEX TST', width=10, command=self.check_bex_test_texto)
                    button_tst.pack(side="right")
                if key == "traduccion":
                    self.traduccion = value
                    button_usr = tk.Button(frame, text='BEX USR', width=10, command=self.check_bex_user_traduccion)
                    button_usr.pack(side="right")
                    button_tst = tk.Button(frame, text='BEX TST', width=10, command=self.check_bex_test_traduccion)
                    button_tst.pack(side="right")

            field = tk.StringVar()
            field.set(value)
            entry = tk.Entry(frame, textvariable=field, width=70 if value != "" and key in ["itemId", "imagen", "texto", "traduccion"] else 100)
            # entry.config(state='disabled')
            entry.pack(side="right")
            if key in line_dict["found_key_list"]:
                entry["bg"] = "lightyellow"

            frame.pack()

        self.label = tk.Label(self.frame, width=120)
        self.label.pack()

        self.frame.pack()

    def get_html(self, url):
        self.session = requests.Session()
        data = {"username": USERNAME, "password": PASSWORD}
        r = self.session.post(url, data=data, cookies={'from-my': 'browser'})
        print(r.status_code)

    def check_bex_user_item(self):
        os.startfile(BEX_USER_URL % self.item_id)
        # self.get_html(BEX_USER_URL % self.item_id)

    def check_bex_test_item(self):
        os.startfile(BEX_TEST_URL % self.item_id)
        # self.get_html(BEX_TEST_URL % self.item_id)

    def check_bex_user_imagen(self):
        os.startfile(BEX_USER_URL % self.imagen)
        # self.get_html(BEX_USER_URL % self.imagen)

    def check_bex_test_imagen(self):
        os.startfile(BEX_TEST_URL % self.imagen)
        # self.get_html(BEX_TEST_URL % self.imagen)

    def check_bex_user_texto(self):
        os.startfile(BEX_USER_URL % self.texto)
        # self.get_html(BEX_USER_URL % self.texto)

    def check_bex_test_texto(self):
        os.startfile(BEX_TEST_URL % self.texto)
        # self.get_html(BEX_TEST_URL % self.texto)

    def check_bex_user_traduccion(self):
        os.startfile(BEX_USER_URL % self.traduccion)
        # self.get_html(BEX_USER_URL % self.traduccion)

    def check_bex_test_traduccion(self):
        os.startfile(BEX_TEST_URL % self.traduccion)
        # self.get_html(BEX_TEST_URL % self.traduccion)

    def close_windows(self):
        self.master.destroy()


class ResultMatching:
    def __init__(self, master, str_item_list, title=u"Result"):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(self.frame, text=title, width=60, bg="lightblue")
        self.label.pack()

        self.scrollbar = tk.Scrollbar(self.frame)
        self.text = tk.Text(self.frame, width=60)

        self.text.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.insert(tk.END, str_item_list)

        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


class ResultDiff:
    def __init__(self, master, file_name, joined_diff):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(self.frame, text=file_name, width=200, bg="lightblue")
        self.label.pack()

        self.scrollbar = tk.Scrollbar(self.frame)
        self.text = tk.Text(self.frame, width=200)

        self.text.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.insert(tk.END, joined_diff)

        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


class ResultDir:
    def __init__(self, master, directori):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(self.frame, text=directori, width=120, bg="lightblue")
        self.label.pack()

        for root, dirs, files in os.walk(directori, topdown=True):
            for dir_item in dirs:
                self.label = tk.Label(self.frame, text=os.path.join(root, dir_item), width=120)
                self.label.pack()
            for file_item in files:
                self.label = tk.Label(self.frame, text=os.path.join(root, file_item), width=120)
                self.label.pack()

        self.label = tk.Label(self.frame, width=120)
        self.label.pack()

        self.frame.pack()


class ResultCheck:
    def __init__(self, master, check):
        self.master = master
        self.frame = tk.Frame(master)

        b = tk.Label(self.frame, text="file")
        b.grid(row=0, column=0)
        b = tk.Label(self.frame, text="lines")
        b.grid(row=0, column=1)
        b = tk.Label(self.frame, text="dirs")
        b.grid(row=0, column=2)
        b = tk.Label(self.frame, text="trad")
        b.grid(row=0, column=3)
        i = 1
        for file_item in FILES:
            b = tk.Label(self.frame, text=file_item)
            b.grid(row=i, column=0)
            b = tk.Label(self.frame, text=check[file_item]["file_count"])
            b.grid(row=i, column=1)
            b = tk.Label(self.frame, text=check[file_item]["directori_count"])
            b.grid(row=i, column=2)
            b = tk.Label(self.frame, text=check[file_item]["translations_count"])
            b.grid(row=i, column=3)
            i += 1

        self.frame.pack()


class TkDirectoryDialog(tk.Frame):
    def __init__(self, root, parent):
        tk.Frame.__init__(self, root)
        self.parent = parent
        button_opt = {'fill': tk.BOTH, 'padx': 5, 'pady': 5}
        tk.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)
        self.dir_opt = options = {}
        options['initialdir'] = INITIAL_DIR
        options['mustexist'] = True
        options['parent'] = root
        options['title'] = 'Escollir directori'

    def askdirectory(self):
        new_directory = tkFileDialog.askdirectory(**self.dir_opt)
        self.parent.directory_field_entry["text"] = new_directory
        self.parent.directory_field_entry.update()
        self.parent.directory_field = new_directory


def main():
    root = tk.Tk()
    Main(root)
    root.mainloop()

if __name__ == '__main__':
    main()

