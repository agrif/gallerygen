import argparse
import os.path
import sys
import urllib.request

from PIL import Image, ImageFile
import jinja2

loader = jinja2.FileSystemLoader(os.path.split(__file__)[0])
env = jinja2.Environment(loader=loader)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Generate a photo gallery.')
    p.add_argument('photos', metavar='PHOTODIR', type=str,
                   help='the photos to make a gallery for')
    p.add_argument('output', metavar='OUTDIR', type=str,
                   help='the output directory')
    p.add_argument('-q', '--quality', type=int, default=95,
                   help='the JPEG output quality')
    p.add_argument('-f', '--force', action='store_const',
                   const=True, default=False,
                   help='force image regeneration')
    p.add_argument('--title', type=str, default='Gallery',
                   help='title of the gallery')
    p.add_argument('--tagline', type=str, default='',
                   help='tagline of the gallery')

    args = p.parse_args()
    if not os.path.exists(args.photos):
        print('Photo directory does not exist.', file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.output):
        try:
            os.mkdir(args.output)
        except OSError:
            print('Could not create output directory.', file=sys.stderr)
            sys.exit(1)

    imgs = []
    for img in os.listdir(args.photos):
        f = os.path.join(args.photos, img)
        try:
            Image.open(f)
            imgs.append(f)
        except OSError:
            pass

    def local_open(f, *targs, **kwargs):
        return open(os.path.join(args.output, f), *targs, **kwargs)

    def ensure_dir(d):
        p = os.path.join(args.output, d)
        if not os.path.exists(p):
            os.mkdir(p)

    def needs_regen(src, dest):
        if not os.path.exists(dest):
            return True
        return args.force or (os.path.getmtime(src) >= os.path.getmtime(dest))
    
    def grabfile(url, dest='dat'):
        ensure_dir(dest)
        tail = url.rsplit('/', 1)[1]
        destp = os.path.join(args.output, dest, tail)

        if not os.path.exists(destp):
            print('fetching', url)
            urllib.request.urlretrieve(url, destp)
        return dest + '/' + tail
    env.filters['grabfile'] = grabfile

    def large(img):
        ensure_dir('img')
        name = os.path.split(img)[1]
        tail = os.path.splitext(name)[0] + '.jpg'
        destp = os.path.join(args.output, 'img', tail)

        if needs_regen(img, destp):
            print('converting', name)
            im = Image.open(img)
            oldm = ImageFile.MAXBLOCK
            try:
                im.save(destp, quality=args.quality, progressive=True)
            except IOError:
                ImageFile.MAXBLOCK = im.size[0] * im.size[1]
                im.save(destp, quality=args.quality, progressive=True)
            finally:
                ImageFile.MAXBLOCK = oldm
        return 'img/' + tail
    env.filters['large'] = large

    def thumb(img, size):
        ensure_dir('thumbs')
        name = os.path.split(img)[1]
        tail = os.path.splitext(name)[0] + '.jpg'
        destp = os.path.join(args.output, 'thumbs', tail)

        if needs_regen(img, destp):
            print('thumbnailing', name)
            im = Image.open(img)
            im.thumbnail((size, size), Image.ANTIALIAS)
            im.save(destp, quality=args.quality, progressive=True)
        return 'thumbs/' + tail
    env.filters['thumb'] = thumb

    with local_open('index.html', 'wt') as f:
        f.write(env.get_template('template.html').render(images=imgs, title=args.title, tagline=args.tagline))
