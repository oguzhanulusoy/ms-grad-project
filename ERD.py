###################################
###################################
###                             ###
###            LIBS             ###
###                             ###
###################################
###################################
from datetime import datetime
from settings import *
import nltk as nltk
import spacy
import logging
#python -m spacy download en_core_web_sm
#pip freeze > requirements.txt

###################################
###################################
###                             ###
###           OBJECT            ###
###                             ###
###################################
###################################
from object import sentence as s
from object import attribute as a
from object import entity as e
from object import relation as r

###################################
###################################
###                             ###
###            DEBUG            ###
###                             ###
###################################
###################################
isDebug = IS_DEBUG
isTrace = IS_TRACE

###################################
###################################
###                             ###
###             SETUP           ###
###                             ###
###################################
###################################
def setup():
    logging.basicConfig(filename='app.log', format='%(message)s', level=logging.DEBUG)
    if isDebug:
        logging.debug("Running right now => " + str(datetime.now()))

###################################
###################################
###                             ###
###            RUN              ###
###                             ###
###################################
###################################
def run(document):
    setup()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(str(document))
    sentences = list(doc.sents)

    for sentence in sentences:
        print(sentence)

    sentenceList = []
    for sentence in sentences:
        instance = analyzer(sentence)
        fsm(instance)
        sentenceList.append(instance)

    if isTrace:
        if isDebug:
            logging.debug("Drawing right now => " + str(datetime.now()))
        maker()

###################################
###################################
###                             ###
###        GLOBAL LISTS         ###
###                             ###
###################################
###################################
ATTRIBUTE_LIST = []
ENTITY_LIST = []
RELATION_LIST = []

###################################
###################################
###                             ###
###           HELPERS           ###
###                             ###
###################################
###################################
def getEntity(subject):
    for item in ENTITY_LIST:
        if str(item.getName()).lower() == str(subject).lower():
            entity = item
    return entity

def hasEntity(subject):
    for item in ENTITY_LIST:
        if str(item.getName()).lower() == str(subject).lower():
            return True
    return False

def isAttribute(verb):
    if verb in SPECIAL_VERB_LIST:
        return True
    return False

def isSingle(subject):
    if str(subject).lower().__eq__(getSingularNoun(str(subject).lower())):
        return True
    return False

def getSingularNoun(noun):
    lemma = nltk.wordnet.WordNetLemmatizer()
    nouns = noun.split(" ")
    singleForm = ''
    size = len(nouns)

    if size.__eq__(1):
        singleForm = lemma.lemmatize(noun)
        return singleForm

    for item in range(0, size-1):
        singleForm += str(nouns[item] + " ")
    singleForm += str(lemma.lemmatize(nouns[size-1]))
    return singleForm

def getSingularVerb(word):
    stemmer = nltk.SnowballStemmer("english")
    return stemmer.stem(word)

