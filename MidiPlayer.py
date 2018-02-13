import pygame.midi
import time

MAX_VOLUME = 127

#Wraps the pygame.midi module to add functionality such as playing chords by name
class MidiPlayer:

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    noteLetters = {"C" : 0, "C#" : 1, "D" : 2, "D#" : 3, "E" : 4, "F" : 5, "F#" : 6, "G" : 7, "G#" : 8, "A" : 9, "A#" : 10, "B" : 11}
    note_mapping = []
    volume = MAX_VOLUME
    
    def __init__(self):
        pygame.midi.init()
        
        self.init_note_mapping()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)
    
    #Maps a given octave and note to the midi value table
    def mapNote(self, octave, note_val):
        mapping = self.note_mapping[octave + 1][note_val]
        print("Mapping: ", mapping)
        return mapping
    
    #Plays a single note given a mapping
    def playMappedNote(self, mapping, volume):
        self.player.note_on(mapping, volume)
        time.sleep(1)
        self.player.note_off(mapping, volume)
        
    #Plays a single note given in C-B notation
    def playNote(self, octave, note, volume):
        self.playMappedNote(self.mapNote(octave, self.noteLetters[note]), volume)
    
    #Creates a major scale given a base note
    def createMajScale(self, base_note):
        scale = []
        index = self.noteLetters[base_note]
        for x in range(5, 11):
            scale.append(self.notes[index])
            if(77 % x == 0):
                index += 1
            else:
                index += 2
            if(index >= len(self.notes)):
                    index =  index - len(self.notes)
        return scale
        
    #Constructs a major chord from its base note
    def playMajChord(self, octave, base_note):
        base_note_mapping = self.mapNote(octave, self.noteLetters[base_note])
        if ((base_note_mapping + 7) < 128):
            self.player.note_on(base_note_mapping, self.volume)
            self.player.note_on(base_note_mapping + 4, self.volume)
            self.player.note_on(base_note_mapping + 7, self.volume)
            time.sleep(1)
            self.player.note_off(base_note_mapping, self.volume)
            self.player.note_off(base_note_mapping + 4, self.volume)
            self.player.note_off(base_note_mapping + 7, self.volume)
            
    #Constructs a major seventh chord from its base note
    def playMaj7Chord(self, octave, base_note):
        base_note_mapping = self.mapNote(octave, self.noteLetters[base_note])
        if ((base_note_mapping + 11) < 128):
            self.player.note_on(base_note_mapping, self.volume)
            self.player.note_on(base_note_mapping + 4, self.volume)
            self.player.note_on(base_note_mapping + 7, self.volume)
            self.player.note_on(base_note_mapping + 11, self.volume)
            time.sleep(1)
            self.player.note_off(base_note_mapping, self.volume)
            self.player.note_off(base_note_mapping + 4, self.volume)
            self.player.note_off(base_note_mapping + 7, self.volume)
            self.player.note_off(base_note_mapping + 11, self.volume)
    
    #Populates the note_mapping array to represent the midi value table
    #Table contains 9 rows with 11 columns each containing values 0-127 in ascending order
    #The array will be empty from note_mapping[9][8] to note_mapping[9][11]
    def init_note_mapping(self):
        counter = 0
        for row in range(10):
            # Add an empty array that will hold each cell in the row
            self.note_mapping.append([])
            for column in range(12):
                self.note_mapping[row].append(counter)  # Append a cell
                counter += 1
    
    #Shuts down pygame.midi
    def quit(self):
        del self.player
        pygame.midi.quit()
        
    def set_volume(self, volume):
        if(volume > 0 and volume < 128):
            self.volume = volume
            
    def set_octave(self, octave):
        if(octave > -2 and octave < 12):
            self.octave = octave
        
player = MidiPlayer()
#player.playMajChord(4, "C", MAX_VOLUME)
scale = player.createMajScale("D")
for note in scale:
    player.playMajChord(4, note)

player.quit()