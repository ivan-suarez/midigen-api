from flask import Flask, jsonify, send_file
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    generated_sequence = main.generate()
    #output = main.midi_to_json(generated_sequence)
    return send_file('generated_sequence.mid', mimetype='audio/midi')

if __name__ == '__main__':
    app.run(debug=True)
