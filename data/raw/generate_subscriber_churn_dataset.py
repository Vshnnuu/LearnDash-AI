
import numpy as np
import pandas as pd

def generate_subscriber_churn_snapshot(n_rows=5000, seed=42, output_path="subscriber_churn_snapshot.csv"):
    np.random.seed(seed)

    countries = ["India","Germany","USA","UK","Canada","Brazil"]
    country_probs = np.array([0.28,0.16,0.22,0.12,0.10,0.12])

    professions = ["student","software_engineer","data_analyst","marketing","designer","finance","teacher","job_seeker","other"]
    profession_probs = np.array([0.18,0.16,0.10,0.10,0.08,0.08,0.10,0.10,0.10])

    plans = ["basic","standard","premium"]
    plan_probs = np.array([0.42,0.38,0.20])

    payment_methods = ["credit_card","paypal","debit_card","upi","bank_transfer"]

    subscriber_id = [f"SUB_{i:06d}" for i in range(1, n_rows + 1)]
    country = np.random.choice(countries, size=n_rows, p=country_probs)
    profession = np.random.choice(professions, size=n_rows, p=profession_probs)

    age = []
    for prof in profession:
        if prof == "student":
            a = int(np.clip(np.random.normal(23, 3), 18, 30))
        elif prof == "job_seeker":
            a = int(np.clip(np.random.normal(28, 6), 18, 45))
        elif prof in ["software_engineer", "data_analyst", "designer", "marketing", "finance", "teacher"]:
            a = int(np.clip(np.random.normal(34, 8), 21, 60))
        else:
            a = int(np.clip(np.random.normal(36, 10), 18, 65))
        age.append(a)
    age = np.array(age)

    plan_type = np.random.choice(plans, size=n_rows, p=plan_probs)

    monthly_price = np.zeros(n_rows)
    for i, p in enumerate(plan_type):
        if p == "basic":
            monthly_price[i] = np.round(np.random.uniform(9.99, 14.99), 2)
        elif p == "standard":
            monthly_price[i] = np.round(np.random.uniform(19.99, 29.99), 2)
        else:
            monthly_price[i] = np.round(np.random.uniform(39.99, 59.99), 2)

    tenure = np.clip((np.random.gamma(shape=2.2, scale=6.0, size=n_rows)).astype(int) + 1, 1, 48)

    auto_renew_prob = (
        0.45
        + 0.01 * np.minimum(tenure, 20)
        + np.where(plan_type == "premium", 0.12, np.where(plan_type == "standard", 0.05, 0.0))
    )
    auto_renew_enabled = (np.random.rand(n_rows) < np.clip(auto_renew_prob, 0.25, 0.92)).astype(int)

    days_until_renewal = np.random.randint(0, 31, size=n_rows)

    payment_method = []
    for c in country:
        if c == "India":
            probs = [0.22, 0.08, 0.18, 0.45, 0.07]
        elif c in ["Germany", "UK"]:
            probs = [0.35, 0.25, 0.18, 0.02, 0.20]
        elif c in ["USA", "Canada"]:
            probs = [0.45, 0.28, 0.18, 0.01, 0.08]
        else:
            probs = [0.28, 0.18, 0.22, 0.12, 0.20]
        payment_method.append(np.random.choice(payment_methods, p=probs))
    payment_method = np.array(payment_method)

    prof_eng = {
        "student": 0.15,
        "software_engineer": 0.25,
        "data_analyst": 0.22,
        "marketing": 0.05,
        "designer": 0.08,
        "finance": 0.00,
        "teacher": 0.10,
        "job_seeker": 0.18,
        "other": 0.00,
    }
    plan_eng = {"basic": -0.08, "standard": 0.02, "premium": 0.14}

    engagement = (
        np.array([prof_eng[p] for p in profession])
        + np.array([plan_eng[p] for p in plan_type])
        + np.clip((tenure - 6) / 30, -0.12, 0.18)
        + np.random.normal(0, 0.35, n_rows)
    )
    engagement = np.clip(engagement, -1.1, 1.4)

    weekly_learning_hours = np.clip(np.random.normal(4.8 + 4.2 * engagement, 2.3, n_rows), 0, 20)
    sessions_per_week = np.clip(np.round(np.random.normal(3.8 + 2.4 * engagement, 1.6, n_rows)), 0, 14).astype(int)
    avg_session_duration_minutes = np.clip(np.random.normal(42 + 16 * engagement, 15, n_rows), 5, 120)
    days_since_last_login = np.clip(
        np.round(np.random.gamma(shape=1.6, scale=4.5, size=n_rows) + 9 - 7 * engagement - 0.15 * sessions_per_week),
        0,
        45,
    ).astype(int)

    courses_started = np.clip(
        np.round(np.random.normal(2.2 + 2.0 * np.maximum(engagement, -0.2) + 0.04 * tenure, 1.8, n_rows)),
        0,
        15,
    ).astype(int)

    completion_rate = np.clip(0.12 + 0.22 * np.maximum(engagement, -0.3) + np.random.normal(0.12, 0.12, n_rows), 0, 0.95)
    courses_completed = np.minimum(courses_started, np.clip(np.round(courses_started * completion_rate), 0, 10).astype(int))

    active_courses_count = np.clip(
        courses_started - courses_completed + np.round(np.random.normal(0.2, 0.8, n_rows)),
        0,
        6,
    ).astype(int)

    avg_course_progress_pct = np.clip(
        np.random.normal(22 + 28 * np.maximum(engagement, -0.3) + 6 * active_courses_count + 4 * courses_completed, 14, n_rows),
        0,
        100,
    )

    certificates_earned = np.minimum(
        courses_completed,
        np.clip(np.round(courses_completed * np.random.uniform(0.3, 0.9, n_rows) + np.random.normal(0, 0.6, n_rows)), 0, 8).astype(int),
    )

    quiz_attempts_last_30d = np.clip(
        np.round(np.random.normal(2 + 2.0 * active_courses_count + 0.9 * courses_started + 2.0 * np.maximum(engagement, 0), 4.5, n_rows)),
        0,
        40,
    ).astype(int)

    assignment_submissions_last_30d = np.clip(
        np.round(np.random.normal(0.6 + 1.3 * active_courses_count + 0.7 * courses_completed + 1.0 * np.maximum(engagement, 0), 2.5, n_rows)),
        0,
        20,
    ).astype(int)

    forum_posts_last_30d = np.clip(
        np.round(np.random.normal(0.3 + 0.3 * active_courses_count + 0.7 * np.maximum(engagement, 0), 1.5, n_rows)),
        0,
        15,
    ).astype(int)

    payment_failures_last_6m = np.zeros(n_rows, dtype=int)
    for i in range(n_rows):
        base = 0.05
        if payment_method[i] in ["bank_transfer", "debit_card"]:
            base += 0.04
        if payment_method[i] == "upi":
            base += 0.02
        if auto_renew_enabled[i] == 0:
            base += 0.01
        lam = np.clip(base + 0.01 * (monthly_price[i] > 35), 0.02, 0.16)
        payment_failures_last_6m[i] = min(np.random.poisson(lam * 2.0), 4)

    refund_requests_last_12m = np.zeros(n_rows, dtype=int)
    for i in range(n_rows):
        dissatisfaction = max(0, 0.16 - 0.015 * weekly_learning_hours[i] + 0.018 * payment_failures_last_6m[i] + 0.012 * days_since_last_login[i] / 10)
        refund_requests_last_12m[i] = np.random.binomial(2, np.clip(dissatisfaction, 0.01, 0.22))

    support_tickets_last_90d = np.clip(
        np.round(
            np.random.normal(
                0.6 + 0.7 * payment_failures_last_6m + 1.1 * refund_requests_last_12m + 0.05 * (days_since_last_login > 20) - 0.05 * np.maximum(engagement, 0),
                1.2,
                n_rows,
            )
        ),
        0,
        8,
    ).astype(int)

    avg_support_resolution_hours = np.clip(np.random.normal(16 + 10 * support_tickets_last_90d + 8 * refund_requests_last_12m, 12, n_rows), 1, 120)
    no_ticket_mask = support_tickets_last_90d == 0
    avg_support_resolution_hours[no_ticket_mask] = np.clip(np.random.normal(4, 2, no_ticket_mask.sum()), 1, 12)

    email_open_rate = np.clip(np.random.beta(2.2 + 1.3 * np.maximum(engagement, 0), 2.8 + 0.6 * np.maximum(-engagement, 0), n_rows), 0, 1)
    email_open_rate = np.clip(email_open_rate - 0.006 * days_since_last_login + np.random.normal(0, 0.03, n_rows), 0, 1)

    recommendation_click_rate = np.clip(
        0.05 + 0.55 * email_open_rate + 0.10 * np.maximum(engagement, 0) - 0.004 * days_since_last_login + np.random.normal(0, 0.06, n_rows),
        0,
        1,
    )

    logit = (
        0.35
        + 0.07 * days_since_last_login
        - 0.16 * weekly_learning_hours
        - 0.10 * sessions_per_week
        - 0.018 * avg_course_progress_pct
        - 0.20 * courses_completed
        - 0.22 * certificates_earned
        + 0.48 * payment_failures_last_6m
        + 0.78 * refund_requests_last_12m
        + 0.18 * support_tickets_last_90d
        + 0.012 * avg_support_resolution_hours
        - 1.0 * auto_renew_enabled
        - 1.2 * email_open_rate
        - 1.0 * recommendation_click_rate
        + 0.20 * (days_until_renewal <= 5)
        - 0.015 * np.minimum(tenure, 24)
        + 0.22 * (monthly_price > 35)
        + 0.18 * (plan_type == "premium")
        + 0.08 * (plan_type == "basic")
        + np.random.normal(0, 0.65, n_rows)
    )
    churn_probability = 1 / (1 + np.exp(-logit))

    np.random.seed(seed + 1)
    churn_label = (np.random.rand(n_rows) < churn_probability).astype(int)

    df = pd.DataFrame({
        "subscriber_id": subscriber_id,
        "age": age.astype(int),
        "country": country,
        "profession_segment": profession,
        "plan_type": plan_type,
        "monthly_price_usd": np.round(monthly_price, 2),
        "tenure_months": tenure.astype(int),
        "auto_renew_enabled": auto_renew_enabled.astype(int),
        "days_until_renewal": days_until_renewal.astype(int),
        "payment_method": payment_method,
        "weekly_learning_hours": np.round(weekly_learning_hours, 1),
        "sessions_per_week": sessions_per_week.astype(int),
        "avg_session_duration_minutes": np.round(avg_session_duration_minutes, 1),
        "days_since_last_login": days_since_last_login.astype(int),
        "courses_started": courses_started.astype(int),
        "courses_completed": courses_completed.astype(int),
        "active_courses_count": active_courses_count.astype(int),
        "avg_course_progress_pct": np.round(avg_course_progress_pct, 1),
        "certificates_earned": certificates_earned.astype(int),
        "quiz_attempts_last_30d": quiz_attempts_last_30d.astype(int),
        "assignment_submissions_last_30d": assignment_submissions_last_30d.astype(int),
        "forum_posts_last_30d": forum_posts_last_30d.astype(int),
        "payment_failures_last_6m": payment_failures_last_6m.astype(int),
        "refund_requests_last_12m": refund_requests_last_12m.astype(int),
        "support_tickets_last_90d": support_tickets_last_90d.astype(int),
        "avg_support_resolution_hours": np.round(avg_support_resolution_hours, 1),
        "email_open_rate": np.round(email_open_rate, 3),
        "recommendation_click_rate": np.round(recommendation_click_rate, 3),
        "churn_label": churn_label.astype(int),
    })

    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    df = generate_subscriber_churn_snapshot()
    print(df.head())
    print("\nShape:", df.shape)
    print("Churn rate:", round(df["churn_label"].mean(), 4))
