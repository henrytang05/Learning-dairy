import csv
from tabulate import tabulate
from datetime import datetime
from cs50 import SQL
import os
import re

run = True


def append_concept():
    global run
    print(
        "Type 'Done' to the program",
        "Type 'Exit' to stop adding new concepts",
        sep="\n",
    )

    while run:
        concept_learned = input("What have you learned today: ").capitalize()
        if concept_learned == "Done":
            os.system("cls")
            print("Nice job! You have learned a lot today!")
            return
        elif concept_learned == "Exit":
            os.system("cls")
            run = False
            return
        else:
            if concept_learned != "\n" and not concept_learned.strip():
                today = datetime.now().strftime("%Y-%m-%d")
                db.execute(
                    "INSERT INTO learning (date, concept) VALUES (?, ?)",
                    today,
                    concept_learned,
                )


def view_concept():
    os.system("cls")
    concepts_dict = {}
    reader = db.execute("SELECT * FROM learning")
    for row in reader:
        date = row["date"]
        concept = row["concept"]
        index = row["id"]

        if date in concepts_dict:
            concepts_dict[date].append({"ID": index, "Concept": concept})
        else:
            concepts_dict[date] = [{"ID": index, "Concept": concept}]
    if concepts_dict == {}:
        print("You haven't learned anything yet!")
        return

    table_data = []
    for date, concepts in concepts_dict.items():
        for idx, concept in enumerate(concepts):
            if idx == 0:
                table_data.append([date, concept["ID"], concept["Concept"]])
            else:
                table_data.append(["", concept["ID"], concept["Concept"]])

    headers = ["Date", "ID", "Concept"]

    print(tabulate(table_data, headers, tablefmt="grid"))


def delete_concept():
    os.system("cls")
    view_concept()
    print("Type 'Back' to stop deleting concepts\n")
    while True:
        try:
            sequence = input(
                "Enter the ID of the concept you want to delete: "
            ).capitalize()
            if sequence == "Back":
                os.system("cls")
                return
            numbers = re.findall(r"\d+", sequence)
            delete_items = sorted([int(num) for num in numbers])
        except (TypeError, ValueError):
            print("Please enter a valid ID")
        else:
            break
    print()
    print(
        f"Are you sure you want to delete these concepts?: {','.join(map(str,delete_items))}"
    )
    while True:
        try:
            user_input = input("Press 'Y' to confirm, 'N' to cancel: ").strip().lower()
            if user_input[0] == "n":
                os.system("cls")
                print("Delete canceled")
                return
            elif user_input[0] == "y":
                # Perform delete operation here
                print("Deletion confirmed\n")
                break
            else:
                raise ValueError("Please enter a valid input")
        except (ValueError, IndexError) as e:
            print(e)
    for idx in delete_items:
        if db.execute("SELECT * FROM learning WHERE id = ?", idx) == []:
            print(f"ID {idx} not found")
        else:
            db.execute("DELETE FROM learning WHERE id = ?", idx)
            print(f"Concept {idx}: Successfully deleted")
    input("Press enter to continue\n")
    os.system("cls")


if __name__ == "__main__":
    os.system("cls")
    db = SQL("sqlite:///learning.db")
    while run:
        print("Menu: ")
        print("1. Add Concept")
        print("2. View Concept")
        print("3. Delete Concept")
        print("4. Exit")
        try:
            choice = int(input("Type your choice here: "))
        except ValueError:
            os.system("cls")
            print("Please enter a valid number")
            continue
        os.system("cls")
        if choice == 1:
            append_concept()
        elif choice == 2:
            view_concept()
        elif choice == 3:
            delete_concept()
        elif choice == 4:
            run = False
    input("Thanks for using!")
