import nltk as nltk
import spacy
from object import sentence as s
from object import attribute as a
from object import entity as e
#python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_sm")
doc = nlp("Each red musician has a database management systems unique SSN, many names, an addresses, and a department head. Each song recorded at Music Company has a title and an author.")
sentences = list(doc.sents)

ATTRIBUTE_LIST = []
ENTITY_LIST = []
RELATION_LIST = []

def createSentence(sentence):

    subject = None
    verb = None
    object = None

    multiplicities = []
    primaryKeys = []

    #get subject part
    SUBJECTS = ["nsubj","nsubjpass"] ## add or delete more as you wish
    subject = [tok.text for tok in sentence if (tok.dep_ in SUBJECTS) ]


    #get verb part
    for token in sentence:
        if token.pos_ == 'VERB' and token.dep_ == 'ROOT':
            verb = token.text


    #get object part
    previousWord = ""
    nouns = []

    for i in range (0, len(sentence)-1):

        if str(sentence.__getitem__(i).text) not in previousWord and str(sentence.__getitem__(i).dep_) != "compound":
            if sentence.__getitem__(i).pos_ == "NOUN":
                if sentence.__getitem__(i).text not in subject:
                    nouns.append(doc.__getitem__(i).text)

            if sentence.__getitem__(i).pos_ == "ADJ":
                if sentence.__getitem__(i).text == "unique":
                    primaryKeys.append(sentence.__getitem__(i+1).text)

                if str(sentence.__getitem__(i).text).lower() == "many":
                    multiplicities.append(doc.__getitem__(i+1).text)

        if str(sentence.__getitem__(i).text) not in previousWord and str(sentence.__getitem__(i).dep_) == "compound" and str(sentence.__getitem__(i+1).dep_) != "compound":
            previousWord = sentence.__getitem__(i).text + " " + sentence.__getitem__(i).head.text
            nouns.append(previousWord)

        if str(sentence.__getitem__(i).dep_) == "compound" and str(sentence.__getitem__(i+1).dep_) == "compound":
            previousWord = sentence.__getitem__(i).text + " " + sentence.__getitem__(i+1).text + " " + sentence.__getitem__(i).head.text
            nouns.append(previousWord)

    object = nouns
    instance = s.sentence(subject=subject, verb=verb, object=object, primaryKeys=primaryKeys, multiplicities=multiplicities)

    return instance



specialVerbs = ["has"]
entity_list = [""]
def heuristicMachine(sentence):
    subject = sentence.getSubject()
    verb = sentence.getVerb()
    object = sentence.getObject()



    # attribute iliskisi gelecek
    if verb in specialVerbs:
        # subject varsa attribute ları ekle
        if subject[0] in entity_list:
            print()

        # yeni yarat
        else:
            print( "geldim")
            makeEntity(sentence=sentence)

    # normal relation gelecek
    else:
        print()


def getSingularNoun(noun):
    lemma = nltk.wordnet.WordNetLemmatizer()
    return lemma.lemmatize(noun)

def makeEntity(sentence):

    primaryKeys = sentence.getPk()
    subject = sentence.getSubject()
    object = sentence.getObject()

    print(object)
    attributes = []
    # Create attribute, then convert the result into a list
    for item in object:
        isPrimaryKey = False
        if item in primaryKeys:
            isPrimaryKey = True

        # karsilastir, cogul mu diye bakıver.
        # get singular form

        newAttribute = a.attribute(getSingularNoun(item), isPrimaryKey, False)
        attributes.append(newAttribute)
        ATTRIBUTE_LIST.append(newAttribute)

    #singular form
    newEntity = e.entity(name=getSingularNoun(subject), attributes=attributes)
    ENTITY_LIST.append(newEntity)

    for i in attributes:
        print(i.getName())
    return None


''' TEST '''
test_sentence = sentences[0]
test_instance = createSentence(test_sentence)
heuristicMachine(test_instance)

'''RUN
sentenceList = []
#createSentence(sentences[0])
for sentence in sentences:
    instance = createSentence(sentence)
    heuristicMachine(instance)
    sentenceList.append(instance)
'''

