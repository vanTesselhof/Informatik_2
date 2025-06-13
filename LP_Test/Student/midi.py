from midi2audio import FluidSynth
from midiutil import MIDIFile

# MIDI-Datei erzeugen
track = 0
channel = 0
time = 0     # Startzeit
tempo = 90   # BPM
volume = 100 # Lautstärke

mf = MIDIFile(1)
mf.addTempo(track, time, tempo)

# Notenfolge (MIDI-Noten, Länge in Vierteln)
notes = [
    (78, 0.5),       # F#5 Auftakt
    (74, 1), (74, 1), (76, 1),      # D5, D5, E5
    (78, 1), (76, 1), (74, 1),      # F#5, E5, D5
    (79, 1), (78, 1), (76, 1),      # G5, F#5, E5
    (74, 1), (74, 1), (69, 1),      # D5, D5, A4
    (71, 1), (71, 1), (85, 1),      # B4, B4, C#6
    (86, 1), (81, 1), (78, 1),      # D6, A5, F#5
    (76, 1), (74, 1), (74, 1),      # E5, D5, D5
    (74, 3)                         # D5 Schluss
]

# Noten hinzufügen
for pitch, duration in notes:
    mf.addNote(track, channel, pitch, time, duration, volume)
    time += duration

# Speichern
output_path = "/mnt/data/HB04_Melodie.mid"
with open(output_path, "wb") as f:
    mf.writeFile(f)

output_path
