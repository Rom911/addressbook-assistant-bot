from datetime import datetime


class Note:
    def __init__(self, note_id, text, tags=[]):
        self.id = note_id
        self.text = text
        self.tags = tags
        self.created_at = datetime.now()

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def edit(self, new_text):
        self.text = new_text


class NotesBook:
    def __init__(self):
        self.notes = {}

    def add_note(self, note):
        self.notes[note.id] = note

    def delete_note(self, note_id):
        if note_id in self.notes:
            del self.notes[note_id]

    def find_note_by_text(self, text):
        return [n for n in self.notes.values() if text in n.text]

    def find_by_tag(self, tag):
        return [n for n in self.notes.values() if tag in n.tags]
