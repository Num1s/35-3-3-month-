import aiosqlite

class Database(object):
	def __init__(self):
		self.name = 'dbs/main.db'

	async def create_table(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = '''CREATE TABLE IF NOT EXISTS books(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				price DECIMAL,
				author TEXT,
				in_stock BOOLEAN DEFAULT None
			)'''
			await cursor.execute(query)
			await db.commit()

	async def insert_default_book(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			books_list = [
				('Волк и Красная шапочка', 12.33, 'Шарлем Перро', True),
				('Властелин колец', 16.22, 'Джон Р. Р. Толкин', False),
				('Тёмные начала', 14.55, 'Филип Пулман', True),
				('Автостопом по галактике', 19.22, 'Дуглас Адамс', False),
				('Гордость и предубеждение', 19.22, 'Джейн Остин', True)
			]
			for i in books_list:
				query = f'INSERT INTO books (name, price, author, in_stock) VALUES (?, ?, ?, ?)'
				await cursor.execute(query, (i[0], i[1], i[2], i[3],))
			await db.commit()

	async def get_table(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM books'
			await cursor.execute(query)
			return await cursor.fetchall()