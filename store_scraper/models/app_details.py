class AppDetails:
    """
    Base class for app details, not related to any specific app store.
    """

    def __init__(
        self,
        name: str,
        version: str,
        downloads: str,
        release_date: str,
        description: str,
    ):
        self.name = name
        self.version = version
        self.downloads = downloads
        self.release_date = release_date
        self.description = description
