import pickle

class Note:
    """Class representing a single note with title, content, and tags."""

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        """Add a tag to the note."""
        self.tags.append(tag)

class Notes:
    """Class for managing multiple notes."""

    def __init__(self):
        self.notes = {}

    def add_note(self, note):
        """Add a new note."""
        self.notes[note.title] = note

    def find(self, title):
        """Find a note by its title."""
        return self.notes.get(title)

    def find_note(self, keyword):
        """Find notes containing the keyword in their content."""
        return [note for note in self.notes.values() if keyword in note.content]

    def delete_note(self, title):
        """Delete a note by title."""
        if title in self.notes:
            del self.notes[title]
            return True
        return False

    def change_note(self, title, new_content):
        """Change content of an existing note."""
        note = self.find(title)
        if note:
            note.content = new_content
            return True
        return False

    def find_by_tag(self, tag):
        """Find notes containing a specific tag."""
        return [note for note in self.notes.values() if tag in note.tags]

    def save_to_file(self, filename="notes.pkl"):
        """Serialize notes to file."""
        with open(filename, "wb") as f:
            pickle.dump(self.notes, f)

    @classmethod
    def load_from_file(cls, filename="notes.pkl"):
        """Load notes from file."""
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                notes = cls()
                notes.notes = data
                return notes
        except FileNotFoundError:
            return cls()
