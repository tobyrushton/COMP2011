from datetime import datetime

# calculate how long ago a post was made
def time_ago(value):
    now = datetime.now()
    diff = now - value
    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m  ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    elif seconds < 2592000:
        return f"{int(seconds // 86400)}d ago"
    elif seconds < 31536000:
        return f"{int(seconds // 2592000)}m ago"
    else:
        return f"{int(seconds // 31536000)}y ago"