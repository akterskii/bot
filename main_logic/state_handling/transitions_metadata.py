import abc
from abc import ABC
from enum import Enum, auto
from typing import Dict, Optional


class Platform(Enum):
    Telegram = auto()
    Web = auto()
    Android = auto()
    IOS_app = auto()


class TransitionMetadata(ABC):
    @abc.abstractmethod
    def get_service_name(self):
        pass


class TransitionMetadataHandler:
    def __init__(self):
        self.transitions_mapping: Dict[Platform, TransitionMetadata] = {}

    def set_platform_metadata(
            self, platform: Platform, metadata: TransitionMetadata) -> None:
        self.transitions_mapping[platform] = metadata

    def get_platform_metadata(
            self, platform: Platform) -> Optional[TransitionMetadata]:
        return self.transitions_mapping.get(platform)

    def print(self, spacing: int) -> None:
        for platform, metadata in self.transitions_mapping.items():
            space = " " * spacing
            print(space + f'{platform.name}: {metadata}')
