from groq import Groq
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import os
import requests
from random import choice
from bs4 import BeautifulSoup
from pyfiglet import Figlet

#GROK API_KEY
load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")
NAME=os.getenv("NAME")
LEVEL=os.getenv("LEVEL")
FOCUS_AREA=os.getenv("FOCUS_AREA")
FOLDER="notes"
MAX_WORDS=3000
console=Console()


#reusable figlet
def reusable_figlet(to_display:str):
    print(Figlet(font='slant').renderText(to_display))

#check api and client groq client
def groq_client():
    if API_KEY is None:
        print("\n")
        panel=Panel.fit(f"[yellow] To use MTABE CLI AI tool you need to add groq api key just vist at [italic blue] https://console.groq.com/keys [/italic blue] To get you api key and past it below!, [italic green]Note: ITS FREE Mtabe usiogope kama Marioo😁[/italic green],  Thank your![/yellow]",title="ADD GROK API KEY ONCE", border_style='yellow')
        console.print(panel)
        api_key=Prompt.ask("[green]Past Groq API_KEY here[/green]")
        if len(api_key) <56:
            panel=Panel.fit("[red]Ijust vist at [italic yellow] https://console.groq.com/keys [/italic yellow] To get you api key and passed it here!,[italic green] Note: ITS FREE Mtabe usiogope kama Marioo😁[/red]",title="INVALID KEY", border_style="bold red")
            console.print(panel)
            quit()
        try:
            with open(".env","+a", encoding='utf-8') as f:
                f.write("\nGROQ_API_KEY="+api_key+"\n")
                panel=Panel.fit(f"Groq api key added! enjoy your learning [green]Mtabe kipange 😁🔥[/green] ",title="Successful!",border_style='green')
                console.print(panel)
                #return client here!
                return Groq(api_key=api_key)
        except:
            panel=Panel.fit("[red]Try again [green]Mtabe wetu[/green] Just vist at [italic yellow] https://console.groq.com/keys [/italic yellow] To get you api key and past it below!,[italic green] Note: ITS FREE Mtabe usiogope kama Marioo😁[/red]",title="Error when adding key", border_style="red")
            console.print(panel)
            quit()
    else:
        #return client here! if key is there
        return Groq(api_key=os.getenv("GROQ_API_KEY"))
    

#slipt to get maxwords to return:
def slipt_max_words(notes_loaded:str)-> str:
    notes_words=notes_loaded.split()
    if len(notes_words)<=MAX_WORDS:
        return notes_loaded
    if choice([True,False]):
        selected_words=notes_words[:MAX_WORDS]
        print("TOP-TOTAL WORD PASSED TO LLM : ",len(selected_words))
    else:
        selected_words=notes_words[-MAX_WORDS:]
        print("BOTTOM-TOTAL WORD PASSED TO LLM: ",len(selected_words))
    return " ".join(selected_words)


#load student notes
def get_notes(filename:str)->str:
    print(f"filename: {filename}")
    filepath=os.path.join(FOLDER,f'{filename}.txt')
    print(f"filepath: {filepath}")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding='utf-8') as f:
            notes_loaded=f.read()
        #max sure notes to return is not greater than MAX_WORDS
        return slipt_max_words(notes_loaded)
    else:
        reusable_panel_console(text=f"Missing filepath [magenta]{filepath}[/magenta] error\nBot need reference notes\nType Mutabe [BOTNAME] --help to see other options, Thank you!",border_style='red',text_style='red', title='Oops❌')
        quit()


#Display in Table
def display_table(columns:list,title:str,row_data:list):
    table=Table(title=title)

    # static column
    table.add_column("IDX", style="cyan", justify="start")
    for column in columns:
        table.add_column(column)

    for idx,data in enumerate(row_data):
        table.add_row(f"{idx+1}",*[str(value) for value in data])
    console.print(table)


#configuration commant:
    # - student information
        # - name, level, Language, area of focus (IT, CS, science)
#configuration command
def get_user_info()->list:
    if NAME is None or LEVEL is None or FOCUS_AREA is None:
        panel=Panel.fit("Help Bots to know you, for better results")
        console.print(panel)
        vibe_name=Prompt.ask("[green]Enter vibe name(eg. Henry)[/green]")
        vibe_level=Prompt.ask("[green]Your vibe level (eg. college student)[/green]")
        focus=Prompt.ask("[green]Your Area of focus(eg. IT)[/green]")
        try:
            with open(".env","+a",encoding="utf-8") as file:
                file.write(f"\nNAME={vibe_name}\nLEVEL={vibe_level}\nFOCUS_AREA={focus}")
            return [vibe_name,vibe_level,focus]
        except:
            panel=Panel.fit("[red] Error when writing your info to .env file")
            console.print(panel)
            quit()
    else:
        return [NAME,LEVEL,FOCUS_AREA]



#reusable panel
def reusable_panel_console(text:str,border_style:str,title:str,text_style:str="white"):
    panel=Panel.fit(f"[{text_style}]{text}[/{text_style}]",border_style=border_style,title=title)
    console.print(panel)

#saving the notes func
def save_notes(notes:str, notes_name:str)->tuple:
    try:
        #create FOLDER if not available
        os.makedirs(FOLDER,exist_ok=True)
        file_path=os.path.join(FOLDER,f'{notes_name}.txt')
        with open(file_path,"w", encoding='utf-8') as f:
            w_num=f.write(notes)      
        return True,w_num
    except:
        return False,0

#requirest
def response(url:str):
    try:
        response=requests.get(url)
        response.raise_for_status
        return response
    except requests.exceptions.RequestException as e:
        panel=Panel.fit(f"[red]Error geting: {e}, Program quit due to some requests error, Double check url [italic blue]{url}[/italic blue]!, Thank your![/red]",title="Requirest Error!", border_style='red')
        console.print(panel)
        return None
        
#getting the notes from the web and saving it
def get_web_notes(url:str)->str:
    if url=='NOT-FOUND':
        # PRINT
        reusable_panel_console('Provide notes form the internet (web), copy and past or type url below!', border_style='yellow', title='Past/Type notes',text_style='bright_cyan')
        url=Prompt.ask("[italic yellow]Past/Type here![/italic yellow]")
    res=response(url)
    if res is None:
        quit()
    soup=BeautifulSoup(res.content,"html.parser")
    content_text=soup.get_text().replace("\n"," ").replace("\r"," ")
    return content_text



# past/type notes and saving it
def get_past_notes(notes:str)-> str:
    if notes=="NOT-FOUND":
        #print
        reusable_panel_console('Provide notes for the bot, copy and past or type it below!', border_style='yellow', title='Past/Type notes',text_style='bright_cyan')
        notes=Prompt.ask("[italic yellow]Past/Type here![/italic yellow]")
    if len(notes)<10:
        panel=Panel.fit(f"[red]Please provide more that 99 charaters, Program quit due to some small notes provided, reRun and provide much notes, Thank your![/red]",title="Note adding error!", border_style='red')
        console.print(panel)
        quit()
    return notes


