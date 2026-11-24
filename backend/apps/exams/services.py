from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password
from .models import ExamResult, TopStudent
from apps.academic.models import Student


def hash_pin(pin: str) -> str:
    return make_password(str(pin).strip())


def verify_pin(raw_pin: str, pin_hash: str) -> bool:
    return check_password(str(raw_pin).strip(), pin_hash)


def get_grade_label(percentage: Decimal, thresholds: list | None = None) -> str:
    pct = float(percentage)
    rules = thresholds or [
        {"min": 90, "ar": "ممتاز", "en": "Excellent"},
        {"min": 80, "ar": "جيد جدًا", "en": "Very Good"},
        {"min": 65, "ar": "جيد", "en": "Good"},
        {"min": 50, "ar": "مقبول", "en": "Pass"},
        {"min": 0, "ar": "يحتاج إلى تحسين", "en": "Needs Improvement"},
    ]
    for rule in sorted(rules, key=lambda x: x["min"], reverse=True):
        if pct >= float(rule["min"]):
            return rule["ar"]
    return "يحتاج إلى تحسين"


def calculate_student_cumulative(student_id, academic_year_id=None, term_id=None, subject_id=None):
    filters = {
        "student_id": student_id,
        "exam__status": "approved",
        "is_absent": False,
    }
    if academic_year_id:
        filters["exam__academic_year_id"] = academic_year_id
    if term_id:
        filters["exam__term_id"] = term_id
    if subject_id:
        filters["exam__subject_id"] = subject_id

    qs = ExamResult.objects.filter(**filters).select_related("exam")
    agg = qs.aggregate(
        total_score=Sum("score"),
        total_max_score=Sum("exam__max_score"),
    )

    total_score = agg["total_score"] or Decimal("0.00")
    total_max_score = agg["total_max_score"] or Decimal("0.00")
    percentage = (
        round((total_score / total_max_score) * Decimal("100.00"), 2)
        if total_max_score > 0
        else Decimal("0.00")
    )

    exams_list = [
        {
            "exam_id": str(r.exam.id),
            "title": r.exam.title,
            "exam_type": r.exam.exam_type,
            "subject": r.exam.subject.name_ar,
            "term": r.exam.term.name_ar,
            "exam_date": r.exam.exam_date.isoformat(),
            "score": float(r.score),
            "max_score": float(r.exam.max_score),
            "pass_score": float(r.exam.pass_score),
            "percentage": float(r.percentage),
            "passed": r.score >= r.exam.pass_score,
        }
        for r in qs.order_by("exam__exam_date")
    ]

    return {
        "total_score": float(total_score),
        "total_max_score": float(total_max_score),
        "cumulative_percentage": float(percentage),
        "grade_label": get_grade_label(percentage),
        "exams_count": len(exams_list),
        "exams": exams_list,
    }


def rebuild_top_10(academic_year_id, group_id=None, term_id=None, subject_id=None):
    students_qs = Student.objects.filter(status="active")
    if academic_year_id:
        students_qs = students_qs.filter(academic_year_id=academic_year_id)
    if group_id:
        students_qs = students_qs.filter(group_id=group_id)

    ranked_candidates = []
    for st in students_qs:
        stats = calculate_student_cumulative(
            st.id,
            academic_year_id=academic_year_id,
            term_id=term_id,
            subject_id=subject_id,
        )
        if stats["exams_count"] > 0:
            ranked_candidates.append((st, Decimal(str(stats["cumulative_percentage"]))))

    ranked_candidates.sort(key=lambda item: (-item[1], item[0].serial_number))

    TopStudent.objects.filter(
        academic_year_id=academic_year_id,
        group_id=group_id,
        term_id=term_id,
        subject_id=subject_id,
    ).delete()

    rank = 0
    prev_pct = None
    for idx, (student, pct) in enumerate(ranked_candidates):
        if pct != prev_pct:
            rank = idx + 1
            prev_pct = pct
        if rank > 10:
            break
        TopStudent.objects.create(
            academic_year_id=academic_year_id,
            group_id=group_id,
            term_id=term_id,
            subject_id=subject_id,
            student=student,
            rank=rank,
            cumulative_percentage=pct,
        )
