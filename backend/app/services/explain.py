import base64
from typing import List, Dict
import time

FEATURES = ['land_issues', 'pending_approvals', 'compensation_pending', 'possession_pct', 'legal_disputes']

# simple in-memory cache: project_id -> (timestamp, data)
_CACHE: Dict[str, Dict] = {}
CACHE_TTL = 3600  # seconds (1 hour)

def invalidate_explain_cache(project_id: str) -> bool:
    """Invalidate the cached explanation for a project. Returns True if an entry was removed."""
    if project_id in _CACHE:
        del _CACHE[project_id]
        return True
    return False


def _deterministic_scores(project_id: str):
    seed = sum(ord(c) for c in str(project_id))
    vals = []
    for i in range(len(FEATURES)):
        v = ((seed * (i+3)) % 101) - 50  # range -50..50
        vals.append(round(v / 10.0, 3))
    return vals


def _build_svg(contribs: List[float], features: List[str]) -> str:
    max_len = max((abs(v) for v in contribs), default=1)
    width = 600
    bar_height = 18
    padding = 10
    height = padding*2 + len(features) * (bar_height + 8)
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    svg_parts.append(f'<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:12px}}</style>')
    for idx, (f, v) in enumerate(zip(features, contribs)):
        y = padding + idx * (bar_height + 8)
        val = v
        bar_w = int((abs(val) / max_len) * (width*0.45)) if max_len else 1
        if val >= 0:
            x = int(width*0.5)
            color = '#ef4444'
        else:
            x = int(width*0.5 - bar_w)
            color = '#10b981'
        svg_parts.append(f'<text x="6" y="{y + int(bar_height*0.75)}">{f}</text>')
        svg_parts.append(f'<text x="{int(width*0.5)+6}" y="{y + int(bar_height*0.75)}" fill="#333">{val:+.3f}</text>')
        svg_parts.append(f'<rect x="{int(width*0.5)-int(width*0.45)}" y="{y}" width="{int(width*0.9)}" height="{bar_height}" fill="#f3f4f6" />')
        svg_parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_height}" fill="{color}" />')
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_shap_explanation(project_id: str) -> Dict:
    # Use cache if available
    now = time.time()
    cached = _CACHE.get(project_id)
    if cached and (now - cached.get('ts', 0) < CACHE_TTL):
        return cached['data']

    scores = _deterministic_scores(project_id)
    items = [{'feature': f, 'contribution': float(score)} for f, score in zip(FEATURES, scores)]
    sorted_items = sorted(items, key=lambda x: x['contribution'], reverse=True)
    top_positive = [it for it in sorted_items if it['contribution'] > 0][:5]
    top_negative = [it for it in sorted_items if it['contribution'] < 0][:5]
    svg = _build_svg([it['contribution'] for it in items], FEATURES)
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    chart_data = f'data:image/svg+xml;base64,{b64}'
    data = {
        'chart_base64': chart_data,
        'top_positive_contributors': top_positive,
        'top_negative_contributors': top_negative,
        'raw_contributions': items
    }
    _CACHE[project_id] = {'ts': now, 'data': data}
    return data


def simulate_intervention(project_id: str, adjustments: Dict) -> Dict:
    """Simulate applying adjustments and return before/after risk scores and delta.
    adjustments expected keys:
      - pending_approvals (int)
      - compensation_pending_percentage (float)
      - possession_percentage (float)
      - legal_disputes (int)
    This is a lightweight deterministic simulation (heuristic weights) used for UI exploration.
    """
    base = generate_shap_explanation(project_id)
    base_score = sum([it['contribution'] for it in base['raw_contributions']])

    # Heuristic weights (per-unit effect on the aggregate score)
    w_pending = 0.3
    w_comp = 0.02
    w_poss = -0.02  # increasing possession reduces risk (negative effect)
    w_legal = 0.5

    pa = float(adjustments.get('pending_approvals', 0))
    comp = float(adjustments.get('compensation_pending_percentage', 0))
    poss = float(adjustments.get('possession_percentage', 0))
    legal = float(adjustments.get('legal_disputes', 0))

    # Compute delta as weighted sum (note signs chosen so that increases in pa/comp/legal increase risk)
    delta = (pa * w_pending) + (comp * w_comp) + (legal * w_legal) + (poss * w_poss)

    after_score = base_score + delta
    return {
        'before': round(float(base_score), 3),
        'after': round(float(after_score), 3),
        'delta_score': round(float(after_score - base_score), 3)
    }
