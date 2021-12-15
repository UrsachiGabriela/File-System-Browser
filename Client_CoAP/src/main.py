from src.CoAP.CoAPclient import CoAPclient


if __name__=='__main__':


     client=CoAPclient(10002,'127.0.0.1')
     client.startConnection()
     client.run()
     #client.endConnection()

     # primire ACK -serial...???
     #daca raspunsul primit separat de ack este de tip con, ar trebui trimis un ack catre server?
     # pot retransmite un mesaj de tip non-confirmabil daca acesta contine o comanda ce asteapta date de la server??


     # port mapping/ forwarding


