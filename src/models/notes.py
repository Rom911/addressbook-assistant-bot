class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

class NoteBook:
    def __init__(self):
        self.notes = {}

    def add_note(self, note):
        self.notes[note.title] = note

    def find_note(self, keyword):
        return [note for note in self.notes.values() if keyword in note.content]

    def find_by_tag(self, tag):
        return [note for note in self.notes.values() if tag in note.tags]
