from mtabe.config.config import groq_client,get_notes,display_table,reusable_figlet,reusable_panel_console,get_user_info
from rich.prompt import Prompt
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
import ast

from random import choice
console=Console()

student_info=get_user_info()
# print(student_info)
quotes = [
    ["The secret of getting ahead is getting started.", "Mark Twain"],
    ["Success is not final, failure is not fatal: It is the courage to continue that counts.", "Winston Churchill"],
    ["Don’t watch the clock; do what it does. Keep going.", "Sam Levenson"],
    ["Believe you can and you're halfway there.", "Theodore Roosevelt"],
    ["Start where you are. Use what you have. Do what you can.", "Arthur Ashe"],
    ["It does not matter how slowly you go as long as you do not stop.", "Confucius"],
    ["The best way to predict the future is to create it.", "Peter Drucker"],
    ["Push yourself, because no one else is going to do it for you.", "Unknown"],
    ["You don’t have to be great to start, but you have to start to be great.", "Zig Ziglar"],
    ["Your limitation—it’s only your imagination.", "Unknown"],
    ["Learning never exhausts the mind.", "Leonardo da Vinci"],
    ["Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"],
    ["There are no shortcuts to any place worth going.", "Beverly Sills"],
    ["Study while others are sleeping; work while others are loafing; prepare while others are playing; and dream while others are wishing.", "William Arthur Ward"],
    ["The expert in anything was once a beginner.", "Helen Hayes"],
    ["Education is the most powerful weapon which you can use to change the world.", "Nelson Mandela"],
    ["I am not a product of my circumstances. I am a product of my decisions.", "Stephen R. Covey"],
    ["Success is the sum of small efforts, repeated day in and day out.", "Robert Collier"],
    ["Don’t let what you cannot do interfere with what you can do.", "John Wooden"],
    ["Hard work beats talent when talent doesn't work hard.", "Tim Notke"]
]

