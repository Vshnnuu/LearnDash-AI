from __future__ import annotations

import gradio as gr

from configs.settings import MODEL_PATH
from src.inference import load_model, predict_one

model = None


def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    return model


def run_prediction(
    age,
    country,
    profession_segment,
    plan_type,
    monthly_price_usd,
    tenure_months,
    auto_renew_enabled,
    days_until_renewal,
    payment_method,
    weekly_learning_hours,
    sessions_per_week,
    avg_session_duration_minutes,
    days_since_last_login,
    courses_started,
    courses_completed,
    active_courses_count,
    avg_course_progress_pct,
    certificates_earned,
    quiz_attempts_last_30d,
    assignment_submissions_last_30d,
    forum_posts_last_30d,
    payment_failures_last_6m,
    refund_requests_last_12m,
    support_tickets_last_90d,
    avg_support_resolution_hours,
    email_open_rate,
    recommendation_click_rate,
):
    payload = {
        "age": int(age),
        "country": country,
        "profession_segment": profession_segment,
        "plan_type": plan_type,
        "monthly_price_usd": float(monthly_price_usd),
        "tenure_months": int(tenure_months),
        "auto_renew_enabled": 1 if auto_renew_enabled == "Yes" else 0,
        "days_until_renewal": int(days_until_renewal),
        "payment_method": payment_method,
        "weekly_learning_hours": float(weekly_learning_hours),
        "sessions_per_week": int(sessions_per_week),
        "avg_session_duration_minutes": float(avg_session_duration_minutes),
        "days_since_last_login": int(days_since_last_login),
        "courses_started": int(courses_started),
        "courses_completed": int(courses_completed),
        "active_courses_count": int(active_courses_count),
        "avg_course_progress_pct": float(avg_course_progress_pct),
        "certificates_earned": int(certificates_earned),
        "quiz_attempts_last_30d": int(quiz_attempts_last_30d),
        "assignment_submissions_last_30d": int(assignment_submissions_last_30d),
        "forum_posts_last_30d": int(forum_posts_last_30d),
        "payment_failures_last_6m": int(payment_failures_last_6m),
        "refund_requests_last_12m": int(refund_requests_last_12m),
        "support_tickets_last_90d": int(support_tickets_last_90d),
        "avg_support_resolution_hours": float(avg_support_resolution_hours),
        "email_open_rate": float(email_open_rate),
        "recommendation_click_rate": float(recommendation_click_rate),
    }

    result = predict_one(get_model(), payload)

    summary = (
        f"Churn probability: {result['churn_probability']:.2%}\n"
        f"Predicted label: {'Likely to churn' if result['prediction'] == 1 else 'Likely to stay'}\n"
        f"Risk level: {result['risk_level']}"
    )

    drivers = "\n".join(f"- {item}" for item in result["churn_drivers"])
    if not drivers:
        drivers = "- No major churn drivers detected."

    actions = "\n".join(f"- {item}" for item in result["recommended_actions"])

    strategy_report = (
        f"Detected churn drivers:\n{drivers}\n\n"
        f"Retention strategy:\n{actions}"
    )

    crm_lines = "\n".join(f"✅ {item}" for item in result["crm_actions"])
    crm_report = (
        "Execution mode: Simulated CRM workflow\n\n"
        f"{crm_lines}"
    )

    return summary, strategy_report, crm_report


