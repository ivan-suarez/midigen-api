from flask import Flask, jsonify, send_file
import main

app = Flask(__name__)


@app.route('/')
def home():
    generated_sequence = main.generate()
    output = main.midi_to_json(generated_sequence)
    return send_file('my_generated_midi.mid', mimetype='audio/midi')

if __name__ == '__main__':
    app.run(debug=True)
