import pprint

from os import listdir, mkdir
from os.path import isfile, join, basename, isdir
from shutil import copyfile


def make_command(outfilename, inlist):
  mainoutput = 'qtmux name=outmux ! filesink location={output}'.format(
    output=outfilename,
  )
  cvideo = 'cvideo'
  caudio = 'caudio'

  videoout = 'concat name={concat} ! outmux.video_0'.format(
    concat = cvideo,
  )
  audioout = 'concat name={concat} ! outmux.audio_0'.format(
    concat = caudio,
  )
  return 'gst-launch-1.0 {mainout} {videoout} {audioout} {files}'.format(
    mainout = mainoutput,
    videoout = videoout,
    audioout = audioout,
    files = ' '.join(map(lambda x: make_input_file(x, 'cvideo', 'caudio'), inlist))
  )


def make_input_file(filename, cvideo, caudio):
  demuxname = 'demux_{}'.format(
      os.path.basename(filename).replace('.', '_')
  )
  fileinput = 'filesrc location={infile} ! queue ! qtdemux name={demux}'.format(
    infile=filename,
    demux=demuxname,
  )
  videoout = '{demux}.video_0 ! queue ! {concat}.'.format(
    demux=demuxname,
    concat=cvideo,
  )
  audioout = '{demux}.video_0 ! queue ! {concat}.'.format(
    demux=demuxname,
    concat=caudio, 
  )
  return '{inelem} {videoout} {audioout}'.format(
    inelem=fileinput,
    videoout=videoout,
    audioout=audioout,
  )


def get_jobs(inpath, outpath):
  files = [join(inpath, f) for f in listdir(inpath) if isfile(join(inpath, f))]
  result = {}
  prefixMain = 'GOPR'
  prefixPart = 'GP'
  
  for f in files:
    filename = basename(f)
    if filename.startswith(prefixMain):
      name = filename.split('.')[0][len(prefixMain):]
    elif filename.startswith(prefixPart):
      name = filename.split('.')[0][len(prefixPart):][2:]
    if not name in result:
      result[name] = []
    result[name].append(f)
    # not terrible efficient, but I don't expect to have
    # many elements
    result[name].sort()

  for k in result:
    handle_job(outpath, k, result[k])



def handle_job(outpath, groupName, infiles):
  outdir = join(outpath, groupName)
  if isdir(outdir):
    raise IOError('{} already exists'.format())
  
  mkdir(outdir) 
  mkdir(join(outdir, 'processed'))
  mkdir(join(outdir, 'originals'))
  infiles.sort()
  for f in infiles:
    copyfile(
      f,
      join(join(join(outdir, 'originals'), basename(f)))
    )
  

def main():
  get_jobs(
    '/home/coditza/movies/gopro/staging/',
    '/home/coditza/movies/gopro/sorted/',
  )


if __name__ == '__main__':
    main()
