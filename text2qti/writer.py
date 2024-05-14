from abc import abstractmethod
from typing import BinaryIO


class WriterBase(object):
    @abstractmethod
    def write(self, bytes_stream: BinaryIO):
        pass


