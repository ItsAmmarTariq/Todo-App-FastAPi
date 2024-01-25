import logging
import sys


#get logger

logger=logging.getLogger()

# create formattor
format = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler=logging.FileHandler("app.log",mode='a')

stream_handler.setFormatter(format)    
file_handler.setFormatter(format)

logger.handlers=[stream_handler,file_handler]
logging.getLogger('bcrypt').setLevel(logging.ERROR)
logger.setLevel(logging.INFO)