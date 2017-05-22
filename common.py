# -*- coding: cp1252 -*-

INITIAL_DIR = 'C:\\Users\\varqjrf\\PycharmProjects\\Migration\\files'

# http://docs.python-requests.org/en/master/
BEX_USER_URL = 'https://www.user.generali.es/dfw6k/arq_decenalFormWeb/viewDocument.po?sessionState=new&tarea=directView&viewDocument.refDocument=%s'
BEX_TEST_URL = 'https://www.test.generali.es/dfw4k/arq_decenalFormWeb/viewDocument.po?sessionState=new&tarea=directView&viewDocument.refDocument=%s'
LOGIN_USER_URL = 'https://www.user.generali.es/dfw6k/arq_decenalFormWeb/pkmslogin.form'
LOGIN_TEST_URL = 'https://www.test.generali.es/dfw4k/arq_decenalFormWeb/pkmslogin.form'
USERNAME = "varqjrf"
PASSWORD = "Tuxedo02"

CATEGORIAS_FILE = u"categorias.txt"
COMPONENTES_FILE = u"componentes.txt"
CONTENIDOS_FILE = u"contenidos.txt"
CONTIENES_FILE = u"contienes.txt"
DOCUMENTOS_FILE = u"documentos.txt"
ENLACES_FILE = u"enlaces.txt"
METADATOS_FILE = u"metadatos.txt"
MULTIMEDIAS_FILE = u"multimedias.txt"
NODOSMENU_FILE = u"nodosMenu.txt"
PAGINAS_FILE = u"paginas.txt"
TEXTOS_FILE = u"textos.txt"
TRADUCCIONES_FILE = u"traducciones.txt"
VISTAS_FILE = u"vistas.txt"
ZONAS_FILE = u"zonas.txt"
PLANTILLAS_FILE = u"plantillas.txt"
FILES = [CATEGORIAS_FILE, COMPONENTES_FILE, CONTENIDOS_FILE, CONTIENES_FILE, DOCUMENTOS_FILE, ENLACES_FILE, METADATOS_FILE,
         MULTIMEDIAS_FILE, NODOSMENU_FILE, PAGINAS_FILE, TEXTOS_FILE, TRADUCCIONES_FILE, VISTAS_FILE, PLANTILLAS_FILE, ZONAS_FILE]

COMP_DIR = u"comp"
DOC_DIR = u"doc"
IMG_DIR = u"img"
TEXTO_DIR = u"texto"

categorias_fields = ['id', 'tipo', 'literal']
componentes_fields = ['id', 'fechaModificacion', 'tipo', 'usuarioModificacion', 'liten', 'dest', 'texto', 'imagen', 'tipen', 'titulo2', 'titulo', 'titulo3', 'clase', 'itemId']
contenidos_fields = ['id', 'cia', 'fechaCreacion', 'fechaModificacion', 'fkExpediente', 'plant', 'referencia', 'tipo', 'usuarioCreacion', 'usuarioModificacion']
contienes_fields = ['estado', 'fkHijo', 'fkPadre', 'orden', 'tipoRelacion']
documentos_fields = ['id', 'tipo', 'nombreVideo', 'tipoDoc', 'fechaCaducidad', 'fechaEfecto', 'documentoPath', 'titulo', 'descripcion', 'itemId', 'literal']
enlaces_fields = ['id', 'tipo', 'peso', 'tipoContenidoEnlazado', 'enlacePath', 'servicioOpcional', 'destino', 'titulo', 'contenidoEnlazado', 'transaccional', 'parametros', 'tipoURL', 'iconos', 'abrirEnVentanaNueva', 'paramOpcional', 'literal']
metadatos_fields = ['id', 'tipo', 'valor', 'name', 'metaType']
multimedias_fields = ['id', 'tipo', 'multimediaPath', 'textoAlternativo', 'descLarga', 'alto', 'fechaEfecto', 'ancho', 'itemId']
nodosmenu_fields = ['id', 'tipo', 'literal']
paginas_fields = ['id', 'tipo', 'plantilla', 'literal']
textos_fields = ['id', 'tipo', 'itemId']
vistas_fields = ['id', 'tipo', 'categoria', 'literal']
traducciones_fields = ['traduccion', 'tipoTrad', 'idioma', 'usuarioReserv', 'estadoTrad', 'usuarioModificacion', 'campo', 'idContenido']
zonas_fields = ['id', 'relacionId', 'maxHijos', 'tiposPermitidos', 'orden', 'fechaModificacion', 'usuarioModificacion', 'minHijos', 'fechaCreacion', 'usuarioCreacion', 'fkPlantilla', 'relacionesDesc']
plantillas_fields = ['id', 'referencia', 'jsp', 'fechaModificacion', 'usuarioModificacion', 'fechaCreacion', 'usuarioCreacion']

fields_dict = {"categorias": categorias_fields,
               "componentes": componentes_fields,
               "contenidos": contenidos_fields,
               "contienes": contienes_fields,
               "documentos": documentos_fields,
               "enlaces": enlaces_fields,
               "metadatos": metadatos_fields,
               "multimedias": multimedias_fields,
               "nodosmenu": nodosmenu_fields,
               "paginas": paginas_fields,
               "textos": textos_fields,
               "vistas": vistas_fields,
               "traducciones": traducciones_fields,
               "zonas": zonas_fields,
               "plantillas": plantillas_fields}


