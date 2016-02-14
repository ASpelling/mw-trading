import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'trading'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
#THREADS_PER_PAGE = 2

# pagination
POST_PER_PAGE = 30 #default = 10
#MAX_SEARCH_RESULTS = 50 #default = 50

# SCTR average, days
SCTR_AVERAGE = 1  #default = 50



