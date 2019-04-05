A very basic implementation of the Red Badger Martian Robots coding challenge.

```
$ pipenv run python red_badger_bot.py
Mars size: 5 3
Starting coordinates and direction for robot #1: 1 1 E
Instructions for robot #1: RFRFRFRF
1 1 E
Starting coordinates and direction for robot #2: 3 2 N
Instructions for robot #2: FRRFLLFFRRFLL
3 3 N LOST
Starting coordinates and direction for robot #3: 0 3 W
Instructions for robot #3: LLFFFLFLFL
2 3 S
Starting coordinates and direction for robot #4: ^C
```

![CircleCI branch](https://img.shields.io/circleci/project/github/craiga/red-badger-bot/master.svg)


# Notes

 * The input requirements are *very* specific. Input must be *exactly* as it appeared in the PDF. I'd like to add some validation and error handling, but I ran out of time.
 * The program includes some prompts to make it a bit easier to tell which line of input is being entered.
 * The output of the program is interlaced with the input.
 * There's no validation of maximum values of coordinates or maximum lengths of instruction strings. I took those lines in the challenge to mean such validation was out of scope of this project.
 * To exit the program, press Control+C (or your operating system's keyboard interrupt key).


# Getting Started

```
pipenv install
pipenv run python red_badger_bot.py
```


# Running Tests

```
pipenv install --dev
pipenv run pytest
```


# Checking Code Quality

```
pipenv install --dev
pipenv run black --check .
pipenv run isort --check-only
find . -iname "*.py" | xargs pipenv run pylint
```
