# from faker import Faker

# fake = Faker()

# FIELD_GENERATORS = {
#     # Personal Information
#     "first_name": lambda _: fake.first_name(),
#     "last_name": lambda _: fake.last_name(),
#     "full_name": lambda _: fake.name(),
#     "username": lambda _: fake.user_name(),
#     "email": lambda _: fake.email(),
#     "password": lambda _: fake.password(),
#     "ssn": lambda _: fake.ssn(),
#     "phone_number": lambda _: fake.phone_number(),
#     "age": lambda _: fake.random_int(min=18, max=100),
#     "date_of_birth": lambda _: fake.date_of_birth(minimum_age=18, maximum_age=100),
#     "gender": lambda _: fake.random_element(elements=["Male", "Female", "Other"]),

#     # Address and Location
#     "street_address": lambda _: fake.street_address(),
#     "street_name": lambda _: fake.street_name(),
#     "city": lambda _: fake.city(),
#     "state": lambda _: fake.state(),
#     "state_abbr": lambda _: fake.state_abbr(),
#     "zipcode": lambda _: fake.zipcode(),
#     "country": lambda _: fake.country(),
#     "country_code": lambda _: fake.country_code(),
#     "latitude": lambda _: fake.latitude(),
#     "longitude": lambda _: fake.longitude(),
#     "time_zone": lambda _: fake.timezone(),
#     "address": lambda _: fake.address(),

#     # Business and Finance
#     "company": lambda _: fake.company(),
#     "company_suffix": lambda _: fake.company_suffix(),
#     "job_title": lambda _: fake.job(),
#     "currency": lambda _: fake.currency_name(),
#     "currency_code": lambda _: fake.currency_code(),
#     "iban": lambda _: fake.iban(),
#     "bic": lambda _: fake.bban(),
#     "credit_card_number": lambda _: fake.credit_card_number(),
#     "credit_card_expiry": lambda _: fake.credit_card_expire(),
#     "credit_card_provider": lambda _: fake.credit_card_provider(),
#     "bank_country": lambda _: fake.bank_country(),

#     # Internet and Network
#     "ip_v4": lambda _: fake.ipv4(),
#     "ip_v6": lambda _: fake.ipv6(),
#     "mac_address": lambda _: fake.mac_address(),
#     "domain_name": lambda _: fake.domain_name(),
#     "url": lambda _: fake.url(),
#     "uri": lambda _: fake.uri(),
#     "slug": lambda _: fake.slug(),
#     "uuid": lambda _: fake.uuid4(),

#     # Dates and Time
#     "date": lambda _: fake.date(),
#     "time": lambda _: fake.time(),
#     "date_time": lambda _: fake.date_time(),
#     "iso8601": lambda _: fake.iso8601(),
#     "date_time_this_century": lambda _: fake.date_time_this_century(),
#     "date_time_this_decade": lambda _: fake.date_time_this_decade(),
#     "day_of_week": lambda _: fake.day_of_week(),
#     "month": lambda _: fake.month(),
#     "year": lambda _: fake.year(),

#     # Payment
#     "credit_card_full": lambda _: fake.credit_card_full(),
#     "payment_method": lambda _: fake.random_element(elements=["Visa", "MasterCard", "PayPal", "Stripe"]),
#     "price": lambda _: fake.pricetag(),

#     # Product Information
#     "product_name": lambda _: fake.word(),
#     "product_category": lambda _: fake.random_element(elements=["Electronics", "Books", "Clothing", "Furniture", "Food"]),
#     "product_description": lambda _: fake.sentence(nb_words=10),
#     "product_code": lambda _: fake.bothify(text='???-#######'),

#     # Miscellaneous
#     "boolean": lambda _: fake.boolean(),
#     "uuid": lambda _: fake.uuid4(),
#     "random_digit": lambda _: fake.random_digit(),
#     "random_number": lambda _: fake.random_number(digits=8),
#     "color_name": lambda _: fake.color_name(),
#     "hex_color": lambda _: fake.hex_color(),
#     "file_extension": lambda _: fake.file_extension(),
#     "mime_type": lambda _: fake.mime_type(),

#     # Language and Culture
#     "language_code": lambda _: fake.language_code(),
#     "locale": lambda _: fake.locale(),
#     "currency_symbol": lambda _: fake.currency_symbol(),
#     "country_code": lambda _: fake.country_code(),
#     "country": lambda _: fake.country(),

#     # Text and Writing
#     "sentence": lambda _: fake.sentence(),
#     "paragraph": lambda _: fake.paragraph(),
#     "text": lambda _: fake.text(max_nb_chars=200),
#     "word": lambda _: fake.word(),
#     "words": lambda _: fake.words(nb=5),

#     # Numbers and Values
#     "integer": lambda _: fake.random_int(min=0, max=1000),
#     "float": lambda _: fake.pyfloat(left_digits=5, right_digits=2, positive=True),
#     "decimal": lambda _: fake.pydecimal(left_digits=5, right_digits=2, positive=True),

#     # Vehicle Information
#     "vehicle_make": lambda _: fake.vehicle_make(),
#     "vehicle_model": lambda _: fake.vehicle_model(),
#     "license_plate": lambda _: fake.license_plate(),

#     # Medical Information
#     "blood_type": lambda _: fake.random_element(elements=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
#     "medication": lambda _: fake.lexify(text='Med-???-#####'),

#     # Scientific Data
#     "atomic_element": lambda _: fake.random_element(elements=["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron"]),
#     "planet": lambda _: fake.random_element(elements=["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]),

#     # Geographic Details
#     "continent": lambda _: fake.random_element(elements=["Africa", "Antarctica", "Asia", "Europe", "North America", "Australia", "South America"]),
#     "ocean": lambda _: fake.random_element(elements=["Atlantic", "Pacific", "Indian", "Arctic", "Southern"]),

#     # Sport and Entertainment
#     "sport": lambda _: fake.random_element(elements=["Soccer", "Basketball", "Tennis", "Swimming", "Cycling"]),
#     "movie_title": lambda _: fake.catch_phrase(),
#     "genre": lambda _: fake.random_element(elements=["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]),
# }

# # Example usage
# for field, generator in FIELD_GENERATORS.items():
#     print(f"{field}: {generator(None)}")
