"""Authorization backbone (SUBMISSION.md §5).

Policy lives in ONE place: the capabilities table.
authorize() depends only on its arguments, no globals, no shared state,
so one user's request can never leak into another's decision.
"""

ROLES = ("policyholder", "beneficiary")

CAPABILITIES = {
    "qna":                {"policyholder": True, "beneficiary": True},
    "claims":             {"policyholder": True, "beneficiary": True},
    "what_if":            {"policyholder": True, "beneficiary": False},
    "updates":            {"policyholder": True, "beneficiary": False},
    "beneficiary_change": {"policyholder": True, "beneficiary": False},
    "banking_change":     {"policyholder": True, "beneficiary": False},
}


def authorize(claims: dict, capability: str) -> tuple[bool, str]:
    role = claims.get("role")

    if role not in ROLES:
        return False, f"Invalid role: {role!r}"

    if capability not in CAPABILITIES:
        return False, f"Unknown capability: {capability!r}"

    # Runtime condition, separate from static policy: a beneficiary's access
    # is only active once the linked policyholder's deceased flag is set.
    # Security inputs are compared exactly, never trusted as truthy.
    if role == "beneficiary" and claims.get("deceased_flag") is not True:
        return False, "beneficiary access inactive: deceased flag not set"

    allowed = CAPABILITIES[capability][role]  # keys proven above; crash loudly if not
    if allowed:
        return True, f"{role} may use {capability}"
    return False, f"{role} is not permitted to use {capability}"


if __name__ == "__main__":
    # happy paths
    assert authorize({"role": "policyholder"}, "what_if") == (True, "policyholder may use what_if")
    assert authorize({"role": "beneficiary", "deceased_flag": True}, "claims")[0] is True
    assert authorize({"role": "beneficiary", "deceased_flag": True}, "updates")[0] is False

    # deceased flag gate
    assert authorize({"role": "beneficiary", "deceased_flag": False}, "claims")[0] is False
    assert authorize({"role": "beneficiary"}, "claims")[0] is False          # missing flag = deny
    assert authorize({"role": "beneficiary", "deceased_flag": "yes"}, "claims")[0] is False  # truthy != True

    # garbage in
    assert authorize({"role": "admin"}, "qna")[0] is False
    assert authorize({}, "qna")[0] is False
    assert authorize({"role": "policyholder"}, "hack_the_planet")[0] is False

    ok, reason = authorize({"role": "beneficiary", "deceased_flag": True}, "updates")
    assert not ok and "not permitted" in reason, reason

    # contract: EVERY exit is a (bool, str) tuple
    for c in ({"role": "policyholder"}, {"role": "beneficiary", "deceased_flag": True}, {}):
        for cap in ("qna", "claims", "banking_change", "nonsense"):
            result = authorize(c, cap)
            assert isinstance(result, tuple) and len(result) == 2, f"bad return for {c}, {cap}: {result!r}"
            assert isinstance(result[0], bool) and isinstance(result[1], str), f"bad types for {c}, {cap}: {result!r}"

    print("all checks pass")