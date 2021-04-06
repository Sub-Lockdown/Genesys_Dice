import random
import sys
import re
import argparse

### Gensys Dice Symbols ###
SUCCESS = {"success": 1}
ADVANTAGE = {"advantage": 1}
TRIUMPH = {"success": 1, "triumph": 1}
FAILURE = {"success": -1}
THREAT = {"advantage": -1}
DESPAIR = {"success": -1, "despair": 1}
BLANK = {}

### Gensys Dice ###
DIE_OPTIONS = {
    "b": ((BLANK),(BLANK),(SUCCESS,),(SUCCESS, ADVANTAGE,),(ADVANTAGE, ADVANTAGE,),(ADVANTAGE,)),
    "s": ((BLANK),(BLANK),(FAILURE,),(FAILURE,),(THREAT,),(THREAT,),),
    "a": ((BLANK),(SUCCESS,),(SUCCESS,),(SUCCESS, SUCCESS,),(ADVANTAGE,),(ADVANTAGE,),(SUCCESS, ADVANTAGE,),(ADVANTAGE, ADVANTAGE,),),
    "d": ((BLANK),(FAILURE,),(FAILURE, FAILURE,),(THREAT,),(THREAT,),(THREAT,),(THREAT, THREAT,),(FAILURE, THREAT,)),
    "p": ((BLANK),(SUCCESS,),(SUCCESS,),(SUCCESS, SUCCESS),(SUCCESS, SUCCESS),(ADVANTAGE,),(SUCCESS, ADVANTAGE),(SUCCESS, ADVANTAGE),(SUCCESS, ADVANTAGE),(ADVANTAGE, ADVANTAGE),(ADVANTAGE, ADVANTAGE),(TRIUMPH,)),
    "c": ((BLANK),(FAILURE,),(FAILURE,),(FAILURE, FAILURE,),(FAILURE, FAILURE,),(THREAT,),(THREAT,),(FAILURE, THREAT,),(FAILURE, THREAT,),(THREAT, THREAT,),(THREAT, THREAT,),(DESPAIR,))
}

### Difficulty Levels ###
DIFFICULTY = {
    "simple": (),
    "easy": ("d"),
    "average": ("dd"),
    "hard": ("ddd"),
    "daunting": ("dddd"),
    "formidable": ("ddddd"),
}

class DicePool(object):
    """
    Class representing a pool of dice to be rolled by the script. Stores a dict
    representing the current roll. Has a roll() function which (re)rolls all
    dice in the pool and an internal function __add_results(results) which adds
    a set of results to the value of the current pool.
    """

    __value = {}

    def __init__(self, dice_pool):
        self.dice = re.findall(r"([A-Za-z])(\d+)?", dice_pool)

        for die in self.dice:
            if not die[0] in list(DIE_OPTIONS.keys()) + ["D"]:
                raise ValueError("Invalid die type supplied. Valid dice are: " + ", ".join(list(DIE_OPTIONS.keys()) + ["D"]))

    def __add_results(self, results):
        """
        Takes a set of results as a dictionary (or tuple for custom dice) and
        adds then to the current value of the dice pool.

        input: A dictionary of results.
        output: None, but __value is updated.
        """
        for res in results:
            if isinstance(res, dict):
                for key in res.keys():
                    if key in self.__value.keys():
                        self.__value[key] += res[key]
                    else:
                        self.__value['custom'].append((key, res[key]))
            else:
                raise ValueError("Illegal result type.")

    def reset_results(self):
        """
        Resets the value of __value to all zero.

        input: None.
        output: None, but resets __value.
        """

        self.__value = {
            "success":   0,
            "advantage": 0,
            "triumph":   0,
            "despair":   0,
            "custom":    [],
            "custom_mod": 0
        }

    def roll(self):
        """
        Rolls all dice in this pool and adds the results to the value of the
        dice pool.

        input: None.
        output: None.
        """

        self.reset_results()

        for die in self.dice:
            results = Die(die).roll()
            self.__add_results(results)

    def get_values(self):
        """
        Returns a complete list of dice pool values, including failure and
        threat.

        input: None.
        output: The value of the dice pool after (re)rolling all dice.
        """
        values = self.__value.copy()

        values['failure'] = -values['success']
        values['threat'] = -values['advantage']

        return values

