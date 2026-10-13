"""Download packages in downloads/. Each zip keeps the kit's folder paths.

Run last (build_all.sh does), so every zip holds the current assets.
"""
import os, sys, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from common import KIT

SKIP_NAMES = {'.DS_Store', '.render.html'}
SKIP_DIRS = {'__pycache__'}

PACKS = {
    'hey-atu-google-play': ['03-stores/google-play'],
    'hey-atu-app-store': ['03-stores/app-store'],
    'hey-atu-app-icons': ['02-app-icon', '03-stores/ai-directories'],
    'hey-atu-logo': ['01-logo'],
    'hey-atu-marketing': ['04-marketing', '05-states'],
    'hey-atu-character': ['05-states', '10-character'],
    'hey-atu-fonts-tokens': ['07-fonts-and-tokens'],
    # everything except the PDF, the research and the downloads themselves
    'hey-atu-brand-kit-full': ['README.md', 'Hey-Atu-Brand-Guidelines.html', '01-logo', '02-app-icon', '03-stores',
                               '04-marketing', '05-states', '06-app-samples', '07-fonts-and-tokens', '08-source',
                               '09-generator', '10-character'],
}


def files(rel):
    p = os.path.join(KIT, rel)
    if os.path.isfile(p):
        yield rel
        return
    for root, dirs, names in os.walk(p):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for n in sorted(names):
            if n not in SKIP_NAMES:
                yield os.path.relpath(os.path.join(root, n), KIT)


def main():
    out = os.path.join(KIT, 'downloads')
    os.makedirs(out, exist_ok=True)
    for name, parts in PACKS.items():
        path = os.path.join(out, name + '.zip')
        tmp = path + '.tmp'
        n = 0
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for part in parts:
                for rel in files(part):
                    z.write(os.path.join(KIT, rel), rel)
                    n += 1
        os.replace(tmp, path)
        print(f'{name}.zip  {n} files  {os.path.getsize(path) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
