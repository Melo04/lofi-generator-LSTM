## __LoFi Music Generator with LSTM model__
A LoFi music webplayer with AI generated tracks that utilizes LSTM model to generate music. Try out the webplayer [here](https://melo04.github.io/lofi-generator-LSTM/). For how I built it, check out the blog post [here](https://melodykoh.vercel.app/blog/lofi-generator-lstm).

![LOFI Music Generator](./assets/output.gif)

This LSTM model is trained on MIDI dataset and the webplayer is built with [Tone.js](https://tonejs.github.io/). Users could chose the theme of the music, the drum beats as well as the movie dialogues to be played. The model will generate the music based on the user's input.

To run the LSTM model locally, clone the repository and cd into lstm-model
1. Then run the following command:
```bash
python lstm.py
```
2. After that, run:
```bash
python predict.py
```