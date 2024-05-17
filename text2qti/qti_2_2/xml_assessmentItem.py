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
  {response_declarations}
  {outcome_declarations}
  {item_body}
  {response_processing}
</assessmentItem>
"""

RESPONSE_DECLARATION_CHOICE_SINGLE = """\
<responseDeclaration identifier="RESPONSE" cardinality="single" baseType="identifier">
  <correctResponse>
    {correct_value}
  </correctResponse>
</responseDeclaration>
"""

RESPONSE_DECLARATION_CHOICE_MULTIPLE = """\
<responseDeclaration identifier="RESPONSE" cardinality="multiple" baseType="identifier">
  <correctResponse>
    {correct_values}
  </correctResponse>
  {mapping}
</responseDeclaration>
"""

CORRECT_VALUE = """\
    <value>{correct_choice}</value>
"""

MAPPING = """\
  <mapping defaultValue="0">
    {map_entries}
  </mapping>
"""

MAP_ENTRY = """\
    <mapEntry mapKey="{choice}" mappedValue="{value}"/>
"""

OUTCOME_DECLARATION_CHOICE = """\
<outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
  <defaultValue>
    <value>0</value>
  </defaultValue>
</outcomeDeclaration>
"""
# TODO: The v2 spec allows content independent of the prompt
ITEM_BODY_CHOICE = """\
<itemBody>
  <choiceInteraction responseIdentifier="RESPONSE" shuffle="false" maxChoices="{max_choices}">
    <prompt>{prompt}</prompt>
    {choices}
  </choiceInteraction>
</itemBody>
"""

SIMPLE_CHOICE = """\
<simpleChoice identifier="{identifier}">{text}</simpleChoice>
"""

RESPONSE_PROCESSING_MATCH_CORRECT = """\
<responseProcessing template="http://www.imsglobal.org/question/qti_v2p2/rptemplates/match_correct"/>
"""

RESPONSE_PROCESSING_MAP_RESPONSE = """\
<responseProcessing template="http://www.imsglobal.org/question/qti_v2p2/rptemplates/map_response"/>
"""


def assessment_item(*, quiz: Quiz, question: Question, title: str) -> str:
    """
    Generate XML file for assessmentItem element.
    """
    response_declarations = ""
    outcome_declarations = ""
    item_body = ""
    response_processing = ""

    match question.type:
        case "true_false_question" | "multiple_choice_question":
            response_declarations = RESPONSE_DECLARATION_CHOICE_SINGLE.format(
                correct_value=CORRECT_VALUE.format(
                    correct_choice=question.correct_choices
                )
            )
            outcome_declarations = OUTCOME_DECLARATION_CHOICE
            item_body = ITEM_BODY_CHOICE.format(
                prompt=question.question_html_xml,
                max_choices=1,
                choices="".join(
                    SIMPLE_CHOICE.format(
                        identifier=choice.id, text=choice.choice_html_xml
                    )
                    for choice in question.choices
                ),
            )
            response_processing = RESPONSE_PROCESSING_MATCH_CORRECT
        case "multiple_answers_question":
            response_declarations = RESPONSE_DECLARATION_CHOICE_MULTIPLE.format(
                correct_values="".join(
                    CORRECT_VALUE.format(correct_choice=correct_choice)
                    for correct_choice in question.correct_choices
                ),
                # TODO: This is a placeholder. The mapping should be generated based on the correct choices.
                mapping=MAPPING.format(
                    map_entries="".join(
                        MAP_ENTRY.format(choice=choice.id, value=choice.choice_html_xml)
                        for choice in question.choices
                    )
                ),
            )
            outcome_declarations = OUTCOME_DECLARATION_CHOICE
            item_body = ITEM_BODY_CHOICE.format(
                prompt=question.question_html_xml,
                max_choices=0,
                choices="".join(
                    SIMPLE_CHOICE.format(
                        identifier=choice.id, text=choice.choice_html_xml
                    )
                    for choice in question.choices
                ),
            )
            response_processing = RESPONSE_PROCESSING_MAP_RESPONSE

    return ITEM.format(
        item_identifier=question.id,
        title=title,
        response_declarations=response_declarations,
        outcome_declarations=outcome_declarations,
        item_body=item_body,
        response_processing=response_processing,
    )
