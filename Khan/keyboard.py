from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton as Button
from db.texts import *
from db.config import bot_channel_public, bot_username
from db.Mongo import r


def pv_keyboard():
    keyboardـstart = InlineKeyboardMarkup(
        [
            [
                Button(pv_AddToGroup_button, url=f'http://t.me/{bot_username}?startgroup=new') 
            ], # row 1
            [
                Button(pv_MyChannel_Button, url=f'https://t.me/{bot_channel_public}'), Button(pv_Help_Button, callback_data='pv_Help_Button')
            ], # row 2
            [
                Button(pv_About_Button, callback_data='pv_About_Button')
            ] # row 3
        ]
    )
    return keyboardـstart

def back_main_pv():
    keyboard = InlineKeyboardMarkup(
        [
            [
                Button(back_button, callback_data='back_button_pv')
            ]
        ]
    )
    return keyboard

def group_panel(chatID:int):
    status_on, status_off = 'روشن','خاموش'
    if r.get(f'{chatID}:status') == 'True':
        status_on += '✅' 
    else:
        status_off += '✅'
    keyboard_group = InlineKeyboardMarkup(
        [
            [
                Button(group_button_commands, callback_data='group_button_commands')
            ],
            [
                Button(status_on , callback_data='status_on'), Button(group_button_status_main, callback_data='group_button_status_main'), Button(status_off, callback_data='status_off')
            ],
            [
                Button(group_button_channel, url=f'https://t.me/{bot_channel_public}'), Button(group_button_help, callback_data='group_button_help')
            ],
            [
                Button(group_button_close, callback_data='group_button_close')
            ]
            
        ]
    )
    return keyboard_group

def list_commands_page():
    keyboard_group = InlineKeyboardMarkup(
        [
            [
                Button(clear_commands_button, callback_data='clear_commands_button')
            ],
            [
                Button(back_button, callback_data='back_button_main')
            ]
        ]
    )
    return keyboard_group

def clear_all_keys_page():
    keyboard_group = InlineKeyboardMarkup(
        [
            [
                Button(yes_clear_button, callback_data='yes_clear_button')
            ],
            [
                Button(back_button, callback_data='back_button_main')
            ]
        ]
    )
    return keyboard_group

def stats_keyboard(fun_txt:str):
    vote = InlineKeyboardMarkup([
        [
            Button(fun_txt, callback_data='statsfun')
        ]
    ])
    return vote

def group_help():
    keyboard_group = InlineKeyboardMarkup(
        [
            [
                Button(group_help_button_learn_text, callback_data='group_help_button_learn_text'), Button(group_help_button_learn_voice, callback_data='group_help_button_learn_voice')
            ],
            [
                Button(group_help_button_echo_text, callback_data='group_help_button_echo_text'), Button(group_help_button_fun, callback_data='group_help_button_fun')
            ],
            [
                Button(group_help_button_text_delete, callback_data='group_help_button_text_delete'), Button(group_help_button_text_delete_all, callback_data='group_help_button_text_delete_all')
            ],
            [
                Button(group_help_button_list_commands, callback_data='group_help_button_list_commands'), Button(group_help_button_status, 'group_help_button_status')
            ],
            [
                Button(back_button, callback_data='back_button_main')
            ]
        ]
    )
    return keyboard_group

def back_help_group():
    keyboard = InlineKeyboardMarkup(
        [
            [
                Button(back_button, callback_data='back_button_help')
            ]
        ]
    )
    return keyboard

def sponser_button():
    keyboard = InlineKeyboardMarkup(
        [
            [
                Button(channel_sponser_text, url=f'https://t.me/{bot_channel_public}')
            ]
        ]
    )
    return keyboard