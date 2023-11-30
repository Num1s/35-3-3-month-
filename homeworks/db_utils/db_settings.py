import aiosqlite

class Database(object):
	def __init__(self):
		self.name = 'C:/Users/user/Documents/Geeks/Backend/month_3/Home-Works/homeworks/dbs/main_bot.db'

	async def create_table(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query_houses = '''CREATE TABLE IF NOT EXISTS houses(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT,
				location TEXT,
				price TEXT,
				url TEXT
			)'''
			await cursor.execute(query_houses)
			query_newsletter = '''CREATE TABLE IF NOT EXISTS newsletter(
				user_id INTEGER,
				text_user TEXT,
				date_start TEXT
			)
			'''
			await cursor.execute(query_newsletter)
			query_user = '''CREATE TABLE IF NOT EXISTS users(
				id INTEGER,
				product_id INTEGER
			)'''
			await cursor.execute(query_user)
			query_category = '''CREATE TABLE IF NOT EXISTS categories(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT
			)'''
			await cursor.execute(query_category)
			query = '''CREATE TABLE IF NOT EXISTS products(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				price DECIMAL,
				author TEXT,
				in_stock BOOLEAN DEFAULT None,
				category_id INTEGER,
				FOREIGN KEY (category_id) REFERENCES category (id)
			)'''
			await cursor.execute(query)
			await db.commit()

	async def drop_table_house(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'DROP TABLE IF EXISTS houses'
			await cursor.execute(query)
			await db.commit()

	async def insert_default_category(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'INSERT INTO categories (name) VALUES (?), (?), (?)'
			await cursor.execute(query, ('Книги', 'Сувениры', 'Комиксы'))

	async def insert_default_book(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			products_list = [
				('Волк и Красная шапочка', 12.33, 'Шарлем Перро', True, 1),
				('Властелин колец', 16.22, 'Джон Р. Р. Толкин', False, 1),
				('Тёмные начала', 14.55, 'Филип Пулман', True, 1),
				('Автостопом по галактике', 19.22, 'Дуглас Адамс', False, 1),
				('Гордость и предубеждение', 19.22, 'Джейн Остин', True, 1),
				('Кружка', 19.12, 'Эмаль', True, 2),
				('Ручка', 22.22, 'Hatber', True, 2),
				('Тетрадь', 15.32, 'Hatber', True, 2),
				('Хранители', 150.23, 'DC Comics', True, 3),
				('Бэтмен. Убийственная шутка', 150.23, 'DC Comics', True, 3),
				('Сказки', 120.43, 'Vertigo', True, 3),
			]
			for i in products_list:
				query = f'INSERT INTO products (name, price, author, in_stock, category_id) VALUES (?, ?, ?, ?, ?)'
				await cursor.execute(query, (i[0], i[1], i[2], i[3], i[4]))
			await db.commit()

	async def insert_user_product(self, user: int, product: int):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'INSERT INTO users VALUES (?, ?)'
			await cursor.execute(query, (user, product))
			await db.commit()

	async def insert_user_scheduler(self, user: int, text: str, date):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'INSERT INTO newsletter VALUES (?, ?, ?)'
			await cursor.execute(query, (user, text, date))
			await db.commit()

	async def insert_value_in_houses(self, type_, value, id_):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			if not await self.get_house_id(id_):
				print(123)
				query = f'INSERT INTO houses ({type_}) VALUES (?)'
				await cursor.execute(query, (value,))
			else:
				if type_ == 'location':
					query = 'UPDATE houses SET location = ? WHERE id = ?'
					await cursor.execute(query, (value, id_,))
				elif type_ == 'price':
					query = 'UPDATE houses SET price = ? WHERE id = ?'
					await cursor.execute(query, (value, id_,))
				elif type_ == 'url':
					query = 'UPDATE houses SET url = ? WHERE id = ?'
					await cursor.execute(query, (value, id_,))

			await db.commit()

	async def get_house_id(self, id_):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM houses WHERE id = ?'
			await cursor.execute(query, (id_,))
			return await cursor.fetchone()

	async def get_user(self, user):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM users WHERE id = ?'
			await cursor.execute(query, (user,))
			return await cursor.fetchall()

	async def get_table(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM products'
			await cursor.execute(query)
			return await cursor.fetchall()

	async def get_table_category(self, ct_id: int):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM products WHERE category_id = ?'
			await cursor.execute(query, (ct_id,))
			return await cursor.fetchall()

	async def get_table_id(self, id_product: int):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM products WHERE id = ?'
			await cursor.execute(query, (id_product,))
			return await cursor.fetchone()

	async def get_users_scheduler(self):
		async with aiosqlite.connect(self.name) as db:
			cursor = await db.cursor()
			query = 'SELECT * FROM newsletter'
			await cursor.execute(query)
			return await cursor.fetchall()