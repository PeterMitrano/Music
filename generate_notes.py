from numpy import random
from music21 import midi


def populate_midi_track_from_data(mt, data):
    t = 0
    tLast = 0
    for d, p, v in data:
        dt = midi.DeltaTime(mt)
        dt.time = t - tLast
        # add to track events
        mt.events.append(dt)

        me = midi.MidiEvent(mt)
        me.type = "NOTE_ON"
        me.channel = 1
        me.time = None  # d
        me.pitch = p
        me.velocity = v
        mt.events.append(me)

        # add note off / velocity zero message
        dt = midi.DeltaTime(mt)
        dt.time = d
        # add to track events
        mt.events.append(dt)

        me = midi.MidiEvent(mt)
        me.type = "NOTE_ON"
        me.channel = 1
        me.time = None  # d
        me.pitch = p
        me.velocity = 0
        mt.events.append(me)

        tLast = t + d  # have delta to note off
        t += d  # next time

    # add end of track
    dt = midi.DeltaTime(mt)
    dt.time = 0
    mt.events.append(dt)

    me = midi.MidiEvent(mt)
    me.type = "END_OF_TRACK"
    me.channel = 1
    me.data = ''  # must set data to empty string
    mt.events.append(me)

    return mt

mt = midi.MidiTrack(1)

# describe the chord progression
chords = [
    {'beats': 16, 'pitches': [
                             35, 39, 42, 46,
                             47, 51, 54, 58,
                             59, 63, 66, 70,
                             71, 75, 78, 82
                             ]}, # B7
    {'beats': 16, 'pitches': [
                             34, 37, 41, 44,
                             46, 49, 53, 56,
                             58, 61, 65, 68,
                             70, 73, 77, 80
                             ]}, # B flat minor 7 / D flat
    {'beats': 16, 'pitches': [
                             32, 35, 39,
                             44, 47, 41,
                             56, 59, 63,
                             68, 71, 75,
                             ]}, # A flat minor 7
    {'beats': 8, 'pitches': [
                             37, 41, 44,
                             49, 53, 55,
                             61, 65, 68,
                             73, 77, 80,
                             ]}, # D flat major
    {'beats': 8, 'pitches': [
                             36, 39, 45,
                             48, 51, 57,
                             60, 63, 69,
                             72, 75, 81,
                             ]}, # E flat diminished 7 ??? not sure
]

# duration, pitch, velocity
data = [[256, 59, 100]] # one start note
total_duration = 0

beats_per_measure = 64
measures = 16
num_beats = measures * beats_per_measure
chord_idx = 0
beat_idx = 1
last_real_pitch = 59

# note array is ordered [duration, pitch, velocity]
for i in range(1, num_beats):

    # generate one beat
    note = [256, 0, 0]
    current_chord = chords[chord_idx]

    e = random.random()
    last_note_was_rest = data[-1][2] < 0
    last_note_pitch = data[-1][1]
    if e < 0.15:
        # rest
        note[0] = 256
        note[1] = 0
        note[2] = 0
        data.append(note)
    elif last_note_was_rest and e < 0.25 and last_note_pitch in current_chord['pitches']:
        # sustain rest
        data[-1][0] += 256
    elif not last_note_was_rest and e < 0.70 and last_note_pitch in current_chord['pitches']:
        # sustain note
        data[-1][0] += 256
    else:
        # new note
        note[0] = 256  # 256 is 16th note

        e2 = random.random()
        if e2 < 0.02:  # totally random note
            for i in range(20):
                pitch = random.randint(30, 90)
                note[1] = pitch
                pitch_distance = abs(last_real_pitch - pitch)
                if pitch_distance < 6:
                    break
        elif e2 < 0.06:
            note[1] = last_real_pitch - 1
        elif e2 < 0.10:
            note[1] = last_real_pitch + 1
        else:
            # pick random notes until we find one close enough to our last note
            # because large register changes sound weird
            for i in range(100):
                # pick note from chord
                rand_idx = random.randint(0, len(current_chord['pitches']))
                pitch = current_chord['pitches'][rand_idx]
                note[1] = pitch
                pitch_distance = abs(last_real_pitch - pitch)
                if pitch_distance < 6:
                    break

        note[2] = random.randint(20, 127)
        last_real_pitch = note[1]
        data.append(note)

    # change chords
    beat_idx += 1
    if beat_idx == current_chord['beats']:
        beat_idx = 0
        chord_idx = (chord_idx + 1) % len(chords)

    print(i, ' out of ', num_beats)

print(data)
populate_midi_track_from_data(mt, data)

mf = midi.MidiFile()
mf.ticksPerQuarterNote = 1024 #  magic number?
mf.tracks.append(mt)

mf.open('comp1 Project/melody.mid', 'wb')
mf.write()
mf.close()

