from __init__ import create_app

if __name__ == "__main__":
    api = create_app()

    api.debug = True
    api.run(host="0.0.0.0", port=5001)