class Die(object):
    """
    Shortlived class that respresents a rollable die. Has a type of die which
    is represented as a tuple.
    """

    def __init__(self, die_type):
        self.die_type = die_type

    def roll(self):
        """
        Rolls this die and retuns the value of the roll as a tuple.

        input: None.
        output: The result of the roll as a dictionary.
        """
        if self.die_type[0] == "D":
            return ({self.die_type[0] + self.die_type[1]:random.randint(1, int(self.die_type[1]))},)
        else:
            return random.choice(DIE_OPTIONS[self.die_type[0]])

def roll_string(info):
    """
    Creates a dice pool from an input string, rolls it and returns the result.

    input: A string representing a dice pool.
    output: The result of the dice pool when rolled.
    """
    diff_pool = DIFFICULTY[info['difficulty'].lower()]
    if info['upgrade'] != None:
        upgrades = info['upgrade']
        if upgrades > len(diff_pool):
            diff_pool = "c"*len(diff_pool) + "d"*(upgrades - len(diff_pool))
        else:
            diff_pool = "c"*upgrades + "d"*(len(diff_pool) - upgrades)
    pool = DicePool(info["pool"] + str(diff_pool))
    pool.roll()
    return (pool.get_values(), info['symbols'])

def adding_symbols(results):
    final_pool, symbols = results
    options = {"suc" : 'success', 
        "fai" : 'failure', 
        "adv" : 'advantage',
        "thr" : 'threat',
        "tri":  'triumph',
        "des": 'despair'}
    if symbols:
        for i in symbols:
            try:
                final_pool['custom_mod'] += int(i)
            except:
                final_pool[options[i]] += 1
    return final_pool


def display_results(results):
    """
    Prints some human-readable information about the results of a dice roll,
    like if it succeeded, if it generated threat, advantage, triumph, despair,
    Also prints the values of any custom dice.

    input: A dictionary of results.
    output: Some printed information about the roll.
    """
    if results['success'] < 0:
        print("The roll failed with {failure} failure.".format(**results))
    elif results['success'] == 0:
        print("The roll failed with {success} success!".format(**results))
    else:
        print("The roll succeeded with {success} success!".format(**results))

    if results['advantage'] > 0:
        print("The roll generated {advantage} advantage!".format(**results))
    elif results['advantage'] < 0:
        print("The roll generated {threat} threat!".format(**results))

    if results['despair'] > 0:
        print("The roll generated {despair} despair..".format(**results))
    if results['triumph'] > 0:
        print("The roll generated {triumph} triumph!".format(**results))
    
    if results['custom']:
        custom_total = 0
        for custom_roll in results['custom']:
            if len(results['custom']) == 1 and results['custom_mod'] > 0:
                print("Your %s-sided die rolled %d, with a %d modifier, for a total of %d." % (custom_roll[0][1:], custom_roll[1], results['custom_mod'], (custom_roll[1] + results['custom_mod'])))
                break
            print("Your %s-sided die rolled %d." % (custom_roll[0][1:], custom_roll[1]))
            custom_total += custom_roll[1]
        if len(results['custom']) > 1 and results['custom_mod'] > 0:
            print("The total of your dice roll is %s, with a %d modifier." % ((custom_total + results['custom_mod']), results['custom_mod']))
        elif len(results['custom']) > 1:
            print("The total of your dice roll is %s." % ((custom_total + results['custom_mod'])))


def main(arguments):
    args = arguments.parse_args()
    if vars(args)['difficulty'] in DIFFICULTY.keys():
        display_results(adding_symbols(roll_string(vars(args))))
    else:
        print("Error, incorrect difficulty selected")   

def parser():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-pool', action='store', type=str, required=True, help='The pool of dice to roll')
    my_parser.add_argument('-difficulty', action='store', default='simple', type=str, help='The difficulty pool, set to Simple (-) as default')
    my_parser.add_argument('-upgrade', action='store', type=int, help="The number of difficulty dice to upgrade")
    my_parser.add_argument('-symbols', nargs='+', action='store', help='Add additional symbols to your results')
    return my_parser

if __name__ == '__main__':
    arguments = parser()
    main(arguments)

