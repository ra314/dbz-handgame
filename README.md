# dbz-handgame
## How to run
This requires running one instance of Server.py and two instances of Client.py. To progress through the menus hit enter. Sometimes it is required to hit enter, even if there is no prompt to do so.

## The origins
I used to play this game in school between grades 3-6. Mechanically it is quite similar to the shotgun handgame. But it is flaired with Dragon Ball style. I tried to recreate this game in python, although I have forgotten many of the attacks that were possible for the game.

## The rules
This game is turn based simultaneous, just like rock paper scissors. The actions you can perform are dodge, block, charge or attack. Each attack has a number of required charges (to perform), and an evasion mechanism (either dodging or charging). If you are hit by any attack, you lose all of the charges you held. If both players try to attack eachother on the same turn, both attacks occur successfully and then their charges are set to zero.

| Attack Name     | Charges Needed | Evasion Mechanism |
|-----------------|----------------|-------------------|
| Kamehameha      | 1              | Dodging           |
| Sayonara        | 2              | Blocking          |
| Spin Kamehameha | 3              | Blocking          |
