#!/usr/bin/env python3
"""
Generate a synthetic land acquisition dataset for BHUMIDRISHTI.
Outputs CSV labelled as DEMONSTRATION data.
"""
import argparse
import uuid
import random
import numpy as np
import pandas as pd

STATES = ['StateA', 'StateB', 'StateC', 'StateD']
DISTRICTS = ['District1', 'District2', 'District3', 'District4']
PROJECT_TYPES = ['Road', 'Rail', 'Irrigation', 'Urban']
ACQUISITION_METHODS = ['LA2013', 'Consent', 'Negotiated']
NOTIFICATION_STATUS = ['Notified', 'Under Objection', 'Awarded']
APPROVAL_STATUS = ['Pending', 'Approved', 'Partially Approved']
CURRENT_STAGES = ['Initiation', 'Survey', 'Notification', 'Objections', 'Ownership Verification', 'Valuation', 'Award', 'Compensation', 'R&R', 'Possession', 'Handover']


def generate_row(i):
    project_id = str(uuid.uuid4())
    state = random.choice(STATES)
    district = random.choice(DISTRICTS)
    ptype = random.choice(PROJECT_TYPES)
    lat = 20 + random.random() * 10
    lon = 75 + random.random() * 10
    land_area = round(max(0.5, np.random.exponential(5.0)), 2)
    affected_families = np.random.poisson(5)
    affected_landowners = max(1, int(affected_families * random.uniform(0.6, 1.2)))
    acquisition_method = random.choice(ACQUISITION_METHODS)
    notification_status = random.choice(NOTIFICATION_STATUS)
    notification_date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=random.randint(0, 800))
    award_date = notification_date + pd.Timedelta(days=random.randint(30, 400)) if random.random() < 0.6 else pd.NaT
    approval_status = random.choice(APPROVAL_STATUS)
    pending_approvals = max(0, np.random.poisson(2) + (1 if approval_status=='Pending' else 0))
    approval_delay_days = max(0, int(np.random.normal(60, 40))) if approval_status!='Approved' else 0
    compensation_total = round(land_area * 100000 * random.uniform(0.8, 1.5))
    comp_disbursed_pct = max(0, min(100, int(np.random.normal(50, 40))))
    compensation_disbursed = int(compensation_total * comp_disbursed_pct / 100)
    compensation_pending = compensation_total - compensation_disbursed
    compensation_pending_percentage = 0 if compensation_total==0 else int(100*(compensation_pending/compensation_total))
    legal_disputes = np.random.binomial(1, 0.15)
    court_cases = np.random.poisson(0.2) if legal_disputes else 0
    documentation_completeness = int(min(100, max(10, np.random.normal(75, 20))))
    ownership_conflicts = np.random.binomial(1, 0.12)
    possession_percentage = int(min(100, max(0, np.random.normal(50, 35))))
    rehabilitation_status = random.choice(['Not Started', 'In Progress', 'Completed'])
    rehabilitation_percentage = int(min(100, max(0, np.random.normal(40, 40))))
    stakeholder_responsiveness = int(min(100, max(0, np.random.normal(60, 25))))
    department_response_delay_days = abs(int(np.random.normal(15, 30)))
    interdepartmental_dependencies = np.random.poisson(1)
    previous_project_delay_rate = round(random.random(), 2)
    planned_completion_days = int(np.random.normal(365, 180))
    elapsed_days = int(np.random.uniform(0, planned_completion_days*1.2))
    extension_count = np.random.poisson(0.3)
    grievance_count = np.random.poisson(0.5)
    field_verification_status = random.choice(['Pending', 'Completed', 'Partial'])
    survey_completion_percentage = int(min(100, max(0, np.random.normal(60, 30))))
    utility_shift_status = random.choice(['Not Started', 'In Progress', 'Completed'])
    environmental_clearance_status = random.choice(['Not Required', 'Pending', 'Approved'])
    forest_clearance_status = random.choice(['Not Required', 'Pending', 'Approved'])
    r_and_r_pending_families = max(0, int(affected_families * random.uniform(0, 1)))
    officer_workload = int(min(100, max(0, np.random.normal(40, 30))))
    historical_district_delay_rate = round(random.random(), 2)
    current_stage = random.choice(CURRENT_STAGES)
    # compute a probabilistic delay label (not deterministic) using weighted factors
    score = 0.0
    score += pending_approvals * 0.05
    score += (compensation_pending_percentage / 100.0) * 0.25
    score += legal_disputes * 0.2
    score += (1 - possession_percentage/100.0) * 0.15
    score += (1 - documentation_completeness/100.0) * 0.1
    score += (elapsed_days / max(1, planned_completion_days)) * 0.15
    # noise
    score += np.random.normal(0, 0.05)
    prob = 1.0/(1.0+np.exp(- (score*3 - 1.5)))
    delayed = np.random.binomial(1, prob)
    actual_delay_days = int(max(0, np.random.normal(200, 300))) if delayed else 0

    return {
        'project_id': project_id,
        'project_name': f"Project {i} - {ptype}",
        'project_type': ptype,
        'department': random.choice(['Public Works', 'Irrigation', 'Roads', 'Urban Dev']),
        'state': state,
        'district': district,
        'tehsil': f"Tehsil_{random.randint(1,20)}",
        'village': f"Village_{random.randint(1,200)}",
        'latitude': round(lat,6),
        'longitude': round(lon,6),
        'land_area_hectares': land_area,
        'affected_families': int(affected_families),
        'affected_landowners': int(affected_landowners),
        'acquisition_method': acquisition_method,
        'notification_status': notification_status,
        'notification_date': notification_date.date().isoformat(),
        'award_date': award_date.date().isoformat() if pd.notna(award_date) else '',
        'approval_status': approval_status,
        'pending_approvals': int(pending_approvals),
        'approval_delay_days': int(approval_delay_days),
        'compensation_total': int(compensation_total),
        'compensation_disbursed': int(compensation_disbursed),
        'compensation_pending': int(compensation_pending),
        'compensation_pending_percentage': int(compensation_pending_percentage),
        'legal_disputes': int(legal_disputes),
        'court_cases': int(court_cases),
        'documentation_completeness': int(documentation_completeness),
        'ownership_conflicts': int(ownership_conflicts),
        'possession_percentage': int(possession_percentage),
        'rehabilitation_status': rehabilitation_status,
        'rehabilitation_percentage': int(rehabilitation_percentage),
        'stakeholder_responsiveness': int(stakeholder_responsiveness),
        'department_response_delay_days': int(department_response_delay_days),
        'interdepartmental_dependencies': int(interdepartmental_dependencies),
        'previous_project_delay_rate': float(previous_project_delay_rate),
        'planned_completion_days': int(planned_completion_days),
        'elapsed_days': int(elapsed_days),
        'extension_count': int(extension_count),
        'grievance_count': int(grievance_count),
        'field_verification_status': field_verification_status,
        'survey_completion_percentage': int(survey_completion_percentage),
        'utility_shift_status': utility_shift_status,
        'environmental_clearance_status': environmental_clearance_status,
        'forest_clearance_status': forest_clearance_status,
        'r_and_r_pending_families': int(r_and_r_pending_families),
        'officer_workload': int(officer_workload),
        'historical_district_delay_rate': float(historical_district_delay_rate),
        'current_stage': current_stage,
        'actual_delay_days': int(actual_delay_days),
        'delayed': int(delayed)
    }

def main(n=1000, out='data/projects_demo.csv'):
    rows = []
    for i in range(n):
        rows.append(generate_row(i+1))
    df = pd.DataFrame(rows)
    # ensure directory exists
    df.to_csv(out, index=False)
    print(f"Generated {n} demo projects to {out}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=2000)
    parser.add_argument('--out', type=str, default='data/projects_demo.csv')
    args = parser.parse_args()
    main(args.n, args.out)
