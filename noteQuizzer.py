import pygame.midi
import time
import random
import copy
from collections import deque

VOLUME = 127
notesA = {"C" : 0, "C#" : 1, "D" : 2, "D#" : 3, "E" : 4, "F" : 5, "F#" : 6, "G" : 7, "G#" : 8, "A" : 9, "A#" : 10, "B" : 11}
notesB = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
C_MAJ = [0, 2, 4, 5, 7, 9, 11]
counter = 0
note_mapping = []

for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    note_mapping.append([])
    for column in range(12):
        note_mapping[row].append(counter)  # Append a cell
        counter += 1

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)

octave = int(input("Enter an octave (0-8):"))

def addNote(base_list, note_pool):
    #Pick a random note from the base list, then remove it from the list
    #note_index = random.randint(0, len(base_list) - 1)
    #note_val = base_list[note_index]]
    
    #Take first item from list then delete
    note_val = base_list[0]
    del base_list[0]
    
    #Add note to the list of possible notes
    note_pool.append(note_val)
    
    mapping = mapNote(octave, note_val)
    
    #Demo the note to the user
    player.note_on(mapping, VOLUME)
    time.sleep(1)
    player.note_off(mapping, VOLUME)
    
    #Tell the user what note was just played
    print("This note was: " + notesB[note_val])
    
def mapNote(octave, note_val):
    mapping = note_mapping[octave + 1][note_val]
    print("Mapping: ", mapping)
    return mapping

#Creates a queue with note_pool's elements in random order
def buildQueue(note_queue, note_pool):
    #print("Incoming queue: ", note_queue)
    #print("Incoming pool: ", note_pool)
    
    #Copy note pool so we can delete from it
    note_pool_copy = copy.copy(note_pool)
    
    #Scramble the note order
    random.shuffle(note_pool_copy)
    
    #Populate queue in random order from note_pool_copy
    for note in note_pool_copy:
        #Add the note to the queue
        note_queue.append(note)
    
    #print("Built Queue: ", note_queue)
    return note_queue
    
    
#Clone the list of notes we want to pick from
base_list = copy.copy(C_MAJ)
#Store the list of notes the player can be quizzed on
note_pool = []
#Ensure the user is requizzed on missed items
note_queue = deque()
#Used to determine when to add new note
round = 0
round_num = 1
#Add the first note to the game
addNote(base_list, note_pool)
input()
buildQueue(note_queue, note_pool)


while True:
    
    note_val = note_queue.popleft()
    mapping = mapNote(octave, note_val)
    
    #Play the note to quiz the user
    player.note_on(mapping, VOLUME)
    time.sleep(1)
    player.note_off(mapping, VOLUME)
    
    #Request the note name from the user
    answer = input("Enter note letter:").upper()
    
    #Check if the user was correct
    if (notesA[answer] == note_val):
        print("Good job Will! You got it!")
        
        #If the player has cleared all of the notes from the current pool...
        if not note_queue:
            round += 1
            print("Round: ", round)
            #Add a new note to the list to make the game harder
            if round == round_num:
                print("Level: ", len(note_pool) + 1)
                addNote(base_list, note_pool)
                round = 0
                round_num += 1
            buildQueue(note_queue, note_pool)
    else:
        print("Sorry, the correct note was " + notesB[note_val])
        #Add the note back to the line to requiz
        note_queue.append(note_val)

    input()
        
del player
pygame.midi.quit()
    