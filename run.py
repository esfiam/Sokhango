import os
import subprocess
import click

list_bots = [
    'Khan'
]


def RunAll(bot:str):
    if bot in AllBots():
        original_dir = os.getcwd()
        KillAll(bot)
        os.chdir(bot)
        run = subprocess.run(['tmux', 'new-session', '-d', '-s', bot, 'python bot.py'])
        os.chdir(original_dir)
        return f'{bot} start'
    return f'{bot} not found'


def KillAll(bot:str):
    if bot in AllBots():
        kill = subprocess.run(['tmux', 'kill-session', '-t', bot])
        return f'{bot} is killed'
    return f'{bot} not found'


def AllBots():
    return list_bots



@click.command()
@click.argument('command')    
def main(command):
    if command == 'RunAll':
        for bot in AllBots():
            RunAll(bot)
            print(f'{bot} Run')      
    elif command == 'KillAll':
       for bot in AllBots():
            KillAll(bot)
            print(f'{bot} killed') 
    elif command == 'AllBots':
        for bot in AllBots():
            print(bot)
    else:
        print('your command is wrong\nselect command in list :\n1 - RunAll\n2 - KillAll\n3 - AllBots')
        

if __name__ == "__main__":
    main()