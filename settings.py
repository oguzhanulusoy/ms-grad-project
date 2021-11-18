###################################
###################################
###                             ###
###       CONFIGURATIONS        ###
###                             ###
###################################
###################################
# Constants
SPACY_ENGINE = 'en_core_web_sm'
SPECIAL_VERB_LIST = ["has", "contains", "includes"]
SUBJECT_DEPS_LIST = ["nsubj", "nsubjpass"]
TABLE_SIZE = 60

# Flags
IS_ER_DIAGRAM = True
IS_DEBUG = True
IS_CONSOLE_TRACE = True
IS_CLASS_DIAGRAM = True
IS_XML_OUTPUT_FILE = True
IS_TXT_OUTPUT_FILE = True

# .xml file
XML_OUTPUT_FILENAME = "xml-output"
XML_OUTPUT_FILE_EXTENSION = ".xml"
XML_OUTPUT_FILE = XML_OUTPUT_FILENAME + XML_OUTPUT_FILE_EXTENSION

# .txt file
TXT_OUTPUT_FILENAME = "txt-output"
TXT_OUTPUT_FILE_EXTENSION = ".txt"
TXT_OUTPUT_FILE = TXT_OUTPUT_FILENAME + TXT_OUTPUT_FILE_EXTENSION

###################################
###################################
###                             ###
###         PROPERTIES          ###
###                             ###
###################################
###################################
COMPOUND = "compound"
NOUN = "NOUN"
VERB = 'VERB'
AUX = 'AUX'
POBJ = 'pobj'
NSUBJPASS = 'nsubjpass'
AUXPASS = 'auxpass'
PUNCT = 'PUNCT'
PUNCT_DEP = 'punct'
ROOT = 'ROOT'
ADJECTIVE = "ADJ"
UNIQUE_KEY = "unique"
MANY_KEY = "many"
PRIMARY_KEY = " PK"
MULTIVALUE_KEY = " *"
RELATION = "RELATIONS"
ADP = 'ADP'
DEP = 'agent'
BY_KEY = 'by'

###################################
###################################
###                             ###
###         TABLE FUNC          ###
###                             ###
###################################
###################################
# i.e. +----------------------+
def line_border():
    line_border = "+"

    for i in range (0, TABLE_SIZE - 2):
        line_border += "-"
    line_border += "+"

    return str(line_border)

# i.e. | student              |
def table_line(entity):
    item_line = "| "
    item_line += str(entity).upper()

    for i in range (0, (TABLE_SIZE - 3) - len(str(entity))):
        item_line += " "
    item_line += "|"

    return item_line

# i.e. | + name               |
def item_line(attribute):
    item_line = "| + "
    item_line += str(attribute).capitalize()

    for i in range (0, (TABLE_SIZE - 5) - len(str(attribute))):
        item_line += " "
    item_line += "|"

    return item_line

# i.e. | + name               |
def relation_line(relation):
    item_line = "| "
    item_line += str(relation).capitalize()

    for i in range (0, (TABLE_SIZE - 3) - len(str(relation))):
        item_line += " "
    item_line += "|"

    return item_line