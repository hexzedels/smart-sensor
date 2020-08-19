from myproject import app

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.run()
