from flask import Flask

app = Flask(__main__)

@app.route("/")
def home():
    return "Hello starting the website"



if __name__ == "__main__":
    app.run()