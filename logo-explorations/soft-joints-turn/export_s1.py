"""Write variant S1 (current line work + 6 deg turn) as the guideline glyph:
09-generator/glyph_shapes.json (v2.1). Shapes come from gen.turned_shapes on the pinned
v2.0 glyph; colour silhouette / white face are rebuilt from the new shapes the same way
v2.0 derived them (union of head and ears; head minus ears and patch)."""
import os, json, math
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
import gen

S1 = next(v for v in gen.VARIANTS if v[0] == 'S1')
_, _, _, deg, cheek, waist, _, _ = S1
S = gen.turned_shapes(math.radians(deg), cheek, waist)

def ring(g):
    if g.geom_type != 'Polygon':
        g = max(g.geoms, key=lambda p: p.area)
    return [[round(x, 3), round(y, 3)] for x, y in list(g.exterior.coords)[:-1]]

ears = unary_union([S['lear'], S['rear']])
sil = unary_union([S['head'], ears])
white = S['head'].difference(ears).difference(S['patch'])

def ell(e):
    a = np.array(e.exterior.coords)[:-1]
    return [round(e.centroid.x, 2), round(e.centroid.y, 2), round(float(np.ptp(a[:, 0])), 2), round(float(np.ptp(a[:, 1])), 2), 0.0]

old = json.load(open(os.path.join(gen.HERE, 'glyph_shapes_v2.0.json')))
out = dict(scale=old['scale'], head=ring(S['head']), lear=ring(S['lear']), rear=ring(S['rear']),
           patch=ring(S['patch']), eyes=[ring(e) for e in S['eyes']], eye_ellipses=[ell(e) for e in S['eyes']],
           note='v2.1 (2026-10-15): approved version A turned slightly to the viewer left (variant S1 of '
                'logo-explorations/soft-joints-turn: 6 deg, eyes/patch on a sphere, ears follow their roots, '
                'soft lower-left cheek). Line work and joins unchanged. Master units.',
           color_silhouette=ring(sil), color_white=ring(white))
dst = os.path.join(gen.HERE, '..', '..', '09-generator', 'glyph_shapes.json')
json.dump(out, open(dst, 'w'))
for k in ('head', 'lear', 'rear', 'patch'):
    print(k, len(out[k]))
print('white parts', white.geom_type, 'sil', sil.geom_type)
