

class PinggyNativeLoaderError(Exception):
    pass

class PinggyRemovedPropertyError(AttributeError):
    """Raised when accessing a removed property."""
    pass