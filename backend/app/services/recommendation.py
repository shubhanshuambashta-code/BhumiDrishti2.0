"""
Simple rule-based recommendation engine.
Takes a project dict and returns a list of recommendations with priority.
"""

def recommend_for_project(p: dict):
    recs = []
    # Pending approvals
    if int(p.get('pending_approvals', 0)) > 0:
        recs.append({
            'issue': 'Pending approvals',
            'priority': 'High' if int(p.get('pending_approvals',0))>2 else 'Medium',
            'actions': [
                'Escalate approval request to department head',
                'Assign responsible approval officer',
                'Set approval SLA: 30 days'
            ]
        })
    # Compensation pending
    if int(p.get('compensation_pending_percentage', 0)) > 20:
        recs.append({
            'issue': 'Compensation pending',
            'priority': 'High' if int(p.get('compensation_pending_percentage',0))>50 else 'Medium',
            'actions': [
                'Prioritize compensation verification',
                'Flag pending beneficiaries',
                'Initiate payment reconciliation with accounts'
            ]
        })
    # Legal disputes
    if int(p.get('legal_disputes', 0)) > 0:
        recs.append({
            'issue': 'Legal disputes',
            'priority': 'High',
            'actions': [
                'Refer to legal cell for case prioritization',
                'Perform ownership/document verification',
                'Consider mediation for faster resolution'
            ]
        })
    # Documentation completeness
    if int(p.get('documentation_completeness', 100)) < 70:
        recs.append({
            'issue': 'Documentation incomplete',
            'priority': 'Medium',
            'actions': [
                'Request missing documents from stakeholders',
                'Trigger document verification workflow'
            ]
        })
    # R&R pending
    if int(p.get('r_and_r_pending_families', 0)) > 0:
        recs.append({
            'issue': 'R&R pending',
            'priority': 'High',
            'actions': [
                'Assign R&R officer',
                'Schedule rehabilitation outreach',
                'Track affected families through case management'
            ]
        })
    # Low possession
    if int(p.get('possession_percentage',0)) < 50:
        recs.append({
            'issue': 'Low possession',
            'priority': 'High' if int(p.get('possession_percentage',0))<20 else 'Medium',
            'actions': [
                'Plan possession drives',
                'Coordinate with local police for peaceful handover',
                'Resolve outstanding claims'
            ]
        })

    if not recs:
        recs.append({'issue': 'No immediate issues detected', 'priority': 'Low', 'actions': ['Monitor project progress']})
    return recs
