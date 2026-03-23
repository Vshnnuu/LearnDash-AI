from __future__ import annotations

from typing import Dict, List, Tuple


def analyze_churn_drivers(profile: Dict, churn_probability: float, risk_level: str) -> List[str]:
    scored_drivers: List[Tuple[int, str]] = []

    if churn_probability >= 0.7:
        scored_drivers.append((5, "Overall churn probability is high."))

    if profile.get("days_since_last_login", 0) >= 21:
        scored_drivers.append((5, "The learner has been inactive for a long period."))
    elif profile.get("days_since_last_login", 0) >= 14:
        scored_drivers.append((4, "The learner has reduced recent platform activity."))

    if profile.get("weekly_learning_hours", 0) < 1:
        scored_drivers.append((4, "Weekly learning time is extremely low."))
    elif profile.get("weekly_learning_hours", 0) < 2:
        scored_drivers.append((3, "Weekly learning time is low."))

    if profile.get("avg_course_progress_pct", 0) < 15:
        scored_drivers.append((4, "Course progress is critically low."))
    elif profile.get("avg_course_progress_pct", 0) < 25:
        scored_drivers.append((3, "Course progress is low."))

    if profile.get("payment_failures_last_6m", 0) >= 2:
        scored_drivers.append((5, "Repeated payment failures suggest billing friction."))
    elif profile.get("payment_failures_last_6m", 0) >= 1:
        scored_drivers.append((4, "Recent payment failures may indicate billing friction."))

    if profile.get("support_tickets_last_90d", 0) >= 3:
        scored_drivers.append((4, "Frequent support tickets may indicate unresolved frustration."))

    if profile.get("email_open_rate", 0) < 0.10:
        scored_drivers.append((3, "Email engagement is very low."))
    elif profile.get("email_open_rate", 0) < 0.15:
        scored_drivers.append((2, "Email engagement is below expected levels."))

    if profile.get("recommendation_click_rate", 0) < 0.10:
        scored_drivers.append((3, "Content recommendation engagement is low."))

    scored_drivers.sort(key=lambda x: x[0], reverse=True)
    top_drivers = [driver for _, driver in scored_drivers[:4]]

    if not top_drivers:
        top_drivers = ["No major churn drivers detected."]

    return top_drivers


def recommend_actions(profile: Dict, churn_probability: float, risk_level: str) -> List[str]:
    scored_actions: List[Tuple[int, str]] = []

    if risk_level == "High":
        scored_actions.extend(
            [
                (5, "Offer a 20% retention discount for the next billing cycle."),
                (5, "Trigger a proactive customer success outreach message."),
                (4, "Send a personalized email with course recommendations based on past learning behavior."),
            ]
        )
    elif risk_level == "Medium":
        scored_actions.extend(
            [
                (4, "Offer a 7-day premium feature trial."),
                (4, "Send a learning nudge highlighting partially completed courses."),
                (3, "Recommend one high-value course aligned with the learner's profession segment."),
            ]
        )
    else:
        scored_actions.extend(
            [
                (3, "Send a light engagement email with trending courses."),
                (3, "Recommend a new learning path to maintain momentum."),
            ]
        )

    if profile.get("payment_failures_last_6m", 0) >= 1:
        scored_actions.append((5, "Prompt the learner to verify or update payment details."))

    if profile.get("days_since_last_login", 0) >= 14:
        scored_actions.append((4, "Send a reactivation reminder focused on unfinished learning goals."))

    if profile.get("support_tickets_last_90d", 0) >= 3:
        scored_actions.append((4, "Prioritize support quality follow-up to address unresolved friction."))

    if profile.get("avg_course_progress_pct", 0) < 25:
        scored_actions.append((4, "Recommend a shorter beginner-friendly course to rebuild engagement."))

    if profile.get("auto_renew_enabled", 1) == 0 and risk_level in {"Medium", "High"}:
        scored_actions.append((4, "Incentivize enabling auto-renew with a loyalty perk or small discount."))

    scored_actions.sort(key=lambda x: x[0], reverse=True)

    deduped: List[str] = []
    seen = set()
    for _, action in scored_actions:
        if action not in seen:
            deduped.append(action)
            seen.add(action)

    return deduped[:4]


def build_execution_plan(actions: List[str]) -> List[str]:
    execution_steps: List[str] = []

    for action in actions:
        action_lower = action.lower()

        if "email" in action_lower:
            execution_steps.append("Prepared outreach workflow.")
        elif "discount" in action_lower or "offer" in action_lower:
            execution_steps.append("Prepared retention offer.")
        elif "support" in action_lower or "customer success" in action_lower:
            execution_steps.append("Prepared support follow-up task.")
        elif "payment" in action_lower:
            execution_steps.append("Prepared billing intervention.")
        elif "recommend" in action_lower or "course" in action_lower:
            execution_steps.append("Prepared personalized learning recommendation.")
        else:
            execution_steps.append("Prepared intervention step.")

    deduped_steps: List[str] = []
    seen = set()
    for step in execution_steps:
        if step not in seen:
            deduped_steps.append(step)
            seen.add(step)

    return deduped_steps


def generate_retention_plan(profile: Dict, churn_probability: float, risk_level: str) -> Dict:
    drivers = analyze_churn_drivers(profile, churn_probability, risk_level)
    actions = recommend_actions(profile, churn_probability, risk_level)
    execution_plan = build_execution_plan(actions)

    return {
        "churn_drivers": drivers,
        "recommended_actions": actions,
        "execution_plan": execution_plan,
    }