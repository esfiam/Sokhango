from db.config import *
from db.texts import *
from db.Mongo import *
from keyboard import *
from hydrogram import Client, filters
from hydrogram.types import Message, CallbackQuery
from hydrogram.enums import ChatMemberStatus, ChatType
from hydrogram.errors import Forbidden, ChatAdminRequired, UserNotParticipant
from random import choice
import re

app = Client(name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=api_token)




# -------------- check status filter -----------------#
async def status(_, bot:Client, message:Message):
    return bool(r.get(f'{message.chat.id}:status') == 'True')
filterStatus = filters.create(status)


# ------------------ check admin user -------------------------#
async def admin(bot:Client, chatID:int, userID:int, not_anonymos):
    if not_anonymos:
        if userID == sudo:
            return True
        db_check = r.get(f"{chatID}:{userID}:admin")
        if db_check:
            return True if db_check == "True" else False
        else:
            check = await bot.get_chat_member(chatID, userID)
            if check.status is ChatMemberStatus.ADMINISTRATOR or check.status is ChatMemberStatus.OWNER:
                r.setex(f"{chatID}:{userID}:admin",20,"True")
                return True
            else:
                r.setex(f"{chatID}:{userID}:admin",20,"False")
                return False
    else:
        return False
            

async def check_join_sponser(bot:Client, message:Message):
    try:
        member = await bot.get_chat_member(bot_channel_public, message.from_user.id)
        if member:
            return True
    except ChatAdminRequired:
        return True
    except UserNotParticipant:
        return False
# -------------- antispam filter ---------------------#
async def antispam(_, bot:Client, message:Message):
    if message.from_user:
        db_check = r.get(f"{message.chat.id}:{message.from_user.id}:spam")
        return False if db_check else True
    else:
        return False
filterSpam = filters.create(antispam)

#--------------- new pv --------------#
@app.on_message(filters.private & filters.command('start'))
async def pv_bot(bot:Client, message:Message):
    new_user(message.from_user.id)
    if not await check_join_sponser(bot, message):
        await bot.send_message(message.from_user.id, please_join_sponser, reply_markup=sponser_button())
    else:
        await message.reply(pv_start_text, reply_markup=pv_keyboard())
    
# ------------ new group -------------#
@app.on_message(filters.service & filters.new_chat_members)
async def new_service(bot:Client, message:Message):
    if message.new_chat_members[0].id == bot_userid:
        await bot.send_message(message.chat.id, add_new_group_msg, reply_markup=sponser_button())
        await bot.send_message(sudo, f'#new\ngroup name :\n{message.chat.title}\nchat id:\n{message.chat.id}\ncount :\n{await bot.get_chat_members_count(message.chat.id)}')
        r.set(f'{message.chat.id}:status', 'True') # redis
        new_group(message.chat.id)

# ------------ delete group -------------#
@app.on_message(filters.service & filters.left_chat_member)
async def new_service(bot:Client, message:Message):
    if message.left_chat_member.id == bot_userid:
        await bot.send_message(sudo, f'#remove\ngroup name :\n{message.chat.title}\nchat id:\n{message.chat.id}')
        r.delete(f'{message.chat.id}:status') # redis
        del_group(message.chat.id)


# ------------ sudo -------------#
@app.on_message(filters.user(sudo) & filters.text )
async def sudo_commands(bot:Client, message:Message):
    if message.text == 'stats':
        gps = get_all_groups()
        pvs = get_all_users()
        await message.reply(f'users : {pvs["count_pvs"]}\ngroups : {gps["count_groups"]}\nkeys : {gps["count_keys"]}')
        
# ------------ Conversation ------------#
@app.on_message(filters.group & filters.text & filterSpam & filterStatus, group= 0)
async def conversation(bot:Client, message:Message):
    s = get_key(message.chat.id, message.text)
    if s:
        random_choice = choice(s)
        if random_choice.startswith('voice'):
            await bot.send_voice(message.chat.id, random_choice[len('voice'):].strip(), reply_to_message_id=message.id)
            r.setex(f"{message.chat.id}:{message.from_user.id}:spam", 5, "True") # set expire for antispam in redis
        else:    
            await message.reply(random_choice)
            r.setex(f"{message.chat.id}:{message.from_user.id}:spam", 5, "True") # set expire for antispam in redis
            


