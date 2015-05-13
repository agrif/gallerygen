GalleryGen
==========

This is a simple script I wrote to take a directory of images and wrap
them up all neatly into a simple static web gallery, converting to
JPEG as it goes (since I use it primarily for sharing photos).

GalleryGen requires Python 3, [Pillow], and [Jinja2].

 [Pillow]: https://pillow.readthedocs.org/
 [Jinja2]: http://jinja.pocoo.org/docs/dev/

It comes with a really simple theme that uses [Swipebox][],
[Bagpakk][], and [normalize.css][], and works relatively well on the
desktop or on a phone. You are welcome to edit the [Jinja2][] template
to your satisfaction. The template has a mechanism to download
external JS and CSS urls, so that the resulting gallery is totally
self-contained.

 [Swipebox]: http://brutaldesign.github.io/swipebox/
 [Bagpakk]: http://brutaldesign.github.io/bagpakk/
 [normalize.css]: http://necolas.github.io/normalize.css/

Usage
-----

Basically, you'll want to run:

    python3 gallerygen.py path/to/images/ output/

See `gallerygen.py --help` for more info.
