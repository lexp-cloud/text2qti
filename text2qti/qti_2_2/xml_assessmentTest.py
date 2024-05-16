# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Gary Clarke
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from typing import List


TEST_START = """\
<?xml version="1.0" encoding="UTF-8"?>
<assessmentTest xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
  xmlns:cc="http://canvas.instructure.com/xsd/cccv1p0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p1.xsd
  identifier="{test_identifier}"
  title="{title}">
  <testPart identifier="{part_identifier}" navigationMode="nonlinear" submissionMode="individual">
    <assessmentSection identifier="{section_identifier}" visible="true" title="Section 1">
"""

ITEM_REF = """\
      <assessmentItemRef identifier="{item_identifier}" href="{item_identifier}.xml" />
"""

TEST_END = """\
  </testPart>
</assessmentTest>
"""


def assessment_test(
    *,
    test_identifier: str,
    part_identifier: str,
    section_identifier: str,
    title_xml: str,
    item_identifiers: List[str],
    # description_html_xml: str,
    # points_possible: Union[int, float],
    # shuffle_answers: str,
    # show_correct_answers: str,
    # one_question_at_a_time: str,
    # cant_go_back: str,
) -> str:
    """
    Generate XML file for assessmentTest element.
    """
    xml = []
    xml.append(
        # TODO: The majority of parameters are not yet implemented.
        TEST_START.format(
            test_identifier=test_identifier,
            part_identifier=part_identifier,
            section_identifier=section_identifier,
            # assignment_group_identifier=assignment_group_identifier,
            title=title_xml,
            # description=description_html_xml,
            # points_possible=points_possible,
            # shuffle_answers=shuffle_answers,
            # show_correct_answers=show_correct_answers,
            # hide_results="always" if show_correct_answers == "false" else "",
            # one_question_at_a_time=one_question_at_a_time,
            # cant_go_back=cant_go_back,
        )
    )
    for item_identifier in item_identifiers:
        xml.append(ITEM_REF.format(item_identifier=item_identifier))
    xml.append(TEST_END)
    return "".join(xml)
