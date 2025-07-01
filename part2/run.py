from app import create_app

app = create_app("config.DevelopmentConfig")

if __name__ == '__main__':
    print("DEBUG =", app.config["DEBUG"])
    app.run()
