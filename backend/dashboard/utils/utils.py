def humanize_bytes(value_in_bytes):
    value_in_bytes = float(value_in_bytes)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while value_in_bytes >= 1024 and index < len(units) - 1:
        value_in_bytes /= 1024
        index += 1
    return f"{value_in_bytes:.2f} {units[index]}"
