from src.CoAP.CoAPclient import CoAPclient


if __name__=='__main__':


     client=CoAPclient(10001,10002,'127.0.0.1')
     client.start_connection()
     client.run()
     #client.endConnection()

     # primire ACK -serial...???
     # ar trebui tratat cazul in care pt un request con primesc raspuns inainte de ACK ?  RASPUNS : da --> pun niste if-uri in primul while

     # utilizare coada
     # timeout

     #daca raspunsul primit separat de ack este de tip con, ar trebui trimis un ack catre server!!
     # pot retransmite un mesaj de tip non-confirmabil daca acesta contine o comanda ce asteapta date de la server??


     # interfata


     # server de test ?



     # port mapping/ forwarding


