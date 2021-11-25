from ERD import run

text = "A university contains many faculty. Faculty has unique identification number and name. Each department belongs to a faculty. A department has identification number, name, head, phone numbers. Many students register into programme. A course includes prefix, unique identification number, title and description. Each department opens courses in a semester. And, students take courses."
# text = "A musician sings many songs. Musicians take many course. Each red musician has unique number, a name, " \
#       "an addresses. Musician has phone numbers. Each song recorded at Music Company has a unique title and an " \
#       "author. "
# text = "A course is taken by students."
print(text)
while True:
    choice = int(input("Press one for sample data, two to use your own data => "))
    document = ''
    if choice == 1:
        document = text
        run(document=document)
    elif choice == 2:
        document = input("Enter your text => ")
        run(document=document)
    elif choice == 3:
        print("You have exited.")
        break
    # WARNING: This choice is to delete all files after a sample iteration is executed
    # For example output under diagrammer, log file, output files
    elif choice == 666:
        import os
        try:
            dir = 'diagrammer/output'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
            os.remove(os.path.join("", "app.log"))
            from settings import *
            os.remove(os.path.join("", XML_OUTPUT_FILE))
            os.remove(os.path.join("", TXT_OUTPUT_FILE))
        except Exception as exception:
            print()
    else:
        print("You did invalid choice.")