###################################
###################################
###                             ###
###          ANALYZER           ###
###                             ###
###################################
###################################
def analyzer(sentence):

    if isDebug:
        logging.debug("#####################################################")
        logging.debug("createSentence method is starting for given sentence:")
        logging.debug(sentence)

    subject = []
    verb = None
    object = None

    # retrieve subject part from the sentence
    for token in sentence:
        if token.dep_ in SUBJECT_DEPS_LIST:
            subject.append(token.text)
    if isDebug:
        logging.debug("\t Subject => " + str(subject[0]))

    # retrieve verb part from the sentence
    for token in sentence:
        if token.pos_ == VERB and token.dep_ == ROOT:
            verb = token.text
    if isDebug:
        logging.debug("\t Verb => " + str(verb))

    # retrieve object part from the sentence
    previousWord = ""
    noun = ""
    nouns = []
    isMultiplicity = False
    multiplicities = []
    isPrimaryKey = False
    primaryKeys = []

    for i in range(0, len(sentence)-1):

        try:
            # to find primary key
            if sentence.__getitem__(i).pos_ == ADJECTIVE:
                # to find primary key through many adjective
                if sentence.__getitem__(i).text == UNIQUE_KEY:
                    isPrimaryKey = True
                # to find multiplicity through many adjective
                if str(sentence.__getitem__(i).text).lower() == MANY_KEY:
                    isMultiplicity = True
        except:
            if isDebug:
                logging.error("Analyzer has got and error while parsing multiplicity or primary key")

        try:
            # add one word noun
            if str(sentence.__getitem__(i).text) not in previousWord and str(sentence.__getitem__(i).dep_) != COMPOUND:
                if sentence.__getitem__(i).pos_ == NOUN:
                    if sentence.__getitem__(i).text not in subject:
                        noun = str(sentence.__getitem__(i).text)
        except:
            if isDebug:
                logging.error("Analyzer has got an error while parsing the one word noun => " + str(sentence.__getitem__(i).text))

        try:
            # add two words noun
            if str(sentence.__getitem__(i).text) not in previousWord and str(sentence.__getitem__(i).dep_) == COMPOUND and str(sentence.__getitem__(i+1).dep_) != COMPOUND:
                previousWord = sentence.__getitem__(i).text + " " + sentence.__getitem__(i).head.text
                noun = previousWord
        except:
            if isDebug:
                logging.error("Analyzer has got an error while parsing the two words noun => " + str(sentence.__getitem__(i).text + " " + sentence.__getitem__(i).head.text))

        try:
            # add three words noun
            if str(sentence.__getitem__(i).dep_) == COMPOUND and str(sentence.__getitem__(i+1).dep_) == COMPOUND:
                previousWord = sentence.__getitem__(i).text + " " + sentence.__getitem__(i+1).text + " " + sentence.__getitem__(i).head.text
                noun = previousWord
        except:
            if isDebug:
                logging.error("Analyzer has got an error while parsing the three words noun => " + str(sentence.__getitem__(i).text + " " + sentence.__getitem__(i+1).text + " " + sentence.__getitem__(i).head.text))

        if not noun.__eq__(''):
            nouns.append(noun)

            if isPrimaryKey:
                primaryKeys.append(noun)
                isPrimaryKey = False

            if isMultiplicity:
                multiplicities.append(noun)
                isMultiplicity = False

            noun = ''

    object = nouns
    if isDebug:
        logging.debug("\t Object => " + str(object))

    instance = s.sentence(subject=subject, verb=verb, object=object, primaryKeys=primaryKeys, multiplicities=multiplicities)
    if isDebug:
        logging.debug("\t Primary keys (if exists) => " + str(instance.getPrimaryKeys()))
        logging.debug("\t Multiplicities (if exists) => " + str(instance.getMultiplicities()))
    return instance

###################################
###################################
###                             ###
###       ERD COMPONENTS        ###
###                             ###
###################################
###################################
def fsm(sentence):
    if isDebug:
        logging.debug("fsm method is starting for given sentence:")
        logging.debug(sentence)

    subject = sentence.getSubject()
    verb = sentence.getVerb()
    object = sentence.getObject()
    if isDebug:
        logging.debug("\t Subject => " + str(subject))
        logging.debug("\t Verb => " + str(verb))
        logging.debug("\t Object => " + str(object))

    isSinglePerson = isSingle(subject)
    if isDebug:
        logging.debug("\t isSinglePerson => " + str(isSinglePerson))

    # attribute-based relation
    if isAttribute(verb=verb):
        if isDebug:
            logging.debug("\t\t A special verb is found => " + str(verb))

        # if subject exists, modify
        if hasEntity(subject=subject):
            if isDebug:
                logging.debug("\t\t The entity already exists => " + str(subject))
            try:
                modifyEntity(sentence=sentence, isSinglePerson=isSinglePerson)
            except:
                if isDebug:
                    logging.error("\t\t An error for modifyEntity => " + str(subject))
            if isDebug:
                logging.debug("\t\t Finally modified entity => " + str(subject))

        # otherwise, create new
        else:
            if isDebug:
                logging.debug("\t\t The entity is not found => " + str(subject))
            try:
                createEntity(sentence=sentence, isSinglePerson=isSinglePerson)
            except:
                if isDebug:
                    logging.error("\t\t An error for createEntity => " + str(subject))
            if isDebug:
                logging.debug("\t\t Finally created entity => " + str(subject))

    # non attribute-based relation
    else:
        if isDebug:
            logging.debug("\t\t A special verb is NOT found => " + str(verb))
        try:
            createRelation(sentence=sentence)
        except:
            if isDebug:
                logging.error("\t\t An error for createRelation => " + str(verb))
        if isDebug:
            logging.debug("\t\t Finally created relation => " + str(verb))

