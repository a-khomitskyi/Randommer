import sqlite3
from os.path import exists


def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(e)

	return conn


def db_init():
	pass


def save_pass(conn, data):
	"""
	Create a new task
	:param conn:
	:param data:
	:return:
	"""

	sql = "INSERT INTO password(user_id, passwd, article) VALUES(?,?,?)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


def save_login(conn, data):
	"""
	Create a new task
	:param conn:
	:param data:
	:return:
	"""

	sql = "INSERT INTO login(user_id, login) VALUES(?,?)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


def save_userdata(conn, data):
	"""
	Create a new task
	:param conn:
	:param data:
	:return:
	"""

	sql = "INSERT INTO password(user_id, login, pass) VALUES(?,?)"
	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

	return cur.lastrowid


if __name__ == '__main__':
	try:
		assert not exists('db_bot.sqlite3')
		with open('db_bot.sqlite3', 'w') as f:
			pass
	except AssertionError:
		pass
