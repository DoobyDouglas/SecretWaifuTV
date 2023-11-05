from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav
from bark.generation import generate_text_semantic, preload_models
from bark.api import semantic_to_waveform
import nltk
import numpy
from utils import subs_reader
import os
import time
import ffmpeg
from datetime import datetime as dt
# os.environ["SUNO_OFFLOAD_CPU"] = "True"
# os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# preload_models()
# nltk.download('punkt')

path = 'D:/TEST/NINJA/04/1.ass'

start = dt.now()

text_list = subs_reader(path)
for sub in text_list:
    text = sub.text.replace("\n", " ")
    sentences = nltk.sent_tokenize(f'{text}', language='russian')
    silence = numpy.zeros(int(0.25 * SAMPLE_RATE))
    pieces = []
    for sentence in sentences:
        # semantic_tokens = generate_text_semantic(sentence, history_prompt='v2/ru_speaker_3', min_eos_p=0.05)
        # audio_array = semantic_to_waveform(semantic_tokens, history_prompt='v2/ru_speaker_3')

        audio_array = generate_audio(sentence, history_prompt='v2/ru_speaker_3')

        pieces += [audio_array, silence.copy()]
    file = f"D:/TEST/NINJA/04/voice_{sub.id}.wav"
    write_wav(file, SAMPLE_RATE, numpy.concatenate(pieces))
    # input_file = ffmpeg.input(os.path.normpath(file))
    # ffmpeg.run(ffmpeg.output(input_file, f'{os.path.splitext(file)[0]}.flac'))
print(dt.now() - start)

# параметр history_prompt в обоих функциях
# v2/ru_speaker_9 сээээээ тян
# v2/ru_speaker_6 норм тян
# v2/ru_speaker_5 тоже тян
# v2/ru_speaker_3 норм кун