import click
import os
from rich.panel import Panel
from rich.console import Console
from bots import flash_card_bot
from config import save_notes,get_past_notes,get_web_notes,reusable_panel_console,slipt_max_words
from reader import read_file

#group group
@click.group
def mycommands():
    pass

#console obj
console=Console()

# add notes command
@click.command()
@click.argument('filename',type=click.Path(exists=False))
@click.argument('source',type=click.Choice(['type','web','youtube','local']))
@click.option("-u","--url", help="Website url or youtube url where you need get notes from")
@click.option("-n","--notes", help="Type or paste notes ")
def add_notes(filename,source,url:str='NOT-FOUND',notes: str='NOT-FOUND'):
    match source:
        case "type":
            notes_pasted=get_past_notes(notes)
            isSaved,words_num=save_notes(notes=notes_pasted,notes_name=filename)
            if isSaved:
                #print congrate
                reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
            else:
                #print errors
                reusable_panel_console(text=f"Adding notes typed/pased process failed,\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')


        case "web":
            notes_from_web=get_web_notes(url=url)
            isSaved,words_num=save_notes(notes=notes_from_web,notes_name=filename)
            if isSaved:
                #print congrate
                reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nFrom [italic blue]{url}[/italic blue]\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
            else:
                #print errors
                reusable_panel_console(text=f"Failed to add notes\nFrom [italic blue]{url}[/italic blue],\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')
        case "youtube":
            pass
        case "local":
            pass
        case _:
            reusable_panel_console(text=f"❌ Only type, web, youtube or local is allowed as source, Try again",border_style='red',text_style='red', title='Oops')

#flash_card
@click.command()
@click.option('-f', "--filename", help='To use this option you should alread add notes using add-notes command, if alread just type -n "filename"')
@click.option("-y","--youtube", help="youtube video url where you need get content from")
@click.option("-w","--web", help="Website url where you need get content from")
@click.option("-l","--local", help="Local filepath where you need get content from")
def flash_card(filename: str,youtube: str,web: str,local: str):
    options=[filename,youtube,web,local]
    provided=[opt for opt in options if opt is not None]
    if len(provided)!=1:
        raise click.UsageError("You must provide exactly one of the options: --filename/-f, --youtube/-y, --web/-w, or --local/-l")
    if filename:
        flash_card_bot(filename,notes="FALSE")
    elif web:
        notes_from_web=get_web_notes(web)
        console.clear()
        selected_notes=slipt_max_words(notes_loaded=notes_from_web)
        reusable_panel_console(text=f"Content loaded Successful!\nFrom [italic blue]{web}[/italic blue]\nLoaded words: {len(selected_notes)},\nNow you can type your instruction for a bot to create your flash-card",border_style='green',title="Successful!✅",text_style='green')
        flash_card_bot(filename="FALSE",notes=selected_notes)
    elif youtube:
        pass
    elif local:
        notes_from_local_file=read_file(local)
        console.clear()
        selected_notes=slipt_max_words(notes_loaded=notes_from_local_file)
        reusable_panel_console(text=f"File loaded Successful!\nFrom [italic blue]{local}[/italic blue]\nLoaded words: {len(selected_notes)},\nNow you can type your instruction for a bot to create your flash-card",border_style='green',title="Successful!✅",text_style='green')
        flash_card_bot(filename="FALSE",notes=selected_notes)



#adding command
mycommands.add_command(add_notes)
mycommands.add_command(flash_card)
# mycommands.add_command(set_brain_n)


if __name__ =="__main__":
    mycommands()