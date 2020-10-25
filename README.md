# battleships
An online battleships game, utilizing socket programming.  
## Features
* client.py - server program used for playing battleships game on separate terminals in the same network
* python 3
* Network Programming class project
* uses TCP

**Upgraded version of the game available in the repo :point_right: [_battleship_extended_](https://github.com/matplinta/battleship_extended)**
## Usage
* First, one of the players needs to start the `./server.py` script. Server by default starts on port `9009` and awaits for a client.
* A second player starts the  `client.py` program and connects to server via a specified port and a host name. Default values are `9009` for port and localhost address `127.0.0.1` for host.
* When the client has successfully connected to the server, a proper message is displayed and the game starts.
* First player to send a proper coordinates message starts the game. Coordinates should consist of a letter for a vertical axis and a number for horizontal axis, range **A - J** and **1 - 10**. The order (_letter, number_) should be of no significance.
* To check player board, type `player` into terminal. To check our current knowledge about the opponent board, type `opponent` and press enter.
```
[Me] C10
[Opponent] Missed!
[Me] player
+---+---+---+---+---+---+---+---+---+---+----+
|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
+---+---+---+---+---+---+---+---+---+---+----+
| A | o | o | o | o | _ | o | o | _ | _ | o  |
| B | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| C | o | o | o | _ | _ | _ | _ | _ | _ | _  |
| D | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| E | _ | o | _ | _ | _ | _ | _ | _ | _ | _  |
| F | _ | o | _ | _ | _ | _ | _ | _ | _ | _  |
| G | _ | _ | _ | _ | o | o | _ | _ | _ | _  |
| H | _ | _ | _ | _ | _ | _ | _ | _ | _ | o  |
| I | _ | _ | o | _ | _ | _ | _ | _ | _ | o  |
| J | o | _ | _ | _ | o | _ | _ | _ | _ | o  |
+---+---+---+---+---+---+---+---+---+---+----+
[Me] A1
[Opponent] Hit!
[Me] opponent
+---+---+---+---+---+---+---+---+---+---+----+
|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
+---+---+---+---+---+---+---+---+---+---+----+
| A | X | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| B | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| C | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| D | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| E | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| F | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| G | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| H | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| I | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
| J | _ | _ | _ | _ | _ | _ | _ | _ | _ | _  |
+---+---+---+---+---+---+---+---+---+---+----+

```