#app.py

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from ui import app as ui
from api import app as api 

application = DispatcherMiddleware(ui, {
    '/api': api
})
