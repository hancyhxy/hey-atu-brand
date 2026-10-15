"""HTML templates are written to ROOT/build and load ../HeyAtu-Brand-Kit/... (logo, icons,
states, stickers). When ATU_KIT points somewhere else (e.g. the git clone), copy the freshly
built files there first, so store, marketing and sample images never use stale artwork."""
import os, shutil
from common import ROOT, KIT

dst = os.path.join(ROOT, 'HeyAtu-Brand-Kit')
if os.path.realpath(dst) == os.path.realpath(KIT):
    print('kit is the template source, nothing to sync')
else:
    for d in ('01-logo', '02-app-icon', '04-marketing', '05-states', '10-character'):
        src = os.path.join(KIT, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dst, d), dirs_exist_ok=True)
    print('synced to', dst)
