from ERD import run

text = "A university contains many faculty. Faculty has unique identification number and name. Each department belongs to a faculty. A department has identification number, name, head, phone numbers. Many students register into programme. A course includes prefix, unique identification number, title and description. Each department opens courses in a semester. And, students take courses."
# text = "Musicians take many course. Each red musician has unique number, a name, an addresses. Musician has phone numbers. Each song recorded at Music Company has a title and an author."

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
    else:
        print("You did invalid choice.")
