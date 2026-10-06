"""Build a deterministic MCADDON containing two independently importable MCPACKs."""
from pathlib import Path
import json, zipfile, hashlib
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'package.json').read_text())['version']
DIST=ROOT/'dist';DIST.mkdir(exist_ok=True)
def archive(path, files):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,date_time=(2026,10,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
   z.writestr(info,data)
for p in ['BP','RP']:
 archive(DIST/f'Moonweave_{p}_v{version}.mcpack',[(str(f.relative_to(ROOT/p)),f.read_bytes()) for f in sorted((ROOT/p).rglob('*')) if f.is_file()])
files=[(f'Moonweave_{p}_v{version}.mcpack',(DIST/f'Moonweave_{p}_v{version}.mcpack').read_bytes()) for p in ['BP','RP']]
files.append(('README_JA.md',(ROOT/'README.md').read_bytes()))
addon=DIST/f'Moonweave_Broom_v{version}.mcaddon';archive(addon,files)
(DIST/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}\n' for f in sorted(DIST.iterdir()) if f.is_file() and f.suffix in {'.mcpack','.mcaddon'}))
print(f'Built {addon.name}: {addon.stat().st_size} bytes')
