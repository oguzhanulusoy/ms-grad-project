DEBUG = False
TABLE_STARTING_WITH = "["
ATTRIBUTE_STARTING_WITH = "+"
ATTRIBUTE_ENDING_WITH = ";"
MULTIPLICITY_LINE = " *;"
PRIMARY_KEY_LINE = " PK;"
ENTITY_ENDING_WITH = "|"
TABLE_ENDING_WITH = "]\n"

def createDiagramContent(ENTITY_LIST):
    result = "\""
    for entity in ENTITY_LIST:
        result = result.__add__(TABLE_STARTING_WITH)
        result = result.__add__(entity.getName()).__add__(ENTITY_ENDING_WITH)
        for attribute in entity.getAttributes():
            attribute_line = ATTRIBUTE_STARTING_WITH
            attribute_line = attribute_line.__add__(attribute.getName())
            if eval(attribute.isMultiValued()):
                attribute_line = str(attribute_line).__add__(MULTIPLICITY_LINE)
            elif eval(attribute.isPrimaryKey()):
                attribute_line = str(attribute_line).__add__(PRIMARY_KEY_LINE)
            else:
                attribute_line = str(attribute_line).__add__(ATTRIBUTE_ENDING_WITH)
            result = result.__add__(attribute_line)
        if result[-1].__eq__(ATTRIBUTE_ENDING_WITH):
            result = result[:-1]
        result = result.__add__(TABLE_ENDING_WITH)
    result = result.__add__("\"")
    if DEBUG:
        print("RESULT = {}".format(result))
    createDiagram(context=result)

def nameUtil():
    result = ""
    import random
    for i in range(0, 6):
        number = random.randint(1, 30)
        result = result.__add__(str(number))
    return result

def createDiagram(context):
    command = ""
    command = command.__add__("echo ")
    command = command.__add__(context)
    command = command.__add__(" | ./diagrammer/yuml/yuml -t class -s scruffy -o ./diagrammer/output/")
    command = command.__add__(nameUtil())
    command = command.__add__(".png")

    if DEBUG:
        print("COMMAND = {}".format(command))
    import os
    execute = os.system(command.format(context))
