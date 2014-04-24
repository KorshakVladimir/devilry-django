from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def devilry_student_shortgrade(feedback):
    """
    Takes a :class:`devilry.apps.models.StaticFeedback` and renders it as a
    short oneliner that includes the grade and information about if the grade is
    passed or failed.

    Handles the grades ``Passed`` and ``Failed`` as synonyms for
    ``is_passing_grade``, so we only render a translation of ``Passed`` or
    ``Failed``, instead of both ``is_passing_grade`` and ``Grade``. This avoids
    ugly strings like: ``Passed (Passed)``.
    """
    return render_to_string('devilry_student/devilry_student_shortgrade_tag.django.html', {
        'feedback': feedback,
        'ispassedfailed': feedback.grade == 'Passed' or feedback.grade == 'Failed'
    })