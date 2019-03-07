import argparse
import inspect
import os

rate = -1
duration = -1
color = ''
ffmpeg_path = ''

name_size = {
    '1080p': '1920x1080',
    '4k': '3840x2160',
    '8k': '7680x4320',
}

name_codec = {
    'h264': 'libx264',
    'h265': 'libx265',
    'vp8': 'libvpx',
    'vp9': 'libvpx-vp9', 
}


def parse_arg():
    global args
    parser = argparse.ArgumentParser(description='Gen video with pure color',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog='''
examples:
  python %(prog)s --size 4k --rate 60 --duration 30 --codec vp8
''')
    parser.add_argument('--size', dest='size', help='size (resolution)', required=True)
    parser.add_argument('--rate', dest='rate', help='rate (FPS)', required=True)
    parser.add_argument('--duration', dest='duration', help='duration in seconds', required=True)

    parser.add_argument('--codec', dest='codec', help='codec', default='vp8')
    parser.add_argument('--ffmpeg-path', dest='ffmpeg_path', help='ffmpeg path', default='D:/software/active/ffmpeg/bin/ffmpeg.exe')
    parser.add_argument('--color', dest='color', help='color', default='green')
    args = parser.parse_args()

def setup():
    global size, rate, duration, color, codec, ffmpeg_path
    if args.size in name_size:
        size = name_size[args.size]
    else:
        size = args.size

    rate = args.rate
    duration = args.duration
    color = args.color
    if args.codec not in name_codec:
        _error('Your codec %s is not supported' % args.codec)
    codec = name_codec[args.codec]
    ffmpeg_path = args.ffmpeg_path

def gen():
    if args.codec in ['h264', 'h265']:
        suffix = 'mp4'
    elif args.codec in ['vp8', 'vp9']:
        suffix = 'webm'

    cmd = '{ffmpeg_path} -f lavfi -i color={color}:size={size}:rate={rate}:duration={duration} -vcodec {codec} ../video/{codec_arg}-{size}-{rate}fps-{duration}s-{color}.{suffix}'.format(ffmpeg_path=ffmpeg_path, codec=codec, codec_arg=args.codec, size=size, rate=rate, duration=duration, color=color, suffix=suffix)
    _exec(cmd)

def _exec(cmd, return_out=False, show_cmd=True, show_duration=False, dryrun=False):
    if show_cmd:
        _cmd(cmd)

    if show_duration:
        start_time = datetime.datetime.now().replace(microsecond=0)

    if dryrun and not re.match('git log', cmd):
        result = [0, '']
    else:
        if return_out:
            tmp_out = ''
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = process.communicate()
            out = tmp_out + out
            ret = process.returncode
            result = [ret, out + err]
        else:
            ret = os.system(cmd)
            result = [ret / 256, '']

    if show_duration:
        end_time = datetime.datetime.now().replace(microsecond=0)
        time_diff = end_time - start_time
        _info(str(time_diff) + ' was spent to execute command: ' + cmd)

    return result

def _cmd(cmd):
    _msg(cmd)

def _error(error):
    _msg(error)
    exit(1)

def _info(info):
    _msg(info)

def _warning(warning):
    _msg(warning)

def _msg(msg):
    m = inspect.stack()[1][3].upper().lstrip('_')
    m = '[' + m + '] ' + msg
    print m

if __name__ == '__main__':
    parse_arg()
    setup()
    gen()