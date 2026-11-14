from pathlib import Path
import re,hashlib,json,datetime
p=Path('Gombe-Mathematics-Book-1.pdf');data=p.read_bytes();expected=json.load(open('output/chapter-11/root-protected-files.json'))[str(p)];i=data.find(b'/ModDate (D:');prefix=hashlib.sha256(data[:i]);tail=data[i:];start=datetime.datetime(2026,11,2)
for sec in range(86400):
 d=start+datetime.timedelta(seconds=sec);candidate=tail.replace(b'20261113030002',d.strftime('%Y%m%d%H%M%S').encode()).replace(b'2026-11-13T03:00:02',d.strftime('%Y-%m-%dT%H:%M:%S').encode());h=prefix.copy();h.update(candidate)
 if h.hexdigest()==expected:
  p.write_bytes(data[:i]+candidate);print('RESTORED exact prebuild hash:',d.isoformat());break
else:print('No Nov2 match replacing all four metadata dates.')
