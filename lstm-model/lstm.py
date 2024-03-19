import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation, BatchNormalization
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint

def train_model():
    notes = get_notes()
    vocab = len(set(notes))
    network_input, network_output = notes_sequences(notes, vocab)
    model = create_network(network_input, vocab)
    train(model, network_input, network_output)

def get_notes():
    notes = []
    for file in glob.glob("midi_songs/*.mid"):
        # return a score
        midi = converter.parse(file)
        print("Training ===> %s" % file)
        parse_notes = None
        try:
            # partition into a part for each unique instrument
            s2 = instrument.partitionByInstrument(midi)
            parse_notes = s2.parts[0].recurse()
        except:
            parse_notes = midi.flat.notes
    
        for i in parse_notes:
            if isinstance(i, note.Note):
                notes.append(str(i.pitch))
            elif isinstance(i, chord.Chord):
                notes.append('.'.join(str(n) for n in i.normalOrder))
            elif isinstance(i, note.Rest):
                notes.append('r')
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)
    
    return notes
        
def notes_sequences(notes, n_vocab):
    pitchnames = sorted(set(item for item in notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    network_input = []
    network_output = []

    for i in range(0, len(notes) - 1000, 1):
        sequence_in = notes[i:i + 1000, 1]
        sequence_out = notes[i + 1000]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append([note_to_int[sequence_out]])

    n_patterns = len(network_input)

    network_input = np.reshape(network_input, (n_patterns, 1000, 1))
    # normalization
    network_input = network_input / float(n_vocab)
    network_output = to_categorical(network_output)
    return (network_input, network_output)

def create_network(network_input, n_vocab):
    pass

def train(model, network_input, network_output):
    pass

if __name__ == '__main__':
    train_model()