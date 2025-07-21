import pickle
from typing import List, Dict, Optional

class Note:
    """Class representing a single note with title, content, and tags."""

    def __init__(self, title: str, content: str):
        self.title: str = title
        self.content: str = content
        self.tags: List[str] = []

    def add_tag(self, tag: str) -> None:
        """Add a unique tag to the note."""
        if tag not in self.tags:
            self.tags.append(tag)

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags)
        return f"[{self.title}] {self.content} (Tags: {tags_str})"


class Notes:
    """Class for managing multiple notes."""

    def __init__(self):
        self.notes: Dict[str, Note] = {}

    def add_note(self, note: Note) -> None:
        """Add a new note."""
        self.notes[note.title] = note

    def find(self, title: str) -> Optional[Note]:
        """Find a note by its title."""
        return self.notes.get(title)

    def find_note(self, keyword: str) -> List[Note]:
        """Find notes containing the keyword in their content (case insensitive)."""
        keyword_lower = keyword.lower()
        return [note for note in self.notes.values() if keyword_lower in note.content.lower()]

    def delete_note(self, title: str) -> bool:
        """Delete a note by title."""
        if title in self.notes:
            del self.notes[title]
            return True
        return False

    def change_note(self, title: str, new_content: str) -> bool:
        """Change content of an existing note."""
        note = self.find(title)
        if note:
            note.content = new_content
            return True
        return False

    def find_by_tag(self, tag: str) -> List[Note]:
        """Find notes containing a specific tag."""
        return [note for note in self.notes.values() if tag in note.tags]

    def save_to_file(self, filename: str = "notes.pkl") -> None:
        """Serialize notes to file."""
        with open(filename, "wb") as f:
            pickle.dump(self.notes, f)

    @classmethod
    def load_from_file(cls, filename: str = "notes.pkl") -> "Notes":
        """Load notes from file."""
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                notes = cls()
                notes.notes = data
                return notes
        except FileNotFoundError:
            return cls()
