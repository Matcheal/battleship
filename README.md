# Features :sparkles:
* Client - server program used for playing Battleships game on separate terminals in the same network
* created using Python 3
* Network Programming class project
* Uses TCP


**Upgraded version of the game available in the repo :point_right: [_battleship_extended_](https://github.com/Matcheal/battleship_extended)**
# Usage
To start the server, one must execute server.py script. Server defaultly starts on port `9009` and awaits for a client. A client connects to server via a specified port and a host name. Default values are `9009` for port and localhost address `127.0.0.1` for host. When the client has successfully connected to the server, a proper message is displayed and the game has started. First player to send a proper coordinates message starts the game. Coordinates should consist of a letter for a vertical axis and a number for horizontal axis, range **A - J** and **1 - 10**. The order (_letter, number_) should be of no significance.


To check our board, type `player` into terminal. To check our current knowledge about the opponent board, type `opponent` and press enter.
