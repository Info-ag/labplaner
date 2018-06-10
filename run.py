if __name__ == '__main__':
    from src.main import app, db
    db.create_all()
    app.run(port=5000)
