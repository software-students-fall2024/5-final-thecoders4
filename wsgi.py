from app import create_app  
app = create_app()  # app now refers to the Flask object
if __name__ == "__main__":
    app.run()