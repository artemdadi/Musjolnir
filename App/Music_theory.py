from .Notes_info import *

def find_index(array, elem_str):
    for i in range(len(array)):
        for j in array[i]:
            if j == elem_str:
                return i
    else:
        return None
            
class Note:
    
    max_index = len(Rus_notes) - 1
    
    def __init__(self, note, octave):
        if isinstance(note, str):
            self.index = Rus_notes.index(note)
        elif isinstance(note, int):
            self.index = note
        self.octave = octave
        self.name = str(self)
        if self.name in list(Notes_hz.keys()):
            self.hz = Notes_hz[self.name]
        if self.name in list(Notes_files.keys()):
            self.file_name = Notes_files[self.name]
            
    def new_from_interval(self, interval):
        new_octave = self.octave
        new_index = self.index + find_index(Intervals, interval)
        if new_index > self.max_index:
            new_octave += 1
            new_index -= (self.max_index + 1)
        return Note(new_index, new_octave)
            
    def __str__(self):
        return self.str_lang("rus")

    def _str_with_octave(self):
        return self.str_lang("rus") + str(self.octave)
        
    def __repr__(self):
        return str(self)
            
    def str_lang(self, lang):
        if lang == "eng":
            return Eng_notes[self.index]
        elif lang == "rus":
            return Rus_notes[self.index]
            
    def is_sharp(self):
        return self.index in Sharp_notes
            
class Melody:
    
    major = ["Тон", "Тон", "Полутон", "Тон", "Тон", "Тон", "Полутон"]
    
    def __init__(self, notes, scale_type = None, count = 0):
        if scale_type == "major":
            self.notes = [notes]
            for i in self.major:
                self.notes.append(self.notes[-1].new_from_interval(i))
        elif scale_type == "harmonic":
            self.notes = [notes]
            for i in range(count - 1):
                self.notes.append(self.notes[-1].new_from_interval("Полутон"))
        else:
            self.notes = notes
            
    def __str__(self):
        return str(self.notes)
        
    def __len__(self):
        return len(self.notes)

    def str_list(self, no_octave = True):
        result = []
        for note in self.notes:
            str_note = str(note) if no_octave else note._str_with_octave
            result.append(str_note)
        return result
        
    def count_sharps(self):
        count = 0
        for i in self.notes:
            if i.is_sharp():
                count+=1
        return count

if __name__ == "__main__":
    harmonic = Melody(Note("До", 0), "harmonic", 12*9)
    print(harmonic)
