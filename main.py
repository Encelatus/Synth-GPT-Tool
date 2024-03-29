from convert import main_convert
from prompt import main_prompt  # Assuming you've created a main_prompt function in prompt.py
from store import main_store    # Assuming you've created a main_store function in store.py
from response import main_question  # Assuming you've created a main_question function in question.py

def main():
    main_convert()
    main_prompt()
    main_store()
    # main_question()

if __name__ == "__main__":
    main()
