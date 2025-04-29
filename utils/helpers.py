def format_item_display(name, rap, value, trend):
    return f"{name}\nRAP: {rap} | Value: {value} | Trend: {trend}"

def format_diff(current, previous):
    diff = current - previous
    return f"{current} ({'+' if diff >= 0 else ''}{diff})"