###################################
###################################
###                             ###
###            RULES            ###
###                             ###
###################################
###################################
def createRelation(sentence):

    if isDebug:
        logging.debug("\t\t\tcreateRelation method is starting...")

    subject = sentence.getSubject().lower()
    verb = sentence.getVerb().lower()
    object = sentence.getObject()
    object = str(object[0]).lower()
    multiplicities = sentence.getMultiplicities()

    if isDebug:
        logging.debug("\t\t\t\t Subject => " + str(subject))
        logging.debug("\t\t\t\t Verb => " + str(verb))
        logging.debug("\t\t\t\t Object => " + str(object))
        logging.debug("\t\t\t\t Multiplicities => " + str(multiplicities))

    processedSubject = getSingularNoun(subject)
    processedVerb = getSingularVerb(verb)
    processedObject = getSingularNoun(object)

    if isDebug:
        logging.debug("\t\t\t\t Processed subject => " + str(processedSubject))
        logging.debug("\t\t\t\t Processed verb => " + str(processedVerb))
        logging.debug("\t\t\t\t Processed object => " + str(processedObject))

    m1 = ''
    m2 = ''

    # i.e. Student takes courses
    if processedSubject.__eq__(subject) and not processedObject.__eq__(object):
        m1 = '1'
        m2 = 'N'

    # i.e. Student takes course
    if processedSubject.__eq__(subject) and processedObject.__eq__(object):
        m1 = '1'
        m2 = '1'

    # i.e. Students take courseS
    if not processedSubject.__eq__(subject) and not processedObject.__eq__(object):
        m1 = 'N'
        m2 = 'N'

    # i.e. Students take course
    if not processedSubject.__eq__(subject) and processedObject.__eq__(object):
        m1 = 'N'
        m2 = '1'

    if str(subject).lower() in multiplicities:
        m1 = 'N'

    if str(object).lower() in multiplicities:
        m2 = 'N'

    if isDebug:
        logging.debug("\t\t\t\t Relation between " + subject + " and " + object + " => " + m1 + " - " + m2)

    new_relation = r.relation(who=processedSubject,
                              action=processedVerb,
                              whom=processedObject)
    new_relation.setMultiplicityOne(m1)
    new_relation.setMultiplicityTwo(m2)
    RELATION_LIST.append(new_relation)

def createAttribute(sentence, isSinglePerson):

    primaryKeys = sentence.getPrimaryKeys()
    object = sentence.getObject()
    subject = sentence.getSubject()
    multiplicities = sentence.getMultiplicities()

    if isDebug:
        logging.debug("\t\t\tcreateAttribute method is starting...")
        logging.debug("\t\t\t\t isSinglePerson => " + str(isSinglePerson))
        logging.debug("\t\t\t\t Object => " + str(object))
        logging.debug("\t\t\t\t Subject => " + str(subject))
        logging.debug("\t\t\t\t Primary Keys => " + str(primaryKeys))
        logging.debug("\t\t\t\t Multiplicities => " + str(multiplicities))

    attributes = []
    counter = 1
    for item in object:
        isPrimaryKey = False
        if item in primaryKeys:
            isPrimaryKey = True

        processedItem = getSingularNoun(item)
        isMultiValued = False
        if isSinglePerson:
            if not processedItem.__eq__(item):
                isMultiValued = True

        if item in multiplicities:
            isMultiValued = True

        if isDebug:
            logging.debug("\t\t\t\t\t" + str(counter) + ". attribute => " + str(processedItem) + " {PK: " + str(isPrimaryKey) + "; Multi-valued: " + str(isMultiValued) + "}")

        counter += 1
        newAttribute = a.attribute(processedItem, isPrimaryKey, isMultiValued)
        attributes.append(newAttribute)
        ATTRIBUTE_LIST.append(newAttribute)

    return attributes

