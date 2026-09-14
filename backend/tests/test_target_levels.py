from app.agents.competency.target_levels import resolve_target_level


def test_senior_designation_gets_highest_tier():
    assert resolve_target_level("Joint Director", "Statistical Officer") == 4.0
    assert resolve_target_level("Deputy Secretary", None) == 4.0


def test_middle_designation_gets_middle_tier():
    assert resolve_target_level("Section Officer", None) == 3.0


def test_junior_designation_gets_junior_tier():
    assert resolve_target_level("Junior Statistical Officer", None) == 2.0


def test_unknown_designation_gets_default_tier():
    assert resolve_target_level(None, None) == 2.5
    assert resolve_target_level("Some Unrecognized Title", None) == 2.5


def test_case_insensitive_matching():
    assert resolve_target_level("director", None) == 4.0
