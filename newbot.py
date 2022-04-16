import pprint

from telebot import TeleBot, types
from dotenv import load_dotenv
import logging
from scripts import *
from db import *
from os import getenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] - %(message)s', datefmt='%H:%M:%S')
bot = TeleBot(getenv('BOT_API_KEY'))


@bot.message_handler(commands=['start', 'help'])
def start_bot(message: types.Message):
	msg = """This bot will be able to generate random user data for use on suspect sites. Also, you can save the generated passwords and use them in the future.
<i>Developed by @hasnomatter</i>"""
	bot.send_message(chat_id=message.chat.id,
					 text=f'Hello, <b>{message.from_user.first_name.capitalize()}</b>!\n' + msg,
					 parse_mode='HTML')


@bot.message_handler(commands=['person'])
def person_generator(message: types.Message):
	person = person_gen(URL)
	photo = person['photo']
	msg = f"""\
<b>First name:</b>\t{person['first']}
<b>Last name:</b>\t{person['last']}
<b>Born:</b>\t{person['born']}
<b>Phone:</b>\t{person['phone']}
<b>Country:</b>\t{person['country']}
<b>Street:</b>\t{person['street']}
<b>City:</b>\t{person['city']}
<b>State:</b>\t{person['state']}
<b>Postcode:</b>\t{person['postcode']}\n
<b>Username:</b>\t{person['username']}
<b>Pass:</b>\t{person['password']}"""
	bot.send_photo(message.chat.id, photo)
	bot.send_message(message.chat.id, text=msg, parse_mode='HTML')


@bot.message_handler(commands=['quick_reg'])
def quick_reg(message: types.Message):
	data = quick_registration()
	bot.send_message(message.chat.id, f"<b>Login</b>: {data['login']}\n<b>Password</b>: {data['passwd']}",
					 parse_mode='HTML')


@bot.message_handler(commands=['photo'])
def get_photo(message: types.Message):
	bot.send_photo(message.chat.id, get_avatar(URL))


@bot.message_handler(commands=["pass"])
def get_pass(message: types.Message):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_pass"),
				 types.InlineKeyboardButton(text="🔢", callback_data="custom_pass"),
				 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
	bot.send_message(message.chat.id, f"<b>Your password</b>:\n<code>{passgen()}</code>", parse_mode='HTML',
					 reply_markup=keyboard, timeout=200)


@bot.message_handler(commands=["login"])
def get_pass(message: types.Message):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_login"),
				 types.InlineKeyboardButton(text="🔢", callback_data="custom_login"),
				 types.InlineKeyboardButton(text="✅", callback_data="save_login"))
	bot.send_message(message.chat.id, f"<b>Your login</b>:\n<code>{login_gen()}</code>", parse_mode='HTML',
					 reply_markup=keyboard, timeout=200)


@bot.message_handler(content_types=['text'])
def get_name(message):
	# print(message)
	with open(f'{message.from_user.id}', 'w') as f:
		f.write(message.text)


# def custom_password(message: types.Message):
# 	keyboard = types.InlineKeyboardMarkup()
# 	keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_custom_pass"),
# 				 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
# 	bot.send_message(message.chat.id, f"<b>Your password</b>:\n<code>{passgen(int(message.text))}</code>",
# 					 parse_mode='HTML', reply_markup=keyboard)
#
#
# def custom_login(message: types.Message):
# 	keyboard = types.InlineKeyboardMarkup()
# 	keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_custom_login"),
# 				 types.InlineKeyboardButton(text="✅", callback_data="save_login"))
# 	bot.send_message(message.chat.id, f"<b>Your login</b>:\n<code>{login_gen(int(message.text))}</code>",
# 					 parse_mode='HTML', reply_markup=keyboard)
# 	bot.register_next_step_handler(message, )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
	if call.message:
		match call.data:
			case "next_pass":
				keyboard = types.InlineKeyboardMarkup()
				keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_pass"),
							 types.InlineKeyboardButton(text="🔢", callback_data="custom_pass"),
							 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text=f"<b>Your password</b>:\n<code>{passgen()}</code>", parse_mode='HTML',
									  reply_markup=keyboard)
			case 'custom_pass':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="<b>Enter count of symblols</b>", parse_mode='HTML')

				@bot.message_handler(content_types=['text'])
				def custom_pass(message):
					keyboard = types.InlineKeyboardMarkup()
					keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="custom_pass_next"),
								 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
					bot.send_message(chat_id=call.message.chat.id,
									 text=f"<b>Your password</b>:\n<code>{passgen(int(message.text))}</code>",
									 parse_mode='HTML',
									 reply_markup=keyboard)
			case 'custom_pass_next':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="custom_pass_next"),
							 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text=f"<b>Your password</b>:\n<code>{passgen(call.message.entities[1].length)}</code>",
									  parse_mode='HTML',
									  reply_markup=keyboard)
			# bot.register_next_step_handler(call.message, custom_password)
			# case 'next_custom_pass':
			# 	# print(call.message.entities[1].length, type(call.message.entities[1].length))
			# 	keyboard = types.InlineKeyboardMarkup()
			# 	keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_pass"),
			# 				 types.InlineKeyboardButton(text="✅", callback_data="save_pass"))
			# 	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
			# 						  text=f"<b>Your password</b>:\n<code>{passgen(call.message.entities[1].length)}</code>",
			# 						  parse_mode='HTML', reply_markup=keyboard)
			# 	bot.register_next_step_handler(call.message, custom_password)
			case 'save_pass':
				bot.reply_to(call.message, 'Enter name of service:')
				bot.register_next_step_handler(call.message, get_name)
				article = open(f'{call.message.chat.id}').readline().strip()
				user_id = call.from_user.id
				passwd = call.message.text.split('\n')[-1]
				conn = create_connection('bot_db.sqlite')
				res = save_pass(conn, (user_id, passwd, article))
				if isinstance(res, int):
					bot.send_message(chat_id=call.message.chat.id, text=f"<b>Your password</b>:\n<code>{passwd}</code>",
									 parse_mode='HTML')
					bot.reply_to(call.message, 'Saved!')
				else:
					bot.reply_to(call.message, text='Something wrong... Try again later (')
			case 'next_login':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.row(types.InlineKeyboardButton(text="🔄", callback_data="next_login"),
							 types.InlineKeyboardButton(text="🔢", callback_data="custom_login"),
							 types.InlineKeyboardButton(text="✅", callback_data="save_login"))
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text=f"<b>Your login</b>:\n<code>{login_gen()}</code>", parse_mode='HTML',
									  reply_markup=keyboard)
			case 'custom_login':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="<b>Enter count of symblols</b>", parse_mode='HTML')
			# bot.register_next_step_handler(call.message, custom_login)
			case 'next_custom_login':
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="<b>Enter count of symblols</b>", parse_mode='HTML', )
			# bot.register_next_step_handler(call.message, custom_login)
			case 'save_login':
				user_id = call.from_user.id
				login = call.message.text.split('\n')[-1]
				conn = create_connection('bot_db.sqlite')
				res = save_login(conn, (user_id, login))
				if isinstance(res, int):
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
										  text=f"<b>Your login</b>:\n<code>{login}</code>", parse_mode='HTML')
					bot.reply_to(call.message, 'Saved!')
				else:
					bot.send_message(call.message.chat.id, text='Something wrong... Try again later (')


if __name__ == '__main__':
	bot.infinity_polling()
