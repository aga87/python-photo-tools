import shutil
from typing import Iterable

from photo_tools.exceptions import MissingDependencyError

DEPENDENCY_REGISTRY: dict[str, list[str]] = {
    "exif": ["exiftool"],
}


def check_dependencies(required: Iterable[str]) -> None:
    for dependency in required:
        if not shutil.which(dependency):
            raise MissingDependencyError(dependency)


def validate_feature(feature: str) -> None:
    dependencies = DEPENDENCY_REGISTRY.get(feature, [])
    check_dependencies(dependencies)
