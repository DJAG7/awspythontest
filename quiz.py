import time
import re
import textwrap

def read_quiz(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    questions = re.split(r'^### Question \d+', content, flags=re.MULTILINE)[1:]  # Split using regex pattern
    quiz = []
    for question in questions:
        parts = question.strip().split('\n')
        question_text = parts[0].strip()
        answers = [part.strip() for part in parts[1:] if part.strip()]
        correct_indices = [i for i, ans in enumerate(answers) if '[x]' in ans]
        quiz.append((question_text, answers, correct_indices))
    return quiz

def print_wrapped(text, width=100):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)

def ask_question(question_text, answers, correct_indices):
    print("\n")
    print_wrapped(question_text, width=100)
    for i, answer in enumerate(answers):
        print_wrapped(f"{i + 1}. {answer.replace('[x]', '[ ]')}", width=100)
    
    if len(correct_indices) > 1:
        print("Note: Multiple answers are correct. Separate your answers with commas (e.g., 1,3).")
    else:
        print("Type the option number to answer.")
    
    while True:
        response = input("Your answer: ").strip().upper()
        if len(correct_indices) > 1:
            try:
                response_indices = [int(x) - 1 for x in response.split(',')]
                if set(response_indices) == set(correct_indices):
                    print("Correct!\n")
                    return True
                else:
                    print("Incorrect answer. Please try again.")
            except ValueError:
                print("Invalid input. Please enter the number(s) corresponding to your choice(s).")
        else:
            if response.isdigit() and int(response) - 1 in correct_indices:
                print("Correct!\n")
                return True
            else:
                print("Incorrect answer. Please try again.")

def main():
    file_path = r'C:\Users\danie\Documents\AWS Test\AWS Python Test\quiz.txt'  
    count_file = r'C:\Users\danie\Documents\AWS Test\AWS Python Test\count.txt'
    
    print("Options:")
    print("1. Resume quiz")
    print("2. Reset quiz")
    print("3. Go to question number")
    
    choice = input("Choose an option: ").strip()
    
    if choice == '1':
        pass
    elif choice == '2':
        with open(count_file, 'w') as f:
            f.write('1')  # Reset count to 1
        print("Quiz reset.")
        return
    elif choice == '3':
        goto_question = int(input("Enter the question number: ").strip())
        if goto_question < 1 or goto_question > len(read_quiz(file_path)):
            print("Invalid question number.")
            return
        else:
            with open(count_file, 'w') as f:
                f.write(str(goto_question))  # Set count to the chosen question number
    else:
        print("Invalid option.")
        return

    quiz = read_quiz(file_path)
    
    while True:
        try:
            with open(count_file, 'r') as f:
                count_str = f.read().strip()
                if count_str:
                    count = int(count_str)
                else:
                    count = 1  # Start count at 1 for a new quiz or after reset
        except FileNotFoundError:
            count = 1

        if count > len(quiz):
            print("You have completed the quiz.")
            break

        print(f"\nQuestion {count} / {len(quiz)}:")
        question_text, answers, correct_indices = quiz[count - 1]  # Adjusted index
        completed = ask_question(question_text, answers, correct_indices)
        
        if completed:
            with open(count_file, 'w') as f:
                f.write(str(count + 1))  # Increment count
            count += 1  # Increment count for next question

if __name__ == "__main__":
    main()
