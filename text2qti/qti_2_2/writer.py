# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Gary Clarke
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from typing import BinaryIO
import zipfile

from text2qti.writer import WriterBase
from ..quiz import Quiz, Question
from .xml_imsmanifest import imsmanifest
from .xml_assessmentTest import assessment_test
from .xml_assessmentItem import assessment_item


class Writer(WriterBase):
    """
    Create QTI from a Quiz object.
    """

    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        id_base = "text2qti"
        self.manifest_identifier = f"{id_base}_manifest_{quiz.id}"
        self.test_identifier = f"{id_base}_test_{quiz.id}"
        self.part_identifier = f"{id_base}_part_{quiz.id}"
        self.section_identifier = f"{id_base}_section_{quiz.id}"

        self.questions = [
            item for item in quiz.questions_and_delims if isinstance(item, Question)
        ]

        self.question_ids = [item.id for item in self.questions]

        self.imsmanifest_xml = imsmanifest(
            manifest_identifier=self.manifest_identifier,
            test_identifier=self.test_identifier,
            dependency_identifiers=self.question_ids,
            # images=self.quiz.images, # TODO: Where do images fit in?
        )
        self.assessment_test = assessment_test(
            test_identifier=self.test_identifier,
            part_identifier=self.part_identifier,
            section_identifier=self.section_identifier,
            title_xml=quiz.title_xml,
            item_identifiers=self.question_ids,
            # description_html_xml=quiz.description_html_xml,
            # points_possible=quiz.points_possible,
            # shuffle_answers=quiz.shuffle_answers_xml,
            # show_correct_answers=quiz.show_correct_answers_xml,
            # one_question_at_a_time=quiz.one_question_at_a_time_xml,
            # cant_go_back=quiz.cant_go_back_xml,
        )
        self.assessment_items = []
        for i, question in enumerate(self.questions):
            self.assessment_items.append(
                assessment_item(
                    quiz=self.quiz, question=question, title=f"Question {i}"
                )
            )

    def write(self, bytes_stream: BinaryIO):
        with zipfile.ZipFile(bytes_stream, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("imsmanifest.xml", self.imsmanifest_xml)
            # zf.writestr(zipfile.ZipInfo("non_cc_assessments/"), b"")
            zf.writestr(
                f"{self.test_identifier}.xml",
                self.assessment_test,
            )
            # for image in self.quiz.images.values():
            #     zf.writestr(image.qti_zip_path, image.data)
