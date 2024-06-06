from http.server import BaseHTTPRequestHandler
from main import extract_data, query_data

logger = logging.getLogger(__name__)

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        logger.info("Extracting data")
        extract_data()
        logger.info("Querying data")
        query_data()
        return
