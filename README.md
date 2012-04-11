Fritz-o-matic: A simple part generator for http://fritzing.org/
===============================================================

Background
----------

This is a little Python script that simplifies the process of generating
a generic IC component that can be re-used in [Fritzing](http://fritzing.org/).

Fritzing is a great tool for creating bread-boarded electronics designs,
schematics, and PCB layouts - assuming you have the necessary components.
Unfortunately, building components is still a fairly tedious and messy
process. This script automates that.


Running
-------

Include this checkout directory in your `PYTHONPATH`.

    export PYTHONPATH=.
    ./fritzomatic/main.py examples/mcp23008.py

The application is hosted on [Heroku Cedar Stack](https://devcenter.heroku.com/articles/cedar).

Dependencies:

    flask               # pip install flask
    heroku toolbelt     # See https://toolbelt.heroku.com/

To locally:

   foreman start        # foreman is part of the Heroku Toolbelt
   # Navigate to http://localhost:5000

To deploy live:

   git remote add live git@heroku.com:fritzomatic.git     # one time setup
   git push live master
   # Navigate to http://fritzomatic.quick2wire.com/
