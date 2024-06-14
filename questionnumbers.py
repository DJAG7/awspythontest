def add_question_numbers(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    questions = data.split("<<questionnext>>")
    
    # Add "questionnext" between questions
    updated_data = "questionnext".join(questions)

    with open(file_path, 'w') as file:
        file.write(updated_data)

file_path = r'C:\Users\danie\Documents\AWS Test\AWS Python Test\quiz.txt'  
add_question_numbers(file_path)
