import pyaudio
import wave
import sys
import logging
import os

project_path = os.path.dirname(sys.argv[0])

def setup_logger(name, file, level=logging.WARNING):
    # Function to easily create loggers

    handler = logging.FileHandler(file)
    formatter = logging.Formatter("%(asctime)s:%(filename)s:%(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

parent_of_scripts = os.path.abspath(os.path.join(project_path, os.pardir))

# Error logger
error_logger = setup_logger("Error logging", "{}\\Logs\\logging_errors.log".format(parent_of_scripts))

CHUNK_SIZE = 1024

def play_wav(wav_path, chunk_size=CHUNK_SIZE):
    try:
        wf = wave.open(wav_path, 'rb')
    except IOError:
        error_logger.error("IOError opening file {}".format(wav_path))
        raise SystemExit

    except EOFError:
        error_logger.error("EOFError opening file {}".format(wav_path))
        raise SystemExit

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    p.terminate()


def main():
    play_wav(sys.argv[1])

if __name__ == '__main__':
    main()
