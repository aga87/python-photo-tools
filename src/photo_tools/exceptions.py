class PhotoToolsError(Exception):
    """Base exception for the project."""
    pass

class MissingDependencyError(PhotoToolsError):
    def __init__(self, dependency: str):
        self.dependency = dependency

    def __str__(self) -> str:
        import platform

        system = platform.system()

        if system == "Darwin":
            install_hint = f"brew install {self.dependency}"
        elif system == "Linux":
            install_hint = f"sudo apt install {self.dependency}"
        else:
            install_hint = "See installation instructions: https://exiftool.org/"

        return (
            f"{self.dependency} is required but not installed.\n\n"
            f"Install it using:\n  {install_hint}"
        )