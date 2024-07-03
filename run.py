import os
import subprocess



def run_bot(bot:str):
    if bot in all_bots():
        kill_bot(bot)
        os.chdir(bot)
        run = subprocess.run(['tmux', 'new-session', '-d', '-s', bot, 'python bot.py'])
        return f'{bot} start'
    return f'{bot} not found'


def kill_bot(bot:str):
    if bot in all_bots():
        kill = subprocess.run(['tmux', 'kill-session', '-t', bot])
        return f'{bot} is killed'
    return f'{bot} not found'


def all_bots():
    dirs = os.listdir()
    dirs_bot = [dir for dir in dirs if os.path.isdir(dir)]
    bots = [bot for bot in dirs_bot if bot != 'venv']
    return bots


while True:
    text = '1 - kill all bots\n2 - run all bots\n3 - exit'
    all_choices = ['1', '2', '3']
    print(f'select :\n{text}')
    select = str(input('choice : ')).strip()
    if select in all_choices:
        if select == '1':
            all_session = all_bots()
            for bot in all_session:
                kill_bot(bot)
            os.system('clear')
            print('all bots killed\n')
            print('------------')
        elif select == '2':
            all_session = all_bots()
            for bot in all_session:
                kill_bot(bot)
                run_bot(bot)
            os.system('clear')
            print('all bots run\n')
            print('------------')
        else:           
            print('bye ):')
            break
    else:
        os.system('clear')
        print('please select choice in choices')
        print('------------')
            
    