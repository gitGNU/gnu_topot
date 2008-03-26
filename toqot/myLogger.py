import logging

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/tmp/temp.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
log = logger.info
