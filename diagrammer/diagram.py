'''
:param entities: contains all entitiy objects with their own attributes
:type entities: list
:param relations: contains all relations between two entities
:type relations: list
:param document: contains raw data from console
:type document: str
:returns: filename
:rtype: str
'''
def createERDiagram(entities, relations, document):
    import graphviz
    file = nameUtil() + ".gv"
    # To convert .gv file to png
    # Please use this tool: https://convertio.co/tr/gv-png/
    e = graphviz.Graph('ER', filename=file, engine='neato', directory='diagrammer/output/')

    # For each entity in entity list, create a box shape
    # Place the entity inside of the shape
    # Retrieve all attributes of current entity
    # Decide which shape will be used
    # Create a double circle or ellipse shape
    # Place the attribute inside of the shape
    # If it is primary key, add a star
    for entity in entities:
        e.attr('node', shape='box')
        e.node(entity.getName())
        for attribute in entity.getAttributes():
            attribute_line = attribute.getName()
            if eval(attribute.isMultiValued()):
                e.attr('node', shape='doublecircle')
            else:
                e.attr('node', shape='ellipse')
            if eval(attribute.isPrimaryKey()):
                attribute_line = str(attribute_line).__add__(" pk")
            e.node(attribute_line)
            e.edge(entity.getName(), attribute_line)

    # If there is any relation, edges should be determined
    # For each relation in relationship list, do these:
    # Create a diamond shape with a style and color
    # Place the current relation inside of the shape
    # Add nodes (who, whom)
    # Add multiplicities (who, whom)
    if len(relations) > 0:
        for relation in relations:
            e.attr('node', shape='diamond', style='filled', color='lightgrey')
            e.node(relation.action)
            e.edge(relation.who, relation.action, label=relation.getMultiplicityOne(), len='1.00')
            e.edge(relation.action, relation.whom, label=relation.getMultiplicityTwo(), len='1.00')

    # We may not want to see full text in the figure
    # It can be controlled with a flag
    # that is called isPrint
    # If this block is executed, import nltk and download punkt for dividing a text into sentences
    # This is implemented to convert a full text into paragraphe
    # Otherwise, filename is displayed
    if isPrint:
        import nltk
        nltk.download('punkt')
        sentences = nltk.tokenize.sent_tokenize(document)
        text = ""
        for sentence in sentences:
            text = text.__add__(sentence).__add__("\n")
        e.attr(label=r'\n\n{}'.format(text))
        e.attr(fontsize='20')
    else:
        e.attr(label=r'\n\n{}'.format(file))
        e.attr(fontsize='20')

    try:
        e.view()
    except Exception as exception:
        print("An exception occured when ER diagram has been created. It is following {}.".format(exception))

    return file

isPrint = True
isDebug = True
TABLE_STARTING_WITH = "["
ATTRIBUTE_STARTING_WITH = "+"
ATTRIBUTE_ENDING_WITH = ";"
MULTIPLICITY_LINE = " *;"
PRIMARY_KEY_LINE = " PK;"
ENTITY_ENDING_WITH = "|"
TABLE_ENDING_WITH = "]\n"

'''
:param entities: contains all entitiy objects with their own attributes
:type entities: list
:returns: filename
:rtype: str
'''
def createClassDiagramContent(entities):
    result = "\""

    # To create a class diagram, specialized format is needed
    # Hereby, a context is made up.
    # Each entitiy in entity list is added into context seperately
    # Each attribute groups of current entity is added into context seperately
    # Finally, we are able to reach to formatted context string
    for entity in entities:
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
    if isDebug:
        print("RESULT = {}".format(result))
    return createClassDiagram(context=result)

'''
:returns: result
:rtype: str
'''
def nameUtil():
    result = ""
    import random
    for i in range(0, 6):
        number = random.randint(1, 30)
        result = result.__add__(str(number))
    return result

'''
:param context: formatted context string
:type context: str
:returns: filename
:rtype: str
'''
def createClassDiagram(context):
    file = nameUtil()

    # In here, a shell command is created
    # yuml library is called with own options
    # Context is appended into command
    # Path is obtained
    # Finally, we are able to see a class diagram
    command = ""
    command = command.__add__("echo ")
    command = command.__add__(context)
    command = command.__add__(" | ./diagrammer/yuml/yuml -t class -s scruffy -o ./diagrammer/output/")
    command = command.__add__(file)
    command = command.__add__(".png")

    if isDebug:
        print("COMMAND = {}".format(command))

    # Import os
    # Then execute shell command
    import os
    execute = os.system(command.format(context))

    return file
