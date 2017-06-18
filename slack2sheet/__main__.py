from slack2sheet.web import create_app
import sys


if __name__ == '__main__':
    app = create_app(sys.argv[1], sys.argv[2])
    app.run(host="0.0.0.0", port=8080)