###################################
###################################
###                             ###
###       CONFIGURATIONS        ###
###                             ###
###################################
###################################
SPECIAL_VERB_LIST = ["has"]
SUBJECT_DEPS_LIST = ["nsubj", "nsubjpass"]
TABLE_SIZE = 60
IS_DEBUG = False
IS_TRACE = True

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
ROOT = 'ROOT'
ADJECTIVE = "ADJ"
UNIQUE_KEY = "unique"
MANY_KEY = "many"
PRIMARY_KEY = " PK"
MULTIVALUE_KEY = " *"
RELATION = "RELATIONS"

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