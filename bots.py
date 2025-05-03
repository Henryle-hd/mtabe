from config import groq_client,get_notes,display_table,reusable_figlet
from rich.prompt import Prompt
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
import ast

from random import choice
console=Console()


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

    #Groq client
    client=groq_client()
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
        STUDENT PROFILE: 'HENRY DIONIZI', college student, English, IT
        """
    
    # instruction panel
    print('\n')
    console.print(Panel.fit("1. Give 10 card, \n2. Just 3,\n3.I need very hard 4 questions, etc", title="Example of Instruction.🥰",border_style='yellow'))

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
        # with Live(Panel(content,title=instruction,border_style="bold yellow"),console=console, refresh_per_second=30) as live:
        #     for chuck in completion:
        #         part=chuck.choices[0].delta.content or ""
        #         content+=part
        #         live.update(Panel(content,title=instruction,border_style="bold yellow"))
        display_card(content=content)

        

