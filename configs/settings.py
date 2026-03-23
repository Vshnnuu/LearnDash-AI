from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "subscriber_churn_snapshot.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.joblib"

TARGET_COL = "churn_label"
ID_COLS = ["subscriber_id"]

CATEGORICAL_COLS = [
    "country",
    "profession_segment",
    "plan_type",
    "payment_method",
]

NUMERIC_COLS = [
    "age",
    "monthly_price_usd",
    "tenure_months",
    "auto_renew_enabled",
    "days_until_renewal",
    "weekly_learning_hours",
    "sessions_per_week",
    "avg_session_duration_minutes",
    "days_since_last_login",
    "courses_started",
    "courses_completed",
    "active_courses_count",
    "avg_course_progress_pct",
    "certificates_earned",
    "quiz_attempts_last_30d",
    "assignment_submissions_last_30d",
    "forum_posts_last_30d",
    "payment_failures_last_6m",
    "refund_requests_last_12m",
    "support_tickets_last_90d",
    "avg_support_resolution_hours",
    "email_open_rate",
    "recommendation_click_rate",
]

FEATURE_COLS = CATEGORICAL_COLS + NUMERIC_COLS

RANDOM_STATE = 42
TEST_SIZE = 0.2
CHURN_THRESHOLD = 0.5