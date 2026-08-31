import pytest
from app.services.recommendation import recommend_for_project


def test_recommendation_basic():
    project = {'pending_approvals': 3, 'compensation_pending_percentage': 60, 'legal_disputes': 1, 'documentation_completeness': 50, 'r_and_r_pending_families': 2, 'possession_percentage': 20}
    recs = recommend_for_project(project)
    assert isinstance(recs, list)
    assert any(r['issue']=='Pending approvals' for r in recs)
    assert any(r['issue']=='Compensation pending' for r in recs)
    assert any(r['issue']=='Legal disputes' for r in recs)
