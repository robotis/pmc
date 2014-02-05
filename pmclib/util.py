import collections

def flatten(lst):
    """Flatten list.
    Args:
    lst (list): List to flatten
    Returns:
    generator
    """
    for elm in lst:
        if isinstance(elm, collections.Iterable) and not isinstance(elm, str):
            for sub in flatten(elm):
                yield sub
        else:
            yield elm