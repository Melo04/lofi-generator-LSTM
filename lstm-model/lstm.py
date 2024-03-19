import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation, BatchNormalization
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint

def get_notes():
    """Get all notes from the midi files"""
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
            # flattens all the objects(key, notes, etc.) into a single list
            parse_notes = midi.flat.notes
    
        for i in parse_notes:
            if isinstance(i, note.Note):
                # appends pitch of a single note extracted as a representation of MIDI pitch value, e.g 60
                notes.append(str(i.pitch))
            elif isinstance(i, chord.Chord):
                # encounters a chord and extracts each notes pitch and represent them as a joined string, e.g 64.67.71
                notes.append('.'.join(str(n) for n in i.normalOrder))
            elif isinstance(i, note.Rest):
                # appends Rest to represent a period of silence ('r')
                notes.append('r')

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)
    
    return notes
        
def notes_sequences(notes, n_vocab):
    """Get sequences used by LSTM Network"""
    pitchnames = sorted(set(item for item in notes))
    # create a dictionary to map pitches to integers
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

def lstm_model(network_input, n_vocab):
    """Create LSTM Neural Network model"""
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model

def train(model, network_input, network_output):
    """train LSTM model"""
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]
    model.fit(network_input, network_output, epochs=200, batch_size=128, callbacks=callbacks_list)

def train_model():
    """Train LSTM to generate music"""
    notes = get_notes()
    vocab = len(set(notes))
    network_input, network_output = notes_sequences(notes, vocab)
    model = lstm_model(network_input, vocab)
    train(model, network_input, network_output)

if __name__ == '__main__':
    train_model()