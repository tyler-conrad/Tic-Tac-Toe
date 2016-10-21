Tic-Tac-Toe
===========

An implementation of Tic-Tac-Toe written in Python.  The program allows you to play against a computer AI opponent that never losses.  You have the option of taking the first turn or allowing the computer to play first.  Multiple board sizes are supported.

Implementation
--------------

The program is separated into client and server components. You can configure the hostname and port used for communication by editing config.py in the base directory.

The client is responsible for presenting the GUI to the user and contains the main game controller and logic for user input.

The server was designed to be stateless.  As input it expects a representation of the board as a string (e.g. 'XOOX XOXO') and returns the 'best move' calculated.  The client initiates the communication with a GET request containing the current state of the board as a query parameter.  The response is a string representation of the computers move.

The AI for the server is an implementation of the minimax algorithm using alpha-beta pruning.  For board sizes larger than 3x3 the depth of the search is reduced and preliminary scores are returned using a heuristic for the boards strength.  All server responses are cached.

Installation
============

The program uses a the following frameworks and libraries:

* Kivy_ is used for GUI, input, and client side network requests.
* Twisted_ is used by the server for networking.
* pydoctor_ is used for documentation generation.
* pytest_ is used as the test framework.

The program has been tested on Ubuntu 13.04 and Mac OSX 10.9.1.

Ubuntu
------

To install cd into the base directory and run:
    sudo ./install_ubuntu.sh

To uninstall run:
    sudo ./uninstall_ubuntu.sh

Mac OSX
-------

Installation should work on OSX 10.7+.

To install cd into the base directory and run:
    sudo ./install_mac.sh

To uninstall run:
    sudo ./uninstall_mac.sh

Usage
=====

From the base directory start the server:
    PYTHONPATH=. python server/main.py

From the base directory start the client:
    PYTHONPATH=. python client/main.py

Testing
=======

From the base directory:
    PYTHONPATH=. py.test -v test

Documentation
-------------

From the base directory:
    ./gen_docs.sh

Then open apidocs/index.html

.. _Kivy: http://www.kivy.org/
.. _Twisted: https://twistedmatrix.com/trac/
.. _pydoctor: https://launchpad.net/pydoctor
.. _pytest: http://pytest.org/latest/
