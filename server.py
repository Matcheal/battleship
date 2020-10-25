#!/usr/bin/env python3
import sys
import socket
import select
import battleshipBoard

HOST = ''
RECV_BUFFER = 4096
PORT = 9009

def server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                       #tworzenie socketu servera
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        # add server socket object to the list of readable connections
        # SOCKET_LIST.append(server_socket)

        print("Battleship server started on port  " + str(PORT))
        client_socket, addr = server_socket.accept()                                            #akceptowanie połączenia z klientem
        print("Client " + str(addr) + " connected")
        socket_list = [sys.stdin, client_socket]                                                #lista socketów do metody select()

        oponentBoard = battleshipBoard.Board()                                                  #inicjalizacja planszy przeciwnika
        localBoard = battleshipBoard.Board()                                                    #inicjalizacja planszy gracza
        localBoard.initShips("ready")                                                           #wpisanie położenia statków gracza
        lastGuessStack = list()                                                                 #stos przechowujący ostatnie zgadywane położenie
        client_socket.send(("Opponent ready!\n").encode("utf-8"))                               #wyślij wiadomość gotowości do przeciwnika

        print("Wait for your opponent to initiate their's ships.")

        while True:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block

            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)     #wybieranie albo gniazdo klienta lub std.input

            for sock in ready_to_read:
                if sock == client_socket:
                    # incoming message from remote server, s
                    data = sock.recv(4096)
                    if not data:
                        print('\nDisconnected from server')
                        sys.exit()
                    else:                                                                       # ODCZYT, obsługa odczytu wiadomości
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
                                client_socket.send(("Hit!\n").encode("utf-8"))
                                if localBoard.countSymbols(battleshipBoard.SHIP_SYMBOL) == 0:
                                    print("End of game, You LOST!")
                                    client_socket.send(("Game over.\n").encode("utf-8"))

                            else:
                                client_socket.send(("Missed!\n").encode("utf-8"))
                            print("-->Your turn!")
                            localBoard.yourTurn = True
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()

                else:                                                                           # ZAPIS, obsługa wysyłanej wiadomości
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
                                client_socket.send(msg.encode("utf-8"))
                                lastGuessStack.append(msg)  # w celu ustalenia kolejnosci
                                localBoard.yourTurn = False
                            else:
                                print("Wait for your turn!")
                        sys.stdout.write('[Me] ')
                        sys.stdout.flush()

        server_socket.close()

    except socket.error as e:
        print("Socket error({0}): {1}".format(e.errno, e.strerror))

    except KeyboardInterrupt:
        print("Closing server")
        client_socket.close()

    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


if __name__ == "__main__":
    sys.exit(server())
