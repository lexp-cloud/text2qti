# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Gary Clarke
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from abc import abstractmethod
from typing import BinaryIO


class WriterBase(object):
    @abstractmethod
    def write(self, bytes_stream: BinaryIO):
        pass
