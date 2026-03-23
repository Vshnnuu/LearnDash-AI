from __future__ import annotations

from typing import List


def simulate_crm_actions(actions: List[str]) -> List[str]:
    executed_steps: List[str] = []

    counters = {
        "offer": 1042,
        "email": 2208,
        "support": 3314,
        "billing": 4471,
        "learning": 5586,
        "general": 6620,
    }

    for action in actions:
        action_lower = action.lower()

        if "discount" in action_lower or "offer" in action_lower:
            executed_steps.append(
                f"[COMPLETED] Discount offer created — OFF-{counters['offer']} — Queued just now"
            )
            counters["offer"] += 1

        elif "email" in action_lower or "reactivation" in action_lower:
            executed_steps.append(
                f"[QUEUED] Email campaign queued — EML-{counters['email']} — Queued just now"
            )
            counters["email"] += 1

        elif "customer success" in action_lower or "support" in action_lower:
            executed_steps.append(
                f"[OPEN] Support follow-up task created — SUP-{counters['support']} — Created just now"
            )
            counters["support"] += 1

        elif "payment" in action_lower or "billing" in action_lower:
            executed_steps.append(
                f"[OPEN] Billing intervention task created — BIL-{counters['billing']} — Created just now"
            )
            counters["billing"] += 1

        elif "recommend" in action_lower or "course" in action_lower or "learning path" in action_lower:
            executed_steps.append(
                f"[QUEUED] Learning recommendation workflow queued — LRN-{counters['learning']} — Queued just now"
            )
            counters["learning"] += 1

        else:
            executed_steps.append(
                f"[LOGGED] Retention intervention logged — GEN-{counters['general']} — Logged just now"
            )
            counters["general"] += 1

    deduped_steps: List[str] = []
    seen = set()
    for step in executed_steps:
        if step not in seen:
            deduped_steps.append(step)
            seen.add(step)

    return deduped_steps