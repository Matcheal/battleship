import sys
import socket
import select
import battleshipBoard


def client():
    host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9009
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. You can start playing.')

    oponentBoard = battleshipBoard.Board()
    localBoard = battleshipBoard.Board()
    localBoard.initShips("short")
    lastGuessStack = list()
    s.send(("Opponent ready!\n").encode("utf-8"))
    print("Wait for your opponent to initiate their's ships.")

    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from server')
                    sys.exit()
                else:  # ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT__ODCZYT
                    # print data
                    readableData = data.decode("utf-8")[0:-1]
                    sys.stdout.write("\r[Opponent] ")
                    sys.stdout.write(data.decode("utf-8"))
                    sys.stdout.flush()

                    if readableData == "Hit!":
                        oponentBoard.insertByCoor(lastGuessStack.pop(), battleshipBoard.HIT_SYMBOL)
                    elif readableData == "Missed!":
                        oponentBoard.insertByCoor(lastGuessStack.pop(), battleshipBoard.MISSED_SYMBOL)
                    elif readableData == "Game over.":
                        print("You WON!")
                        exit()
                    elif readableData == "Opponent ready!":
                        continue
                    else:
                        if localBoard.ifHit(readableData):
                            s.send(("Hit!\n").encode("utf-8"))
                            if localBoard.countSymbols(battleshipBoard.SHIP_SYMBOL) == 0:
                                print("End of game, You LOST!")
                                s.send(("Game over.\n").encode("utf-8"))

                        else:
                            s.send(("Missed!\n").encode("utf-8"))
                        print("-->Your turn!")
                        localBoard.yourTurn = True
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

            else:  # ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS__ZAPIS
                # user entered a message
                msg = sys.stdin.readline()

                if str(msg) == "player\n":
                    localBoard.print()
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
                elif str(msg) == "opponent\n":
                    oponentBoard.print()
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
                else:
                    if oponentBoard.validCoor(msg.rstrip()):
                        if localBoard.yourTurn:
                            s.send(msg.encode("utf-8"))
                            lastGuessStack.append(msg)  # w celu ustalenia kolejnosci
                            localBoard.yourTurn = False
                        else:
                            print("Wait for your turn!")
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(client())
