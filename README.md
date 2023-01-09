Genesys Dice Roller
==============================

A Python utility used for rolling special dice used in the Genesys roleplaying game, as well as standard polygon dice. Intended to be used in a future project, can be used as a standalone utlity.

Shoutout to https://github.com/stephenswat/Edge-of-the-Empire-dice, whose Edge of the Empire ultility I shamelessly pulled to make this.

Usage
-----

This dice roller can either be used as a stand-alone dice rolling application invoked from a command line interface, or it can be imported and used from a different program.

To roll dice from the command line, invoke the Python as follows, all arguments can be shortened to their first letter, to make it easier to call:

	usage: dice.py [-h] -pool POOL [-difficulty DIFFICULTY] [-upgrade UPGRADE] [-symbols SYMBOLS [SYMBOLS ...]]

	optional arguments:
  	-h, --help            show this help message and exit
	-pool POOL            The pool of dice to roll
	-difficulty DIFFICULTY
	                    The difficulty pool, set to Simple (-) as default
	-upgrade UPGRADE      The number of difficulty dice to upgrade
	-symbols SYMBOLS [SYMBOLS ...]
                        Add additional symbols to your results

The pool argument is a string representing the dice you want to roll. To roll a standard n-sided die, use D followed by a number, like D20 to roll a 20-sided die. Each letter represents one die, as follows:

	a = Ability die
	b = Boost die
	c = Challenge die
	d = Difficulty die
	p = Proficiency die
	s = Setback die
	D = Standard die

The Difficulty argument allows you to select a difficulty level (a predetermined number of difficulty dice) as well as upgrading X number difficulty dice to Challenge dice (or adding additional difficulty dice, should there not be enough) by use of the Upgrade argument. The difficulty levels are as follows:

	Simple = -
    Easy = d
    Average = dd
    Hard = ddd
    Daunting = dddd
    Formidable = ddddd

Lastely, the Symbols argument can be used to add additional symbols to your dice pool. The following three-letter abbreviations are used: 
   
    suc = Success
    fai = Failure
    adv = Advantage
    thr = Threat
    tri = Triumph
    des = Despair

Finally, to roll 2 ability dice, 1 boost die, and a D12 at Easy difficulty upgraded twice, with a triumph added, you could use either of the following:

	python dice.py -pool aabdcD12 -symbols tri
	python dice.py -pool aabD12 -difficulty easy -upgrade 2 -symbols tri

Which might output the following:

	The roll succeeded with 1 success!
	The roll generated 1 threat.
	The roll generated 1 triumph!
	Your 12-sided die rolled 3.
