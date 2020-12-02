import sys
import logging


logging.basicConfig(
    format="[%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(asctime)s %(message)s ",
    level=logging.INFO,
)
logging.StreamHandler(sys.stdout)
logger = logging.getLogger("brev-rest")
logger.setLevel(logging.DEBUG)
