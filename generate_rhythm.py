from numpy import random
from music21 import midi

mt = midi.MidiTrack(1)

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

# duration, pitch, velocity
data = [[256, 36, 100]] # one start note
total_duration = 0

beats_per_measure = 16
measures = 64
num_beats = measures * beats_per_measure
beat_idx = 1

# note array is ordered [duration, pitch, velocity]
for i in range(1, num_beats):

    # generate one beat
    note = [256, 0, 0]

    e = random.random()
    last_note_was_rest = data[-1][2] < 0
    if e < 0.15 and beat_idx > 0: # no resting on down beat
        # rest
        note[0] = 256
        note[1] = 0
        note[2] = 0
        data.append(note)
    elif last_note_was_rest and e < 0.25 and beat_idx > 0:
        # sustain rest
        data[-1][0] += 256
    elif not last_note_was_rest and e < 0.50 and beat_idx > 0:
        # sustain note
        data[-1][0] += 256
    else:
        # new note
        if beat_idx % 4 == 0:
            pitch = 36
        else:
            pitch = random.randint(36, 52)
        note[0] = 256  # 256 is 16th note
        note[1] = pitch
        note[2] = random.randint(40, 100)
        last_real_pitch = note[1]
        data.append(note)

    # change chords
    beat_idx += 1
    if beat_idx == beats_per_measure/4:
        beat_idx = 0
    print(i, ' out of ', num_beats)

print(data)
populate_midi_track_from_data(mt, data)

mf = midi.MidiFile()
mf.ticksPerQuarterNote = 1024 #  magic number?
mf.tracks.append(mt)

mf.open('comp1 Project/rhythm.mid', 'wb')
mf.write()
mf.close()
