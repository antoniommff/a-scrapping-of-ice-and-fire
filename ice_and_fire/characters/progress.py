progress = {"current": 0, "total": 0, "message": ""}


def update_progress(current, total, message):
    global progress
    progress["current"] = current
    progress["total"] = total
    progress["message"] = message


def get_progress():
    global progress
    return progress
