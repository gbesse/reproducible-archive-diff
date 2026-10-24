import io,zipfile,tarfile,hashlib,stat

def read(value):
 raw=bytes.fromhex(value['archive_hex']);kind=value['format'];records={};duplicates=[];size=0
 if len(raw)>8_000_000:raise ValueError('size')
 def add(name,content,mode,type,target,mtime,uid=None,gid=None):
  nonlocal size
  size+=len(content)
  if len(records)>1000 or size>20_000_000:raise ValueError('uncompressed_budget')
  if name in records:duplicates.append(name)
  records[name]={'name':name,'sha256':hashlib.sha256(content).hexdigest()if type=='file'else None,'size':len(content)if type=='file'else 0,'mode':mode,'kind':type,'link_target':target,'mtime':mtime,'uid':uid,'gid':gid}
 try:
  if kind=='zip':
   with zipfile.ZipFile(io.BytesIO(raw))as archive:
    infos=archive.infolist()
    if len(infos)>1000 or sum(i.file_size for i in infos)>20_000_000:raise ValueError('budget')
    for i in infos:
     mode=i.external_attr>>16;type='directory'if i.is_dir()else'symlink'if stat.S_ISLNK(mode)else'file';content=archive.read(i)
     add(i.filename,content,mode,type,content.decode('utf-8')if type=='symlink'else None,list(i.date_time))
  elif kind=='tar':
   with tarfile.open(fileobj=io.BytesIO(raw),mode='r:*')as archive:
    count=0
    for i in archive:
     count+=1
     if count>1000 or i.size>20_000_000-size:raise ValueError('budget')
     type='file'if i.isfile()else'directory'if i.isdir()else'symlink'if i.issym()else'hardlink'if i.islnk()else'special'
     if type=='special':raise ValueError('unsupported_member')
     stream=archive.extractfile(i)if type=='file'else None;content=stream.read()if stream is not None else b''
     if stream is not None:stream.close()
     add(i.name,content,i.mode,type,i.linkname if i.issym()or i.islnk()else None,i.mtime,i.uid,i.gid)
  else:raise ValueError('format')
 except(zipfile.BadZipFile,tarfile.TarError,UnicodeError,RuntimeError,EOFError):raise ValueError('archive')from None
 return hashlib.sha256(raw).hexdigest(),records,sorted(set(duplicates))
def run(data):
 ignore=data.get('ignore_mtime',False)
 if not isinstance(ignore,bool):raise ValueError('policy')
 ha,a,da=read(data['before']);hb,b,db=read(data['after']);differences=[]
 if da or db:return {'comparable':False,'duplicate_names_before':da,'duplicate_names_after':db,'raw_archives_identical':ha==hb,'model':'bounded_archive_content_and_declared_metadata_comparison'}
 for name in sorted(set(a)|set(b)):
  if name not in a or name not in b:differences.append({'name':name,'status':'added'if name in b else'removed'});continue
  changed=[k for k in a[name]if k!='name'and not(ignore and k=='mtime')and a[name][k]!=b[name][k]]
  if changed:differences.append({'name':name,'status':'changed','fields':changed})
 return {'comparable':True,'raw_archives_identical':ha==hb,'raw_sha256_before':ha,'raw_sha256_after':hb,'equivalent_under_declared_policy':not differences,'ignore_mtime':ignore,'differences':differences,'model':'bounded_archive_content_and_declared_metadata_comparison_order_ignored_paths_exact_no_extraction'}