# ------------ all command in group -----------------#        
@app.on_message(filters.group & filters.text & filters.regex(f'^{bot_name_fa}'), group=1)
async def check_regex(bot:Client, message:Message):
    if await admin(bot, message.chat.id, message.from_user.id, message.from_user):
        if re.search(f'^{bot_name_fa}?.(خاموش|روشن)', message.text) :
            await stats_on_off(bot, message)
        elif re.search(f'^{bot_name_fa}?.(تنظیمات|پنل)', message.text):
            await panel_gp(bot, message)
        elif re.search(f'^{bot_name_fa}?.(آموزش|راهنما)', message.text):
            await help_panel(bot, message)
        elif re.search(f'^{bot_name_fa}?.(چیا?.بلدی|لیست?.دستورات)', message.text):
            await list_commands(bot, message)
        elif re.search(f'^{bot_name_fa}?.(حذف?.دستور|فراموش?.کن)', message.text):
            await del_command(bot, message)
        elif re.search(f'^{bot_name_fa}?.بگو', message.text) and not re.search('در?.جواب', message.text):
            await echo(bot, message)
        elif re.search(f'^{bot_name_fa}?.در?.جواب.*بگو', message.text):
            try:
                if message.reply_to_message:
                    if message.reply_to_message.text:
                        await learn_key_reply_text(bot, message)
                    elif message.reply_to_message.voice:
                        await learn_key_reply_voice(bot, message)
                    else:
                        await message.reply(just_text_supported_reply)
                else:
                    await learn_key(bot, message)
            except UnicodeDecodeError:
                await message.reply(unicode_error)
                
        elif re.search(f'^{bot_name_fa}?.به', message.text):
            await fun_stats(bot, message)
        elif re.search(f'^{bot_name_fa}?.(پاکسازی?.دستورات|پاکسازی?.کلمات|پاکسازی?.لیست?.کلمات)', message.text):
            await clear_all_keys(bot, message)
        


# ----------------- echo ------------------ #
async def echo(bot:Client, message:Message):
        regex_search = re.search(f'^{bot_name_fa}?.بگو',message.text)
        regex_span = regex_search.span()
        txt_echo = message.text[regex_span[1]:].strip()
        msg_id = message.reply_to_message.id if message.reply_to_message else None
        if len(txt_echo) > 0:
            try:
                await message.delete()
                await message.reply(txt_echo, reply_to_message_id=msg_id if msg_id else None)
            except Forbidden:
                await message.reply(group_required_admin) 
        else:
            await message.reply(group_echo_len_none)
        

# -------------- learning --------------- #
async def learn_key(bot:Client, message:Message):
        regex_key = re.search(f"{bot_name_fa}?.در?.جواب", message.text)
        regex_value = re.search("بگو", message.text)
        regex_key_span = regex_key.span()
        regex_value_span = regex_value.span()
        key = message.text[regex_key_span[1]:regex_value_span[0]].strip()
        if key != "" :
            value = message.text[regex_value_span[1]+1:].strip()
            if value != "":
                if new_key(message.chat.id, key, value) == 1:
                    await message.reply(f'خب من یاد گرفتم در جواب :\n{key}\nبگم :\n{value}')
                else:
                    await message.reply(already_existed_value)
            else:
                await message.reply(empty_key_error) 
        else:
            await message.reply(empty_key_error)  
            
async def help_panel(bot:Client, message:Message):
    await message.reply(help_text, reply_markup=group_help())

        
async def learn_key_reply_text(bot:Client, message:Message):
    regex_key = re.search(f"{bot_name_fa}?.در?.جواب", message.text)
    regex_value = re.search("بگو", message.text)
    regex_key_span = regex_key.span()
    regex_value_span = regex_value.span()
    key = message.text[regex_key_span[1]:regex_value_span[0]].strip()                
    if key != "" :
        value = message.reply_to_message.text.strip()
        if value != "":
            if new_key(message.chat.id, key, value) == 1:
                await message.reply(f'خب من یاد گرفتم در جواب :\n{key}\nبگم :\n{value}')
            else:
                await message.reply(already_existed_value)
        else:
            await message.reply(empty_key_error)
    else:
        await message.reply(empty_key_error)

