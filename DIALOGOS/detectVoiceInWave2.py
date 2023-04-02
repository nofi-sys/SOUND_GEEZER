from vad import VoiceActivityDetector
import argparse
import json

def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

if __name__ == "__main__":

    file = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/SAMPLES/8khz/Outer Space Suite (Prelude) Bernard Herrmann.mp4_L.wav'
    out = '/home/nofi/DESARROLLO/PROYECTOS/ASISTENTE DE SONIDO/POSTPRODUCCIÓN/ESA/SAMPLES/SPEECH_DETECTION.json'
    v = VoiceActivityDetector(file)
    raw_detection = v.detect_speech()
    speech_labels = v.convert_windows_to_readible_labels(raw_detection)
    v.plot_detected_speech_regions()
    
    save_to_file(speech_labels, out)
