from .models import ExchangeRate


def course_determinant(num: str, den: str):

    course = ExchangeRate.objects.filter(
        currency_numerator__name=num,
        currency_denominator__name=den).first()

    return course