async def learn_key_reply_voice(bot:Client, message:Message):
    regex_key = re.search(f"{bot_name_fa}?.در?.جواب", message.text)
    regex_value = re.search("بگو", message.text)
    regex_key_span = regex_key.span()
    regex_value_span = regex_value.span()
    key = message.text[regex_key_span[1]:regex_value_span[0]].strip()
    if key != "" :
        if new_key(message.chat.id, key, 'voice'+message.reply_to_message.voice.file_id) == 1:
            await message.reply(f'خب من یاد گرفتم در جواب :\n{key}\nاین ویس رو بگم !')
        else:
            await message.reply(already_existed_value)
    else:
        await message.reply(empty_key_error)
        
        
# ---------------- clear all commands ---------------------#
async def clear_all_keys(bot:Client, message:Message):
    await message.reply(await commands_db(message.chat.id), reply_markup=clear_all_keys_page())


# ----------------- fun stats ------------------------#
async def fun_stats(bot:Client, message:Message):
    regex_search = re.search(f"^{bot_name_fa}?.به", message.text)
    regex_span = regex_search.span()
    stats_txt = message.text[regex_span[1]:].strip()
    if stats_txt.endswith('م'):
        if len(stats_txt) > 2 and len(stats_txt) < 15:
            stats_txt = stats_txt[:-1] 
            stats_txt_msg = stats_txt + "شونه"
            stats_txt_button = stats_txt + "ته؟"
            await message.reply(f"لیست کسانی که این بیام به {stats_txt_msg}", reply_to_message_id=message.reply_to_message.id, reply_markup=stats_keyboard(stats_txt_button))
        else:
            await message.reply(len_stats_fun_error)
            

# ------------------- click button ---------------------- #
@app.on_callback_query()
async def click_button_group(bot:Client, CallBack:CallbackQuery):
    if CallBack.message.from_user:
        msg_txt = CallBack.message.text
        if CallBack.data == "statsfun":
            new_msg_button = CallBack.message.reply_markup.inline_keyboard[0][0].text
            if str(CallBack.from_user.id) in msg_txt:
                await CallBack.answer(f'شما از قبل این بیام به {new_msg_button[:-2]} بود!', show_alert=True)
            else:
                msg_txt = f"{msg_txt}\n[{CallBack.from_user.full_name}] - [{CallBack.from_user.id}]"
                await CallBack.edit_message_text(msg_txt + '\n', reply_markup=stats_keyboard(new_msg_button))
        else:
            if CallBack.message.chat.type != ChatType.PRIVATE:
                if await admin(bot, CallBack.message.chat.id, CallBack.from_user.id, CallBack.message.from_user):
                    if CallBack.from_user.id == CallBack.message.reply_to_message.from_user.id:
                        if CallBack.data == 'group_button_commands':
                            await CallBack.edit_message_text(await commands_db(CallBack.message.chat.id), reply_markup=list_commands_page())
                        elif CallBack.data == 'group_button_close':
                            await CallBack.edit_message_text(close_panel_text)
                        elif CallBack.data == 'back_button_main':
                            await CallBack.edit_message_text(panel_gp_text, reply_markup=group_panel(CallBack.message.chat.id))
                        elif CallBack.data == 'clear_commands_button':
                            if get_all_key(CallBack.message.chat.id):
                                await CallBack.edit_message_text(clear_all_commands_text, reply_markup=clear_all_keys_page())
                            else:
                                await CallBack.answer(commands_empty_error, show_alert=True)
                        elif CallBack.data == 'yes_clear_button':
                            if del_all_keys(CallBack.message.chat.id):
                                await CallBack.answer(clear_all_key_text)
                                await CallBack.edit_message_text(panel_gp_text, reply_markup=group_panel(CallBack.message.chat.id))
                            else:
                                await CallBack.answer(commands_empty_error, show_alert=True)
                        elif CallBack.data == 'status_on':
                            if r.get(f'{CallBack.message.chat.id}:status') == 'True':
                                await CallBack.answer(group_now_status_on, show_alert=True)
                            else:
                                r.set(f'{CallBack.message.chat.id}:status', 'True')
                                await CallBack.answer(status_on, show_alert=True)
                                await CallBack.edit_message_text(panel_gp_text, reply_markup=group_panel(CallBack.message.chat.id))
                        elif CallBack.data == 'status_off':
                            if r.get(f'{CallBack.message.chat.id}:status') != 'True':
                                await CallBack.answer(group_now_status_off, show_alert=True)
                            else:
                                r.set(f'{CallBack.message.chat.id}:status', 'False')
                                await CallBack.answer(status_off, show_alert=True)
                                await CallBack.edit_message_text(panel_gp_text, reply_markup=group_panel(CallBack.message.chat.id))
                        elif CallBack.data == 'group_button_help':
                            await CallBack.edit_message_text(help_text, reply_markup=group_help())
                            
                        # ---------- helps button in group -------#
                        elif CallBack.data == 'back_button_help':
                            await CallBack.edit_message_text(help_text, reply_markup=group_help())
        
                        elif CallBack.data == 'group_help_button_learn_text':
                            await CallBack.edit_message_text(group_help_learn_text, reply_markup=back_help_group())
                            
                        elif CallBack.data == 'group_help_button_learn_voice':
                            await CallBack.edit_message_text(group_help_learn_voice, reply_markup=back_help_group())
                            
                        elif CallBack.data == 'group_help_button_echo_text':
                            await CallBack.edit_message_text(group_help_echo_text, reply_markup=back_help_group())
                        
                        elif CallBack.data == 'group_help_button_fun':
                            await CallBack.edit_message_text(group_help_fun, reply_markup=back_help_group())
                            
                        elif CallBack.data == 'group_help_button_text_delete':
                            await CallBack.edit_message_text(group_help_text_delete, reply_markup=back_help_group())
                            
                        elif CallBack.data == 'group_help_button_text_delete_all':
                            await CallBack.edit_message_text(group_help_text_delete_all, reply_markup=back_help_group())
                        
                        elif CallBack.data == 'group_help_button_list_commands':
                            await CallBack.edit_message_text(group_help_list_commands, reply_markup=back_help_group())
                        
                        elif CallBack.data == 'group_help_button_status':
                            await CallBack.edit_message_text(group_help_status, reply_markup=back_help_group())
                             
                    else:
                        if not r.get(f"{CallBack.message.chat.id}:{CallBack.message.from_user.id}:spam"):
                            await CallBack.answer(just_user_requested, show_alert=True)            
                            r.setex(f"{CallBack.message.chat.id}:{CallBack.message.from_user.id}:spam", 5, "True") # set expire for antispam in redis
                        
                else:
                    if not r.get(f"{CallBack.message.chat.id}:{CallBack.message.from_user.id}:spam"):
                        await CallBack.answer(you_are_not_admin, show_alert=True)            
                        r.setex(f"{CallBack.message.chat.id}:{CallBack.message.from_user.id}:spam", 5, "True") # set expire for antispam in redis
            else:
                if CallBack.data == 'back_button_pv':
                    await CallBack.edit_message_text(pv_start_text, reply_markup=pv_keyboard())
                elif CallBack.data == 'pv_Help_Button':
                    await CallBack.edit_message_text(help_pv, reply_markup=back_main_pv())
                elif CallBack.data == 'pv_About_Button':
                    await CallBack.edit_message_text(info_pv, reply_markup=back_main_pv())

