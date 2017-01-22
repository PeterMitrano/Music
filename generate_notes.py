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
data = []
#[[1024, 60, 90], [1024, 50, 70], [1024, 51, 120],[1024, 62, 80], ]
last_note = []
for i in range(1024): # should be 1024
    note = [1024, 0, 0]
    e = random.random()
    if e < 0.75:
        # new note
        duration = abs(int(random.randn() + 2))
        note[0] = duration * 1024
        note[1] = random.randint(30,90)
        note[2] = random.randint(20, 127)
        data.append(note)
    else:
        # rest
        note[2] = 0
        data.append(note)

    last_note = note


populate_midi_track_from_data(mt, data)
print(mt)

mf = midi.MidiFile()
mf.ticksPerQuarterNote = 1024 #  magic number?
mf.tracks.append(mt)

mf.open('comp1 Project/out.mid', 'wb')
mf.write()
mf.close()
