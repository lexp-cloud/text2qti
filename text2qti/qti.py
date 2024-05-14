# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Geoffrey M. Poore
# Copyright (c) 2024, Gary Clarke
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import io
import pathlib
from typing import Union
from .quiz import Quiz
from .qti_1_2.writer import Writer as Writer_1_2


class QTI(object):
    '''
    Create QTI from a Quiz object.
    '''
    def __init__(self, quiz: Quiz, version: str = '1.2'):
        match version:
            case '1.2':
                self.writer = Writer_1_2(quiz)
            case '2.2':
                raise NotImplementedError
            case _:
                raise ValueError(f'Unsupported QTI version: {self.version}')

    def zip_bytes(self) -> bytes:
        stream = io.BytesIO()
        self.writer.write(stream)
        return stream.getvalue()

    def save(self, qti_path: Union[str, pathlib.Path]):
        if isinstance(qti_path, str):
            qti_path = pathlib.Path(qti_path)
        elif not isinstance(qti_path, pathlib.Path):
            raise TypeError
        qti_path.write_bytes(self.zip_bytes())