def createEntity(sentence, isSinglePerson):

    if isDebug:
        logging.debug("\t\t\tcreateEntity method is starting...")

    primaryKeys = sentence.getPrimaryKeys()
    subject = sentence.getSubject()
    object = sentence.getObject()

    if isDebug:
        logging.debug("\t\t\t\t Primary keys => " + str(primaryKeys))
        logging.debug("\t\t\t\t Subject => " + str(subject))
        logging.debug("\t\t\t\t Object => " + str(object))
        logging.debug("\t\t\t\t isSinglePerson => " + str(isSinglePerson))

    attributes = createAttribute(sentence=sentence, isSinglePerson=isSinglePerson)
    newEntity = e.entity(name=getSingularNoun(subject), attributes=attributes)
    ENTITY_LIST.append(newEntity)
    if isDebug:
        logging.debug("\t\t\t\t Entity is created => " + str(subject))

def modifyEntity(sentence, isSinglePerson):

    if isDebug:
        logging.debug("\t\t\tmodifyEntity method is starting...")

    primaryKeys = sentence.getPrimaryKeys()
    subject = sentence.getSubject()
    object = sentence.getObject()

    if isDebug:
        logging.debug("\t\t\t\t Primary keys => " + str(primaryKeys))
        logging.debug("\t\t\t\t Subject => " + str(subject))
        logging.debug("\t\t\t\t Object => " + str(object))
        logging.debug("\t\t\t\t isSinglePerson => " + str(isSinglePerson))

    attributes = createAttribute(sentence=sentence, isSinglePerson=isSinglePerson)
    entity = getEntity(subject)
    e.entity.setAttributes(entity, attributes)
    if isDebug:
        logging.debug("\t\t\t\t Entity is found => " + str(entity.getName()))

def modifyAttribute(entityName, attributeName):
    entity = getEntity(subject=entityName)
    for attribute in entity.getAttributes():
        if str(attribute.getName).lower().__eq__(str(attributeName).lower()):
            attribute.setPrimaryKey(True)
            if isDebug:
                logging.debug("Modified attribute => " + str(attribute.getName()))

###################################
###################################
###                             ###
###           MAKER             ###
###                             ###
###################################
###################################
def maker():
    for entity in ENTITY_LIST:
        print(line_border())
        print(table_line(entity.getName()))
        print(line_border())
        for attribute in entity.getAttributes():
            attribute_line = attribute.getName()
            if eval(attribute.isMultiValued()):
                attribute_line = str(attribute_line).__add__(MULTIVALUE_KEY)
            if eval(attribute.isPrimaryKey()):
                attribute_line = str(attribute_line).__add__(PRIMARY_KEY)
            print(item_line(attribute_line))
        print(line_border())
        print()

    if len(RELATION_LIST) > 0:
        print(line_border())
        print(table_line(RELATION))
        print(line_border())
        for relation in RELATION_LIST:
            print(relation_line(" (" + relation.getMultiplicityOne() + ") " + relation.who + " -> " + relation.action + " -> (" + relation.getMultiplicityTwo() + ") " + relation.whom))
            print(line_border())
    print("* means multi-valued and pk is primary key.")

