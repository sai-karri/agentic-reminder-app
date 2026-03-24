from agent.storage import ReminderStore

storage = ReminderStore()


def create_reminder(text: str, due_at: str = None, priority: str = None):
    """Create a new reminder for the user."""
    if not due_at and priority is None:
        priority = "low"
    reminder = storage.create(text, due_at=due_at, priority=priority)
    return {"status": "created", "id": reminder["id"], "text": text, "due_at": due_at}


def delete_reminder(reminder_id: str):
    """Delete a reminder."""
    reminder = storage.get(reminder_id)
    if not reminder:
        return {"status": "error", "message": f"Reminder {reminder_id} not found."}
    storage.delete(reminder_id)
    return {"status": "deleted", "message":f"Reminder {reminder['text']} has been deleted."}


def complete_reminder(reminder_id: str):
    """Complete a reminder."""
    reminder = storage.get(reminder_id)
    if not reminder:
        return {"status": "error", "message": f"Reminder {reminder_id} not found."}
    storage.update_status(reminder_id, "completed")
    return {"status": "success", "message": f"Reminder {reminder['text']} has been completed."}


def list_reminders(status: str = "pending", include_unscheduled: bool = False):
    """List reminders."""
    reminders = storage.list(status=status, include_unscheduled=include_unscheduled)
    return {"status": "success", "reminders": reminders}

def snooze_reminder(reminder_id: str, new_due_at: str = None):
    reminder = storage.get(reminder_id)
    if not reminder:
        return {"status": "error", "message": f"Reminder {reminder_id} not found."}
    if new_due_at:
        storage.update_due(reminder_id, new_due_at)
    storage.update_status(reminder_id, "snoozed")
    return {"status": "snoozed", "message": f"Reminder {reminder['text']} has been snoozed."}

def update_reminder(reminder_id: str, new_due_at: str = None, priority: str = None):
    reminder = storage.get(reminder_id)
    if not reminder:
        return {"status": "error", "message": f"Reminder {reminder_id} not found."}
    if new_due_at:
        storage.update_due(reminder_id, new_due_at)
    if priority:
        storage.update_priority(reminder_id, priority)
    return {"status": priority or 'updated', "message": f"Reminder {reminder['text']} status updated."}

TOOL_REGISTRY = {
    "create_reminder": create_reminder,
    "list_reminders": list_reminders,
    "complete_reminder": complete_reminder,
    "snooze_reminder": snooze_reminder,
    "delete_reminder": delete_reminder,
    "update_reminder": update_reminder
}

def execute_tool(name: str, args: dict) -> dict:
    if name not in TOOL_REGISTRY:
        return {"status": "error", "message": f"Unknown tool: {name}"}
    try:
        return TOOL_REGISTRY[name](**args)
    except Exception as e:
        print(f"TOOL ERROR: {name} → {type(e).__name__}: {e}")
        return {"status": "error", "message": str(e)}

