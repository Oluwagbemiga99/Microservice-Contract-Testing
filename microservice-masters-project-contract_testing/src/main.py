from config import Config
from core.Server import server


if __name__ == '__main__':
    server.run(debug=True, port=Config.port, host=Config.host)