def call_llm(SYSTEM_PROMPT: str,bot_name:str):
    #Groq client
    client=groq_client()
    #Taking instruction Loop
    countq=0
    while True:
        countq+=1
        instruction=Prompt.ask("\n[italic yellow]Your Instruction (q to quit)[/italic yellow]")
        if instruction.lower() =='q':
            console.clear()
            reusable_figlet("- Bye -")
            console.print("[italic green]Goodbye....[/italic green]")
            break
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": f"{SYSTEM_PROMPT}"
                },
                {
                    "role": "user",
                    "content": f"Student Instruction: {instruction}"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        #playing with chucks
        content=""
        for chuck in completion:
            part=chuck.choices[0].delta.content or ""
            content+=part

        if bot_name=='flash_card':
            display_card(content=content)
        elif bot_name=="test":
            display_test(content)



#flash card bot 
def flash_card_bot(filename: str,notes:str):

    #check where the notes is from
    notes_passed=""
    if filename=="FALSE":
        notes_passed=notes
    else:
        notes_passed=get_notes(filename)
    
    #Title
    print("\n")
    reusable_figlet(" FLASH CARD ")

    
    SYSTEM_PROMPT=f"""
        You are an expert flashcard generator designed to help students study using terminal-friendly flashcards. You are given:

        - Notes on a topic.
        - Student profile: name, level, preferred language (e.g., English), and area of focus (e.g., IT, CS, Science, Art, etc.).
        - Student Instruction: number of flashcards to generate.

        Your task is to return flashcards that:
        1. Are based on the notes provided.
        2. Match the student’s level and focus area.
        3. Use the student’s preferred language.
        4. Include a mix of text-based questions and **ASCII or emoji-based simple visual illustrations** that help explain or represent concepts.
        5. fun emojis should be related to question, people, cart, computer, mouse, fun emojis to help in remembering
        6. Return a list of Python dictionaries in the following format:
        [
        opening curl bracket
        
            "question": "question here",
            "answer": "Clear and concise answer based on the notes",
            "emoji":"😁"
        closing curl bracket here
        ...
        ]

        If the number of flashcards is not specified, return a maximum of five. Questions must be diverse and vary in format. Prefer simplicity and clarity.
        Return only the Python dictionary list. No pretext or post-text.
        Do not add any pretext or post-text.

        ____________________PROVIDED DETAILS___________________________
        NOTES: {notes_passed}
        STUDENT PROFILE: {student_info[0]}, {student_info[1]}, {student_info[2]}
        """
    
    # instruction panel
    print('\n')
    console.print(Panel.fit("1. Give 10 card, \n2. Just 3,\n3.I need very hard 4 questions, etc", title="Example of Instruction.🥰",border_style='yellow'))

    #llm
    call_llm(SYSTEM_PROMPT,bot_name="flash_card")
    

# Displaying question, answer and qoutes for now!
def display_card(content:str,in_table:bool=False,is_saved:bool=False):
    card_list=[]
    card_list=ast.literal_eval(content)
    table_row_data=[]
    #[question,answer]
    count=0
    total_card=len(card_list)
    while count<total_card:
        console.clear()
        card=card_list[count]
        table_row_data.append([card['question'],card['answer']])
        count+=1
        console.print(f"[italic]{count}/{total_card}[italic]")
        panel=Panel.fit(f"{card['question']}", border_style='blue', title=f"{card["emoji"]}")
        console.print(panel)

        # show answer
        Prompt.ask("[italic green]Press Enter to show answer[/italic green]")
        console.clear()
        panel=Panel.fit(f"[yellow]{card['question']}[/yellow]\n- {card['answer']}",border_style='green', title=f"Answer🔥")
        console.print(panel)

        #wait user to continue
        Prompt.ask("[italic green]Press Enter to continue[/italic green]")

        #if end of the flash card
        if count==total_card:
            quote=choice(quotes)
            console.clear()
            console.print("[bright_green] Oooh, You've reached the end of your flashcards. [/bright_green]\n")
            console.print(Panel.fit(f"[bright_blue]{quote[0]}[/bright_blue]\n[magenta]By - {quote[1]}[/magenta]",title="Congrate!🥳",border_style='bright_blue'))

            #table calling
            display_table(["Question","Answer"],title="All Question(s)",row_data=table_row_data)

            # check if user need to continue or quit
            user_input=Prompt.ask("[italic green]Press Enter to continue or (q to quit)[/italic green]")
            if user_input.lower()=='q':
                console.clear()
                reusable_figlet("- Bye -")
                console.print("[italic green]Goodbye....[/italic green]")
                quit()


def display_test(content: str):
    test_list=[]
    test_list=ast.literal_eval(content)

    #[question]  
    questions_list=[]
    for question in test_list:
        if question.get('options'):
            questions_list.append([f"{question['question']}\n{"\n".join(question['options'])}\n"])
        else:
            questions_list.append([f"{question['question']}\n"])

    #display in  table
    console.clear()
    print("\n")
    console.rule("[bold blue] Start of Test sheat📰[/bold blue]")
    # reusable_figlet(" Test sheat")
    reusable_panel_console(
        text=f"""
        1. Read all questions carefully before answering.\n
        2. Answer all {len(questions_list)} questions below unless stated otherwise.\n
        3. The purpose of this test is to measure your understanding — not to win. [bold red]DO NOT CHEAT.[/bold red]""",border_style="yellow",title="TEST INSTRUCTIONS",text_style="yellow")
    print("\n")
    display_table(["Questions"], f"Questions {len(questions_list)}",row_data=questions_list)
    console.rule("[bold blue] End of Test sheat[/bold blue]")

    student_answers_and_bot_qa=[]
    {
        "question":"",
        "answer":"",
        "student_answer":""
    }
    #Taking user test answer
    for idx,question in enumerate(test_list):
        answer=Prompt.ask(f"[italic green]Answer for qn {idx+1}[/italic green]")
        qn_dict={
            'question':question['question'],
            'answer':question['answer'],
            'student_answer':answer
        }
        if question.get('options'):
            qn_dict['options']=question['options']
        student_answers_and_bot_qa.append(qn_dict)

    # print(student_answers_and_bot_qa)
    mark_text(student_answers_and_bot_qa)


#mark the exam func
{
    "scores":["7/10","3/5",...],
    "test_score":"40/100"
}
def mark_text(sheat_qa: dict):
    SYSTEM_PROMPT=f"""
        > You are a Marking Teacher Bot. You will receive a dictionary with the following keys:
        > opening curl bracket
        >   "question": "",         # The full question, including any indication of total marks
        >   "answer": "",           # The correct or model answer
        >   "student_answer": ""    # The student's submitted answer
        > closing curl bracket
        > Your job is to:
        > 1. Analyze the question to determine the **total possible score** (e.g., from "Qn 1. (10 marks)", infer 10).
        > 2. Compare the student’s answer to the correct answer.
        > 3. Assign a fair score based on **how well the student answered relative to the model answer**, using the total marks available for that question.
        > 4. Repeat for every question.
        > 5. Return the result as a Python dictionary with:
        opening curl bracket
        "score_questions": ["7/10🟨", "3/5🟨", "10/10✅","0/5❌"],  # Individual scores per question
        "test_score": "40/100"       # Total score out of number of question
        closing curl bracket
        
        > **Rules:**
        > * Do not add any explanations or extra text. means no pretext or post text
        > * student’s final score should be out of number of question.
        > * If total marks cannot be found in a question, assume 10 marks.
        > * Make fair, consistent judgments based on content accuracy, clarity, and relevance.
        Quetion, answer & student answer: {sheat_qa}
        STUDENT PROFILE: {student_info[0]}, {student_info[1]}, {student_info[2]}
    """
    client=groq_client()
    completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": f"{SYSTEM_PROMPT}"
            },
            # {
            #     "role": "user",
            #     "content": f"Student Instruction: {instruction}"
            # }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    #playing with chucks
    content=""
    for chuck in completion:
        part=chuck.choices[0].delta.content or ""
        content+=part
    # print("called________")
    # print(content)

    answer_dict=ast.literal_eval(content)

    # question | answer | your answer | score

    table_raw_data=[]
    for idx,qa in enumerate(sheat_qa):
        table_raw_data.append([qa['question'],qa["answer"], qa["student_answer"],answer_dict['score_questions'][idx]])
    # print(table_raw_data)
    display_table(columns=["Question","Answer","Your Answer","Score"],title="Marking-Scheam",row_data=table_raw_data)
    reusable_panel_console(text=f"Total Score: {answer_dict["test_score"]}",border_style="green",title="YOUR SCORE")




