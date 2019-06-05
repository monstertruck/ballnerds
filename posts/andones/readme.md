# How many and-ones does a team get in a year?
andones is a python script that counts the number of 'and-one' basketball plays accomplished by a given NBA team in the 2018-2019 season and outputs an image file describing the results.

## Description
This was an old idea I had kicking around - can we count up the number of and-ones (converted free throws making three- and four-point plays) from game flow/play-by-play data? I was originally going to scrape ESPN/NBA game log data but found that the mysportsfeeds (mysportsfeeds.com/data-feeds) API delivers a JSON game log that works well.

The "user" can choose the team (three character abbreviation) and the number of games (right now it's the first X number of games) from the 2018-2019 season and the ultimate output is a 'shot chart' of converted field goals and the number of total and-ones over the time span for each player. These results are subject to the accuracy of the mysportsfeeds API.

### Let's define an And-1:
And-ones in basketball are when:
1. A made free throw follows a made basket (field goal): made basket + immediate shooting foul (same timestamp)
2. For now, we'll allow the rare teammate and-one (where a foul is called away from the shooter but at the same time as the made field goal)
3. There are edge cases that I'm not sure about - such as when there are double-fouls or multiple fouls called. These _should_ be counted.


## Running
There are a couple options. There is makefile where you can:
```
make build
python andones.py --team [ABB] --games [# of games]
```
If you don't want a particular team, running `python andones.py` without arguments will pick a random team and select all 82 games of the 2018-2019 regular season. Running
```
make run
```
will default to this option.

### Output
The output of the script is a `.png` image file that depicts the locations of each of the _shots_ that led to and-one plays (the free throws are all taken at the free throw line), along with the identities of the players that converted those shots and free throws. The player legend also tells the user how many such plays each player on the team of interest converted.

### Author
David Kang