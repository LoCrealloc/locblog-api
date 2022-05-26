config = {}

db_host = "localhost"
db_port = "5432"
db_user = "test"
db_password = "test123"
db_name = "test"

config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
