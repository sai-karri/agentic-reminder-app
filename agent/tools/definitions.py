
CREATE_REMINDER = {
    "name": "create_reminder",
    "description": (
        "Create a new reminder for the user. Use this when the user wants "
        "to be reminded about something. If the user specifies a time, "
        "you MUST also set a priority. If they don't specify priority, "
        "default to LOW. If no time is given, ask them when."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "What to remind about"},
            "due_at": {
                "type": "string", 
                "description": "When to fire, ISO 8601 and Covert relative times like 'in 2 hours' to absolute times."
            },
            "priority": {
                "type": "string", 
                "enum": ["high", "medium", "low", "None"],
                "description": "Priority level. Default to None if not specified."
            },
        },
        "required": ["text"]
    }
}

DELETE_REMINDER = {
    "name": "delete_reminder",
    "description": (
        "Permanently delete a reminder. Use this only when the user "
        "explicitly wants to remove a reminder, not just mark it done. "
        "Ask for confirmation if the intent is unclear. Requires the "
        "reminder's ID — call list_reminders first if needed."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "reminder_id": {
                "type": "string",
                "description": "The ID of the reminder to delete."
            },
        },
        "required": ["reminder_id"]
    }
}

COMPLETE_REMINDER = {
    "name": "complete_reminder",
    "description": (
        "Mark a reminder as completed. Use this when the user says they've "
        "done something or want to dismiss a reminder. Requires the reminder's "
        "ID — if the user describes it by text, call list_reminders first "
        "to find the matching ID."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "reminder_id": {
                "type": "string",
                "description": "The ID of the reminder to complete."
            },
        },
        "required": ["reminder_id"]
    }
}

LIST_REMINDERS = {
    "name": "list_reminders",
    "description": (
        "List the user's reminders. Use this when the user asks to see "
        "their reminders, or when you need to look up a reminder's ID "
        "before completing, snoozing, or deleting it. By default, only "
        "show reminders that have a due date and priority assigned. "
        "Set include_unscheduled to true to also show reminders without "
        "a due date."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["pending", "completed", "snoozed", "all"],
                "description": "Filter by status. Default to 'pending'."
            },
            "include_unscheduled": {
                "type": "boolean",
                "description": "If true, also show reminders with no due date. Default false."
            },
        },
        "required": []
    }
}

SNOOZE_REMINDER = {
    "name": "snooze_reminder",
    "description": (
        "Postpone a reminder to a later time. Use this when the user wants "
        "to delay a reminder. Requires the reminder's ID — call list_reminders "
        "first if needed."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "reminder_id": {
                "type": "string",
                "description": "The ID of the reminder to snooze."
            },
            "new_due_at": {
                "type": "string",
                "description": "The new time in ISO 8601 format. Omit to snooze with no specific due date."
            },
        },
        "required": ["reminder_id"]
    }
}

UPDATE_REMINDER = {
    "name": "update_reminder",
    "description": (
        "Update an existing reminder's due date or priority. Use this when "
        "the user wants to change when a reminder is due or change its "
        "priority level. Requires the reminder's ID — call list_reminders "
        "first if needed."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "reminder_id": {
                "type": "string",
                "description": "The ID of the reminder to update."
            },
            "new_due_at": {
                "type": "string",
                "description": "The new due date/time in ISO 8601 format. Omit if not changing."
            },
            "priority": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "The new priority level. Omit if not changing."
            },
        },
        "required": ["reminder_id"]
    }
}

ALL_TOOLS = [
    CREATE_REMINDER,
    LIST_REMINDERS,
    COMPLETE_REMINDER,
    SNOOZE_REMINDER,
    DELETE_REMINDER,
    UPDATE_REMINDER,
]