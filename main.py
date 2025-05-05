import click
import os
from rich.panel import Panel
from rich.console import Console
from bots import flash_card_bot,test_gen_bot
from config import save_notes,get_past_notes,get_web_notes,reusable_panel_console,slipt_max_words
from reader import read_file
from youtube_sbt import get_youtube_subtitles

#group group
@click.group
def mycommands():
    pass

#console obj
console=Console()

# add notes command
@click.command()
@click.argument('filename',type=click.Path(exists=False))
@click.option('-t', "--type", help='Type or paste notes')
@click.option("-y","--youtube", help="youtube video url where you need get notes from")
@click.option("-w","--web", help="Website url where you need get notes from")
@click.option("-l","--local", help="Local filepath where you need get notes from")
def add_notes(filename,youtube,web,local:str='NOT-FOUND',type: str='NOT-FOUND'):
    options=[type,youtube,web,local]
    provided=[opt for opt in options if opt is not None]
    if len(provided)!=1:
        raise click.UsageError("You must provide exactly one of the options: --filename/-f, --youtube/-y, --web/-w, or --local/-l")
    
    if type:
        notes_pasted=get_past_notes(type)
        isSaved,words_num=save_notes(notes=notes_pasted,notes_name=filename)
        if isSaved:
            #print congrate
            reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
        else:
            #print errors
            reusable_panel_console(text=f"Adding notes typed/pased process failed,\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')
    elif web:
        notes_from_web=get_web_notes(url=web)
        isSaved,words_num=save_notes(notes=notes_from_web,notes_name=filename)
        if isSaved:
            #print congrate
            reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nFrom [italic blue]{web}[/italic blue]\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
        else:
            #print errors
            reusable_panel_console(text=f"Failed to add notes\nFrom [italic blue]{web}[/italic blue],\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')
    elif youtube:
        notes_from_youtube=get_youtube_subtitles(url=youtube)
        isSaved,words_num=save_notes(notes=notes_from_youtube,notes_name=filename)
        if isSaved:
            #print congrate
            reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nFrom [italic blue]{youtube}[/italic blue]\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
        else:
            #print errors
            reusable_panel_console(text=f"Failed to add notes\nFrom [italic blue]{youtube}[/italic blue],\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')
    elif local:
        notes_from_youtube=read_file(filepath_in=local)
        isSaved,words_num=save_notes(notes=notes_from_youtube,notes_name=filename)
        if isSaved:
            #print congrate
            reusable_panel_console(text=f"Congrate Notes [magenta]({filename})[/magenta] added Successful!\nFrom [italic blue]{local}[/italic blue]\nAdded words: {words_num},\nNow you can refer this notes to bots using filename any time",border_style='green',title="Successful!✅",text_style='green')
        else:
            #print errors
            reusable_panel_console(text=f"Failed to add notes\nFrom [italic blue]{local}[/italic blue],\nTry again, or use another method to add notes-file",border_style='red',text_style='red', title='Oops❌')


def call_bot_and_get_content(filename: str,youtube: str,web: str,local: str, bot_name:str, bot_func):
    options=[filename,youtube,web,local]
    provided=[opt for opt in options if opt is not None]
    if len(provided)!=1:
        raise click.UsageError("You must provide exactly one of the options: --filename/-f, --youtube/-y, --web/-w, or --local/-l")
    if filename:
        bot_func(filename,notes="FALSE")
    elif web:
        notes_from_web=get_web_notes(web)
        console.clear()
        selected_notes=slipt_max_words(notes_loaded=notes_from_web)
        reusable_panel_console(text=f"Content loaded Successful!\nFrom [italic blue]{web}[/italic blue]\nLoaded words: {len(selected_notes)},\nNow you can type your instruction for a bot to create your {bot_name}",border_style='green',title="Successful!✅",text_style='green')
        bot_func(filename="FALSE",notes=selected_notes)
    elif youtube:
        notes_from_youtube=get_youtube_subtitles(youtube)
        console.clear()
        selected_notes=slipt_max_words(notes_loaded=notes_from_youtube)
        reusable_panel_console(text=f"Subtitle loaded Successful!\nFrom [italic blue]{youtube}[/italic blue]\nLoaded words: {len(selected_notes)},\nNow you can type your instruction for a bot to create your {bot_name}",border_style='green',title="Successful!✅",text_style='green')
        bot_func(filename="FALSE",notes=selected_notes)
    elif local:
        notes_from_local_file=read_file(local)
        console.clear()
        selected_notes=slipt_max_words(notes_loaded=notes_from_local_file)
        reusable_panel_console(text=f"File loaded Successful!\nFrom [italic blue]{local}[/italic blue]\nLoaded words: {len(selected_notes)},\nNow you can type your instruction for a bot to create your {bot_name}",border_style='green',title="Successful!✅",text_style='green')
        bot_func(filename="FALSE",notes=selected_notes)




#flash_card
@click.command()
@click.option('-f', "--filename", help='To use this option you should alread add notes using add-notes command, if alread just type -n "filename"')
@click.option("-y","--youtube", help="youtube video url where you need get content from")
@click.option("-w","--web", help="Website url where you need get content from")
@click.option("-l","--local", help="Local filepath where you need get content from")
def flash_card(filename: str,youtube: str,web: str,local: str):
    call_bot_and_get_content(filename,youtube,web,local,bot_name="flash_card",bot_func=flash_card_bot)



@click.command()
@click.option('-f', "--filename", help='To use this option you should alread add notes using add-notes command, if alread just type -n "filename"')
@click.option("-y","--youtube", help="youtube video url where you need get content from")
@click.option("-w","--web", help="Website url where you need get content from")
@click.option("-l","--local", help="Local filepath where you need get content from")
def test(filename: str,youtube: str,web: str,local: str):
    call_bot_and_get_content(filename,youtube,web,local,bot_name="test",bot_func=test_gen_bot)


#adding command
mycommands.add_command(add_notes)
mycommands.add_command(flash_card)
mycommands.add_command(test)


if __name__ =="__main__":
    mycommands()