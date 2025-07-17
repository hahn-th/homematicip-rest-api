class HomeNotInitializedError(Exception):
    """
    Raised when the Home instance is not initialized.

    :param message: Error message
    """

    def __init__(self, message="Home not initialized. Run init() first."):
        super().__init__(message)
