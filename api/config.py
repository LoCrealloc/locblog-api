config = {}

# set the stuff below to the values you need for your setup to work

db_host = "localhost"
db_port = "5432"
db_user = "test"
db_password = "test"
db_name = "test"

redis_host = "localhost"
redis_port = 6379
redis_db = 0

smtp_user = ""
smtp_password = ""
smtp_server = ""
smtp_port = 587

config["SECERET_KEY"] = ""

config["JWT_COOKIE_SECURE"] = True  # You should always set this to 'True' unless you know exactly what you do

config["JWT_SESSION_COOKIE"] = False

config["JWT_COOKIE_CSRF_PROTECT"] = True  # You should always set this to 'True' unless you know exactly what you do

# do not change the stuff below

config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