# ---------------------------- commands list command-------------------------------#
async def list_commands(bot:Client, message:Message):
    await message.reply(await commands_db(message.chat.id))
 
 
# ---------------------------- get all commands on db --------------------------#       
async def commands_db(chatID:int):
        all_key = get_all_key(chatID)
        if all_key:
            list_key = ''
            number_key = 1
            for key in all_key:
                list_key += f'{number_key} - {key}\n' 
                number_key += 1   
            return f'لیست چیزایی که بلدم :\n{list_key}'

        else:
            return commands_empty_error


# ----------------------- forget key -----------------------------------------#
async def del_command(bot:Client, message:Message):
    regex_search = re.search(f'^{bot_name_fa}?.فراموش?.کن', message.text)
    regex_span = regex_search.span()
    key = message.text[regex_span[1]:].strip()
    if len(key) > 1:
        if del_key(message.chat.id, key):
            await message.reply(key_forget_true)
        else:
            await message.reply(key_forget_not_find)
    else:
        await message.reply(len_key_forget_error)


# ---------------------- stats on off --------------------------- #
async def stats_on_off(bot:Client, message:Message):
    if re.search(f'^{bot_name_fa}?.روشن', message.text):
        r.set(f'{message.chat.id}:status', 'True')
        await message.reply(status_on)
    else:
        r.set(f'{message.chat.id}:status', 'False')
        await message.reply(status_off)
            
# -------------------- panel group ----------------------------- #
async def panel_gp(bot:Client, message:Message):
    await message.reply(panel_gp_text, reply_markup=group_panel(message.chat.id))
        
        
        
app.run()