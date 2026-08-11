import logging
import re


logger = logging.getLogger(__name__)


def human_order_sorted(l):
    """Sorts string in human order (i.e. 'stat10' will go after 'stat2')"""

    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        if isinstance(text, tuple):
            text = text[0]
        return [atoi(c) for c in re.split(r"(\d+)", text)]

    return sorted(l, key=natural_keys)
