from flask import Flask
import main

app = Flask(__name__)


@app.route('/')
def home():
    generated_sequence = main.generate()
    return generated_sequence

if __name__ == '__main__':
    app.run(debug=True)
