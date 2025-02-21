from mido import MidiFile, MidiTrack, Message

from tensorflow.keras.models import load_model
import numpy as np



def generate():
    model = load_model('bach_one_note-0_2.keras')

    starting_sequence = [(2.75, 3.25, 72, 50),
    (3.25, 4.0, 72, 50),
    (4.0, 4.25, 72, 52),
    (4.25, 4.5, 74, 47),
    (4.5, 4.5, 72, 46),
    (4.5, 4.75, 71, 46),
    (4.75, 5.0, 72, 52),
    (5.0, 5.25, 77, 40),
    (5.25, 5.5, 72, 44),
    (6.0, 6.5, 69, 43),
    (6.5, 7.25, 72, 48),
    (7.25, 8.0, 64, 44),
    (8.0, 9.25, 67, 53),
    (9.25, 10.0, 65, 48),
    (10.0, 10.75, 65, 73),
    (10.0, 10.75, 60, 40),
    (10.75, 11.25, 67, 75),
    (10.75, 11.25, 64, 51),
    (11.25, 12.0, 69, 76),
    (11.25, 12.0, 65, 52),
    (11.25, 12.0, 60, 40),
    (12.0, 13.0, 70, 77),
    (12.0, 13.0, 65, 63),
    (13.0, 13.0, 72, 61),
    (13.0, 13.25, 74, 57),
    (13.25, 13.5, 72, 55),
    (14.0, 14.5, 65, 46),
    (14.5, 15.25, 64, 52),
    (15.25, 16.0, 65, 46),
    (14.5, 16.0, 59, 25),
    (16.0, 17.25, 69, 47),
    (16.0, 17.25, 65, 32),
    (17.25, 18.0, 64, 21),
    (17.25, 18.0, 67, 46),
    (18.0, 18.75, 67, 54),
    (16.0, 18.75, 60, 32),
    (18.75, 19.25, 67, 59),
    (19.25, 19.75, 67, 65),
    (19.75, 20.0, 67, 66),
    (20.0, 21.0, 79, 74),
    (21.0, 21.25, 74, 50),
    (21.25, 21.25, 71, 46),
    (21.25, 22.0, 67, 48),
    (22.0, 22.5, 67, 55),
    (22.5, 23.25, 67, 63),
    (23.25, 23.75, 67, 69),
    (23.75, 24.0, 67, 68),
    (24.0, 25.75, 79, 73),
    (25.75, 25.75, 81, 56),
    (25.75, 26.0, 83, 49)]

    starting_sequence_one = [(2.75, 3.25, 64, 21)]

    seed_index = 0
    seed_sequence = starting_sequence_one # Starting with an existing sequence as seed
    num_notes_to_generate = 100  # Number of notes you want to generate
    generated_notes = generate_notes(model, seed_sequence, num_notes_to_generate)
    print(generated_notes)
    create_midi_from_notes(generated_notes)
    return generated_notes

def generate_notes(model, seed_sequence, num_notes_to_generate):
    generated_sequence = seed_sequence.copy()  # Copy the seed sequence
    for _ in range(num_notes_to_generate):
        # Reshape the sequence to match the model's input shape: (1, 50, 4)
        input_sequence = np.array(generated_sequence[-1:]).reshape(1, 1, 4)
        
        # Predict the next note
        predicted_note = model.predict(input_sequence)[0]  # model.predict returns a batch, so get the first
        
        # Append the predicted note to the sequence
        generated_sequence.append(predicted_note.tolist())
        
    return generated_sequence

# Assuming `x_train` is your training data and `seed_index` is some index of your choice3
#seed_index = 0
#seed_sequence = starting_sequence # Starting with an existing sequence as seed
#num_notes_to_generate = 100  # Number of notes you want to generate

# Generate notes
#generated_notes = generate_notes(model, seed_sequence, num_notes_to_generate)

def create_midi_from_notes(notes, output_file='generated_sequence.mid'):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    # Assuming the first event happens at time 0
    last_event_time = 0
    
    for note in notes:
        print(note)
        start_time, duration, pitch, velocity = map(float, note)
        print(duration)
        duration = abs(duration*10)
        end_time = start_time +  duration
        time_step = 0.25
        start_time = round(start_time / time_step) * time_step
        end_time = round(end_time / time_step) * time_step
        # Ensure non-negative delta times
        #delta_time_on = max(0, start_time - last_event_time)
        #delta_time_off = max(0, end_time - start_time)
        # Assuming a standard conversion, adjust based on your actual data and tempo
        milliseconds_per_tick = 5 / midi.ticks_per_beat  # For 120 BPM and 480 TPB
        delta_time_on = int(max(0, start_time - last_event_time)/milliseconds_per_tick)
        delta_time_off = int(max(0, end_time - start_time)/milliseconds_per_tick)

        
        # Update last event time for the next iteration
        # For note_on, this is the start time of the current note
        last_event_time = start_time
        print(start_time)
        print(duration)
        print(end_time)
        # Add the note_on message
        track.append(Message('note_on', note=int(pitch), velocity=int(velocity), time=delta_time_on))
        # For note_off, update the last event time to be the end time of the current note
        last_event_time = end_time
        
        # Add the note_off message with time since the note_on
        track.append(Message('note_off', note=int(pitch), velocity=0, time=delta_time_off))
    
    midi.save(output_file)
  #  return output_file

#output_path = 'my_generated_midi.mid'
#create_midi_from_notes(generated_notes, output_file=output_path)



def midi_to_json(generated_notes):
    output_path = 'my_generated_midi.mid'
    create_midi_from_notes(generated_notes)
    midi = MidiFile(output_path)
    events_list = []
    for track in midi.tracks:
        for msg in track:
            # Filter out meta messages and non-note events if desired
            if not msg.is_meta and msg.type in ['note_on', 'note_off']:
                event = {
                    'type': msg.type,
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': msg.time
                }
                events_list.append(event)
    return events_list

