import uuid
from datetime import datetime
import os
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


class ReminderStore:
    COLLECTION_NAME = "reminders"

    def __init__(self):
        self.db = firestore.Client(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            database = 'reminders'
        )

    def get(self, reminder_id: str) -> dict | None:
        """Fetch one reminder by ID. Return None if not found."""
        doc = self.db.collection(self.COLLECTION_NAME).document(reminder_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def create(self, text: str, due_at: str = None, priority: str = None) -> dict:
        """Write a new reminder document. Return the full dict with ID."""
        reminder_id = str(uuid.uuid4())[:8]
        reminder_data = {
            "id": reminder_id,
            "text": text,
            "due_at": due_at,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self.db.collection(self.COLLECTION_NAME).document(reminder_id).set(reminder_data)
        return reminder_data

    def list(self, status: str = "pending", include_unscheduled: bool = False) -> list[dict]:
        """Return a list of reminder dicts matching the status filter."""
        query = self.db.collection(self.COLLECTION_NAME)

        if status and status != "all":
            query = query.where(filter=FieldFilter("status", "==", status))

        if not include_unscheduled:
            query = query.where(filter=FieldFilter("due_at", "!=", None))

        return [doc.to_dict() for doc in query.stream()]

    def delete(self, reminder_id: str) -> dict:
        """Delete a reminder by ID."""
        self.db.collection(self.COLLECTION_NAME).document(reminder_id).delete()
        return {"status": "deleted", "id": reminder_id}

    def update_status(self, reminder_id: str, status: str) -> dict:
        """Update the status of a reminder."""
        self.db.collection(self.COLLECTION_NAME).document(reminder_id).update({
            "status": status,
            "updated_at": datetime.now().isoformat(),
        })
        return {"status": "updated", "id": reminder_id}

    def update_due(self, reminder_id: str, new_due_at: str) -> dict:
        """Update the due date of a reminder."""
        self.db.collection(self.COLLECTION_NAME).document(reminder_id).update({
            "due_at": new_due_at,
            "updated_at": datetime.now().isoformat(),
        })
        return {"status": "updated", "id": reminder_id}

    def update_priority(self, reminder_id: str, priority: str) -> dict:
        """Update the priority of a reminder."""
        self.db.collection(self.COLLECTION_NAME).document(reminder_id).update({
            "priority": priority,
            "updated_at": datetime.now().isoformat(),
        })
        return {"status": "updated", "id": reminder_id}