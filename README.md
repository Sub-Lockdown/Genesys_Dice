Genesys Dice Roller
==============================

A Python utility used for rolling special dice used in the Genesys roleplaying game, as well as standard polygon dice. Intended to be used in a future project, can be used as a standalone utlity.

Shoutout to stephenswat, whose Edge of the Empire ultility I shamelessly pulled to make this.

Usage
-----

To roll dice from the command line, invoke the Python as follows:

	python genesys_dice.py [pool] [difficulty] [upgrade]

Here, pool is a string representing the dice you want to roll. Each letter represents one die, as follows:

	b = Boost die
	s = Setback die
	a = Ability die
	d = Difficulty die
	p = Proficiency die
	c = Challenge die
	D = Standard die

As well, when rolling, you can select a difficulty level (a predetermined number of difficulty dice) as well as upgrading X number difficulty dice to Challenge dice (or adding additional difficulty dice, should there not be enough)

	Simple = -
    Easy = d
    Average = dd
    Hard = ddd
    Daunting = dddd
    Formidable = ddddd

To roll a standard n-sided die, use D followed by a number, like D20 to roll a 20-sided die.

Finally, to roll 2 ability dice, 1 boost die, and a D12 at Easy difficulty upgraded twice, you could use either of the following:

	python genesys_genesys_dice.py aabdcD12
	python genesys_dice.py aabD12 easy 2

Which might output the following:

	The roll succeeded with 1 success!
	The roll generated 1 threat.
	Your 12-sided die rolled 3.