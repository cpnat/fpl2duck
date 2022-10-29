from api.utils import get_bootstrap
from api.types.bootstrap import Bootstrap
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    bootstrap: Bootstrap = get_bootstrap()
    logger.info(bootstrap)