with gr.Blocks(title="Learner Retention AI") as demo:
    gr.Markdown(
        """
        # LearnDash AI – AI Churn Prediction & Retention Agent
        Predicts a learner's unsubscription risk for an online learning platform and displays recommended retention and intervention actions.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            with gr.Tabs():
                with gr.Tab("Learner Profile"):
                    age = gr.Slider(18, 65, value=30, step=1, label="Age")
                    country = gr.Dropdown(
                        ["India", "Germany", "USA", "UK", "Canada", "Brazil"],
                        value="India",
                        label="Country",
                    )
                    profession_segment = gr.Dropdown(
                        [
                            "student",
                            "software_engineer",
                            "data_analyst",
                            "marketing",
                            "designer",
                            "finance",
                            "teacher",
                            "job_seeker",
                            "other",
                        ],
                        value="student",
                        label="Profession Segment",
                    )

                with gr.Tab("Subscription"):
                    plan_type = gr.Dropdown(
                        ["basic", "standard", "premium"],
                        value="standard",
                        label="Plan Type",
                    )
                    monthly_price_usd = gr.Slider(
                        9.99, 59.99, value=24.99, step=0.01, label="Monthly Price (USD)"
                    )
                    tenure_months = gr.Slider(1, 48, value=8, step=1, label="Tenure (Months)")
                    auto_renew_enabled = gr.Radio(
                        ["No", "Yes"], value="Yes", label="Auto Renew Enabled"
                    )
                    days_until_renewal = gr.Slider(
                        0, 30, value=15, step=1, label="Days Until Renewal"
                    )
                    payment_method = gr.Dropdown(
                        ["credit_card", "paypal", "debit_card", "upi", "bank_transfer"],
                        value="credit_card",
                        label="Payment Method",
                    )

                with gr.Tab("Learning Activity"):
                    weekly_learning_hours = gr.Slider(
                        0, 20, value=4.0, step=0.1, label="Weekly Learning Hours"
                    )
                    sessions_per_week = gr.Slider(
                        0, 14, value=3, step=1, label="Sessions Per Week"
                    )
                    avg_session_duration_minutes = gr.Slider(
                        5, 120, value=35, step=0.1, label="Average Session Duration (Minutes)"
                    )
                    courses_started = gr.Slider(0, 15, value=2, step=1, label="Courses Started")
                    courses_completed = gr.Slider(
                        0, 10, value=1, step=1, label="Courses Completed"
                    )
                    active_courses_count = gr.Slider(
                        0, 6, value=1, step=1, label="Active Courses Count"
                    )
                    avg_course_progress_pct = gr.Slider(
                        0, 100, value=35, step=0.1, label="Average Course Progress (%)"
                    )
                    certificates_earned = gr.Slider(
                        0, 8, value=0, step=1, label="Certificates Earned"
                    )

                with gr.Tab("Engagement & Support"):
                    days_since_last_login = gr.Slider(
                        0, 45, value=5, step=1, label="Days Since Last Login"
                    )
                    quiz_attempts_last_30d = gr.Slider(
                        0, 40, value=4, step=1, label="Quiz Attempts in Last 30 Days"
                    )
                    assignment_submissions_last_30d = gr.Slider(
                        0, 20, value=1, step=1, label="Assignment Submissions in Last 30 Days"
                    )
                    forum_posts_last_30d = gr.Slider(
                        0, 15, value=0, step=1, label="Forum Posts in Last 30 Days"
                    )
                    support_tickets_last_90d = gr.Slider(
                        0, 8, value=0, step=1, label="Support Tickets in Last 90 Days"
                    )
                    avg_support_resolution_hours = gr.Slider(
                        1, 120, value=6, step=0.1, label="Average Support Resolution Hours"
                    )

                with gr.Tab("Billing & Marketing"):
                    payment_failures_last_6m = gr.Slider(
                        0, 4, value=0, step=1, label="Payment Failures in Last 6 Months"
                    )
                    refund_requests_last_12m = gr.Slider(
                        0, 2, value=0, step=1, label="Refund Requests in Last 12 Months"
                    )
                    email_open_rate = gr.Slider(
                        0, 1, value=0.4, step=0.01, label="Email Open Rate"
                    )
                    recommendation_click_rate = gr.Slider(
                        0, 1, value=0.3, step=0.01, label="Recommendation Click Rate"
                    )

            submit_btn = gr.Button("Predict Retention Risk", variant="primary")

        with gr.Column(scale=2):
            summary_output = gr.Textbox(label="Prediction Summary", lines=6)
            strategy_output = gr.Textbox(label="Retention Strategy", lines=14)
            crm_output = gr.Textbox(label="CRM Execution Status", lines=10)

    submit_btn.click(
        fn=run_prediction,
        inputs=[
            age,
            country,
            profession_segment,
            plan_type,
            monthly_price_usd,
            tenure_months,
            auto_renew_enabled,
            days_until_renewal,
            payment_method,
            weekly_learning_hours,
            sessions_per_week,
            avg_session_duration_minutes,
            days_since_last_login,
            courses_started,
            courses_completed,
            active_courses_count,
            avg_course_progress_pct,
            certificates_earned,
            quiz_attempts_last_30d,
            assignment_submissions_last_30d,
            forum_posts_last_30d,
            payment_failures_last_6m,
            refund_requests_last_12m,
            support_tickets_last_90d,
            avg_support_resolution_hours,
            email_open_rate,
            recommendation_click_rate,
        ],
        outputs=[summary_output, strategy_output, crm_output],
    )


if __name__ == "__main__":
    demo.launch()