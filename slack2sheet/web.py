from flask import Flask, request


def create_app():
    app = Flask("slack2sheet")

    @app.route("/slack/annotate/")
    def log():
        print(request.get_data())
        return "foobar"

    return app