import yaml, os, tempfile, subprocess

d = yaml.safe_load(open(r'D:\mpv-android\.github\workflows\build-mpv.yml', encoding='utf-8'))
out = os.path.join(tempfile.gettempdir(), 'wfsh')
os.makedirs(out, exist_ok=True)
i = 0
paths = []
for s in d['jobs']['build']['steps']:
    if 'run' in s:
        i += 1
        p = os.path.join(out, 'step%d.sh' % i)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(s['run'])
        paths.append(p)

def to_wsl(p):
    p = p.replace('\\', '/')
    drive, rest = p[0], p[2:]
    return '/mnt/' + drive.lower() + rest

for p in paths:
    r = subprocess.run(['bash', '-n', to_wsl(p)], capture_output=True, text=True)
    print(os.path.basename(p), '->', 'SYNTAX OK' if r.returncode == 0 else 'FAIL')
    if r.returncode != 0:
        print(r.stderr)
