import spacy
from object import sentence as s
#python -m spacy download en_core_web_sm

nlp = spacy.load("en_core_web_sm")
doc = nlp("Each red musician takes a database management systems unique SSN, many name, an address, and a department head. Each song recorded at Music Company has a title and an author.")
sentences = list(doc.sents)

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
            previousWord = sentence.__getitem__(i).text + " " + sentence.__getitem__(i).head.text + " " + sentence.__getitem__(i+1).head.text
            nouns.append(previousWord)

    object = nouns

    instance = s.sentence(subject=subject, verb=verb, object=object, primaryKeys=primaryKeys, multiplicities=multiplicities)

    return instance



specialVerbs = ["has"]
entity_list = ["musician"]
def heuristicMachine(sentence):
    subject = sentence.getSubject()
    verb = sentence.getVerb()
    object = sentence.getObject()


    # attribute iliskisi gelecek
    if verb in specialVerbs:
        print("oguzhan")

        # subject varsa attribute ları ekle
        if subject[0] in entity_list:
            print("ulusoy")

        # yeni yarat
        else:
            print()

    # normal relation gelecek
    else:
        print()




sentenceList = []
#createSentence(sentences[0])
for sentence in sentences:
    instance = createSentence(sentence)
    heuristicMachine(instance)
    sentenceList.append(instance)

