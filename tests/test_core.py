import unittest,io,zipfile,tarfile,json
from pathlib import Path
from reproducible_archive_diff import run
class Tests(unittest.TestCase):
 def zip(self,content='x',mode=0o100644,duplicate=False):
  b=io.BytesIO()
  with zipfile.ZipFile(b,'w')as z:
   i=zipfile.ZipInfo('x',(2020,1,1,0,0,0));i.external_attr=mode<<16;z.writestr(i,content)
   if duplicate:z.writestr(i,content)
  return {'format':'zip','archive_hex':b.getvalue().hex()}
 def test_container_timestamp_difference_only_ignored_when_declared(self):
  d=json.loads(Path('examples/demo.json').read_text());r=run(d);self.assertFalse(r['raw_archives_identical']);self.assertTrue(r['equivalent_under_declared_policy']);d['ignore_mtime']=False;self.assertEqual(run(d)['differences'][0]['fields'],['mtime'])
 def test_content_and_executable_permission_changes_remain_visible(self):
  for after,field in [(self.zip('changed'),'sha256'),(self.zip(mode=0o100755),'mode')]:self.assertIn(field,run({'before':self.zip(),'after':after,'ignore_mtime':True})['differences'][0]['fields'])
 def test_duplicate_member_names_are_not_last_wins(self):self.assertFalse(run({'before':self.zip(duplicate=True),'after':self.zip()})['comparable'])
 def test_tar_symlink_target_change_is_visible(self):
  def tar(target):
   b=io.BytesIO()
   with tarfile.open(fileobj=b,mode='w')as t:
    i=tarfile.TarInfo('link');i.type=tarfile.SYMTYPE;i.linkname=target;t.addfile(i)
   return {'format':'tar','archive_hex':b.getvalue().hex()}
  self.assertIn('link_target',run({'before':tar('a'),'after':tar('b')})['differences'][0]['fields'])
