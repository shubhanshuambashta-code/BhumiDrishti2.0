import base64
from typing import List, Dict

FEATURES = ['land_issues', 'pending_approvals', 'compensation_pending', 'possession_pct', 'legal_disputes']


def _deterministic_scores(project_id: str):
    # deterministic pseudo-random based on project_id so repeated calls return same values
    seed = sum(ord(c) for c in str(project_id))
    vals = []
    for i in range(len(FEATURES)):
        v = ((seed * (i+3)) % 101) - 50  # range -50..50
        vals.append(round(v / 10.0, 3))
    return vals


def _build_svg(contribs: List[float], features: List[str]) -> str:
    # simple horizontal bar SVG, no external deps
    max_len = max(abs(v) for v in contribs) if contribs else 1
    width = 600
    bar_height = 18
    padding = 10
    height = padding*2 + len(features) * (bar_height + 8)
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">']
    svg_parts.append(f'<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:12px}}</style>')
    for idx, (f, v) in enumerate(zip(features, contribs)):
        y = padding + idx * (bar_height + 8)
        val = v
        bar_w = int((abs(val) / max_len) * (width*0.45))
        if val >= 0:
            x = width*0.5
            color = '#ef4444'
        else:
            x = int(width*0.5 - bar_w)
            color = '#10b981'
        # label
        svg_parts.append(f'<text x="6" y="{y + bar_height/1.5}">{f}</text>')
        # value text
        svg_parts.append(f'<text x="{int(width*0.5)+6}" y="{y + bar_height/1.5}" fill="#333">{val:+.3f}</text>')
        # bar background
        svg_parts.append(f'<rect x="{int(width*0.5)-int(width*0.45)}" y="{y}" width="{int(width*0.9)}" height="{bar_height}" fill="#f3f4f6" />')
        # bar
        svg_parts.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_height}" fill="{color}" />')
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_shap_explanation(project_id: str) -> Dict:
    scores = _deterministic_scores(project_id)
    items = [{'feature': f, 'contribution': float(score)} for f, score in zip(FEATURES, scores)]
    sorted_items = sorted(items, key=lambda x: x['contribution'], reverse=True)
    top_positive = [it for it in sorted_items if it['contribution'] > 0][:5]
    top_negative = [it for it in sorted_items if it['contribution'] < 0][:5]
    svg = _build_svg([it['contribution'] for it in items], FEATURES)
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    chart_data = f'data:image/svg+xml;base64,{b64}'
    return {
        'chart_base64': chart_data,
        'top_positive_contributors': top_positive,
        'top_negative_contributors': top_negative
    }
