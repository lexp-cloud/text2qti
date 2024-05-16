# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Gary Clarke
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from text2qti.quiz import Question, Quiz


ITEM = """\
<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p1.xsd
                      http://www.w3.org/1998/Math/MathML http://www.w3.org/Math/XMLSchema/mathml2/mathml2.xsd"
  identifier="{item_identifier}"
  title="{title}"
  adaptive="false"
  timeDependent="false">
  {responseDeclarations}
  {outcomeDeclarations}
  {itemBody}
  {responseProcessing}
</assessmentItem>
"""


def assessment_item(*, quiz: Quiz, question: Question, title: str) -> str:
    """
    Generate XML file for assessmentItem element.
    """
    responseDeclarations = ""
    outcomeDeclarations = ""
    itemBody = ""
    responseProcessing = ""

    return ITEM.format(
        item_identifier=question.id,
        title=title,
        responseDeclarations=responseDeclarations,
        outcomeDeclarations=outcomeDeclarations,
        itemBody=itemBody,
        responseProcessing=responseProcessing,
    )