#Test generator bot
def test_gen_bot(filename:str,notes: str):
    notes_passed=""
    if filename=="FALSE":
        notes_passed=notes
    else:
        notes_passed=get_notes(filename)

    #Title
    print("\n")
    reusable_figlet("- TEST -")

    #Prompt
    SYSTEM_PROMPT=f"""
        You are a smart, helpful teacher. Your role is to create a test based on provided lecture notes and the student's profile.
        You will always receive:

            NOTES, STUDENT PROFILE
            The student may request a specific type of test or ask you to mix types like:
            ["multiple choice", "true/false", "essay", "fill the blank", "mix", "short explanation", "short answer"].

        Your task:
            1. Analyze the notes and student profile to make questions appropriate for their level.
            2. Follow the user (student)'s instruction to decide the number and type of questions.
            3. Mix questions if instructed or generate a default of 5 mixed questions/one time if not specified.
            4. Provide your response as a Python list of dictionaries, each formatted like this:
        [
        opening curl bracket
        "question": "What is the capital of France?",
        "answer": "Paris",
        "options":[]
        "question":"Which platform offers over 900 free certificate courses for learning software development?,
        "answer":"A. Class Central"
        options:[ A. Class Central\n B. freeCodeCamp\n C.Coursera\nD. edX"]
        closing curl bracket
        ]
        
        - Do not include any explanations, pre-text, or post-text. Only return the Python data.
        - Keep questions clear, accurate, and educational.
        -If a question is open-ended, provide a sample good answer.

            ____________________PROVIDED DETAILS___________________________
                NOTES: {notes_passed}
                STUDENT PROFILE: {student_info[0]}, {student_info[1]}, {student_info[2]}
        """

    #Instruction example
    print('\n')
    console.print(Panel.fit("1. I need ten multiple choice, \n2. fill the blank questions ,\n3.Just 5 short explanation qn\n4. True and false 5 question \n5.Two essay qn\n6. short answer question, etc", title="Example of Instruction.🥰",border_style='yellow'))

    #llm
    call_llm(SYSTEM_PROMPT,bot_name="test")

def chat_bot(filename:str,notes: str):
    notes_passed=""
    if filename=="FALSE":
        notes_passed=notes
    else:
        notes_passed=get_notes(filename)

    #Title
    print("\n")
    reusable_figlet("- CHAT -")

# - Do not copy-paste full content from the notes. Instead, help the student understand by rephrasing, asking follow-up questions, giving short examples, and checking their understanding.

    SYSTEM_PROMPT = f"""
        You are a helpful, smart, and motivational chatbot designed to assist students with their learning.

        You receive:
        - Class notes (your only knowledge base),
        - A student profile: name, level (e.g., diploma, degree), and focus area (e.g., AI, marketing).

        Your job is to:

        - Use only the provided notes to answer questions. Do not add any outside information unless the student asks for it.
        - Answer directly and briefly unless the student asks you to explain more.
        - Refer to the student by their name often in the conversation.
        - Offer short, focused study tips and test/exam-winning suggestions based on their focus area.
        - Occasionally mention well-known people in their focus area only if the student asks for inspiration or additional resources.
        - Always encourage critical thinking, curiosity, and active learning. Your goal is not to give answers but to help the student learn.

        ____________________PROVIDED DETAILS___________________________
        NOTES: {notes_passed}
        STUDENT PROFILE: Name: {student_info[0]}, Level: {student_info[1]}, Focus Area: {student_info[2]}
    """

    client=groq_client()

    while True:
        question=Prompt.ask("[yellow italic]Ask anything (q to quit)[/yellow italic]")
        if question.lower()=="q":
            console.clear()
            reusable_figlet("- Bye -")
            console.print("[italic green]Goodbye....[/italic green]")
            break

        completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": f"{SYSTEM_PROMPT}"
                },
                {
                    "role": "user",
                    "content": f"Student Instruction: {question}"
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        #playing with chucks
        # content=""
        # for chuck in completion:
        #     part=chuck.choices[0].delta.content or ""
        #     content+=part

        content=""
        with Live(Panel(content,title=question,border_style="bold yellow"),console=console, refresh_per_second=30) as live:
            for chuck in completion:
                part=chuck.choices[0].delta.content or ""
                content+=part
                live.update(Panel(content,title=question,border_style="bold yellow"))
        print("\n")
