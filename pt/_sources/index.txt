Trader Calculator
=================
    - *Documentation also available in:* `Português <../pt/index.html>`_
      |portugal|
    - *Download the latest version for your platform at* `github 
      <https://github.com/ffunenga/traderCalculator/tree/master/deploy/dist>`_

.. |portugal| image:: images/pt.png
.. |england| image:: images/en.png

Introduction
------------
This application is a simple tool for users of betting exchanges and 
it is meant to solve the well-known problem of *Bet-Hedging*: 
configure the profit/losses of two bets - a back and a lay bet - for 
all outcomes.

.. image:: images/bias-ubuntu-en.png
    :align: center

The main objective in its development was to guarantee the 
possibility of using solely the keyboard fast and efficiently. 
Obviously, their exists other solutions of the same kind [1]_ [2]_ 
[3]_ but all have problems: they depend on the web-browser, none 
allows keyboard devotion, amongst others.

This calculator is an open-source project (GPLv2) and 
cross-platform. It is implemented as free software aiming to be 
executed in all platforms supported by wxPython [4]_.

.. [1] http://www.arbcruncher.com/
.. [2] http://www.betcalc.com/backlaycalc.php
.. [3] http://www.oddschecker.com/betting-tools/hedging-calculator.htm
.. [4] http://www.wxpython.org/

Documentation
-------------
.. toctree::
    :maxdepth: 3
    
    tutorial
    theory

Development
-----------
Suggestions, comments or reviews are welcome! You can send them to filipe.funenga@ist.utl.pt. Also, if you find bugs please create an issue at github [5]_ or send me an email.

The development of this application started in 23/Dec/2012 and has been made in Ubuntu 12.04 with Virtualbox running Windows 7.

In its current state, a macintosh build is not yet available since I have not immediate access to a macintosh machine. But do not worry, deployment to that framework will be done in the near future.

.. [5] https://github.com/ffunenga/traderCalculator/issues
