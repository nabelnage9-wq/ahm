from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.exams.views import (
    DashboardSummaryView,
    StudentCreateUpdateView,
    ExcelImportPreviewView,
    ExcelImportCommitView,
    GradeUpdateWithHistoryView,
    ApproveExamView,
    StudentPortalLoginView,
    StudentPortalProfileView,
    PublicTop10View,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/dashboard/summary/", DashboardSummaryView.as_view()),
    path("api/v1/students/", StudentCreateUpdateView.as_view()),
    path("api/v1/exams/<uuid:exam_id>/approve/", ApproveExamView.as_view()),
    path("api/v1/grades/<uuid:result_id>/update-history/", GradeUpdateWithHistoryView.as_view()),
    path("api/v1/import/excel/preview/", ExcelImportPreviewView.as_view()),
    path("api/v1/import/excel/commit/", ExcelImportCommitView.as_view()),
    path("api/v1/student-portal/login/", StudentPortalLoginView.as_view()),
    path("api/v1/student-portal/me/", StudentPortalProfileView.as_view()),
    path("api/v1/public/top-10/", PublicTop10View.as_view()),
]
