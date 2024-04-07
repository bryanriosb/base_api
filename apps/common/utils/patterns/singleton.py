def singleton(cls):
    """This decorator allows you to create a single instance of a class."""
    instances = dict()

    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrap
