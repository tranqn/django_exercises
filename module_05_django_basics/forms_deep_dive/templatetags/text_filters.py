from django import template

register = template.Library()


@register.filter(name="truncate_chars")
def truncate_chars(value, length):
    """Truncate string to given length with ellipsis."""
    if len(str(value)) <= length:
        return value
    return str(value)[:length] + "..."


@register.filter(name="reading_time")
def reading_time(text, wpm=200):
    """Estimate reading time in minutes."""
    word_count = len(str(text).split())
    minutes = max(1, round(word_count / wpm))
    return f"{minutes} min read"