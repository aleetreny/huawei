"""Fallos de la replica en la accion principal trimestral: que accion, que diferencia y en que contexto."""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ingenieria-inversa'))
os.environ.setdefault('BB_DATA', os.path.join(HERE, '..', '..', 'lab', 'data', 'ingenieria-inversa'))
import replica as R
from bbdata import DATA
R.DEBUG = collections.Counter()
batches = sys.argv[1].split(',') if len(sys.argv) > 1 else ['v03-validation', 'd01-planner2']
R.validate(R.Catalog(json.load(open(DATA / 'catalog_v2.json'))), batches, verbose=False)
tot = collections.Counter()
for (ph, month_change, tags, diff), v in R.DEBUG.items():
    if ph == 'm': tot[(month_change, tags, diff)] += v
for k, v in tot.most_common(25): print(v, k)
