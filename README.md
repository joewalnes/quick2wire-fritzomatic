Fritz-o-matic: A simple part generator for http://fritzing.org/
===============================================================

Background
----------

This is a web-app that simplifies the process of generating
a generic IC component that can be re-used in [Fritzing](http://fritzing.org/).

Fritzing is a great tool for creating bread-boarded electronics designs,
schematics, and PCB layouts - assuming you have the necessary components.
Unfortunately, building components is still a fairly tedious and messy
process. This script automates that.

Usage
-----

Goto [fritzomatic.joewalnes.com](http://fritzomatic.joewalnes.com) to build and download your own component.

Hacking
-------

This is only if you need to make changes to the application itself.

The application is hosted on [Heroku Cedar Stack](https://devcenter.heroku.com/articles/cedar).

Dependencies:

    pip install -r requirements.txt # installs required libraries
    # Also, see https://toolbelt.heroku.com/ to install Heroku toolbelt

To run locally:

    make run
    # Navigate to http://localhost:5000

To deploy live, to http://fritzomatic.joewalnes.com :

    make live


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/joewalnes/quick2wire-fritzomatic/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

