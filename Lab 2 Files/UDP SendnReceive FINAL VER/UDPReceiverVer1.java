//Created by Erdem Yanikomeroglu & Brannon Chan

import java.net.*;

public class UDPReceiverVer1 {

    private final static int PACKETSIZE = 100 ;

    public static void main( String args[] ) {
        
        System.out.println("running");
        
	// Check the arguments
	if( args.length != 1 ) {
	    System.out.println( "usage: UDPReceiver port" ) ;
	    return ;
	}
        //DatagramSocket socket = null;
        //boolean running = true;
	try {
	    // Convert the argument to ensure that is it valid
	    int port = Integer.parseInt( args[0] ) ;

	    // Construct the socket
	    DatagramSocket socket = new DatagramSocket ( port );
            byte[] echoData = new byte[PACKETSIZE];
	    for( ;; ) {
		System.out.println( "Receiving on port " + port ) ;
		DatagramPacket packet = new DatagramPacket( new byte[PACKETSIZE], PACKETSIZE ) ;
	        socket.receive( packet ) ;

	        System.out.println( packet.getAddress() + " " + packet.getPort() + ": " + new String(packet.getData()).trim() ) ;
                String receiveString = new String(packet.getData());
                
                InetAddress echoAddress = packet.getAddress();
                int echoPort = packet.getPort();
				//System.out.println( echoPort );
                String echoString = "ACK: " + receiveString;
                echoData = echoString.getBytes();
                DatagramPacket sendPacket = new DatagramPacket(echoData, echoData.length, echoAddress, echoPort);
                
                
                //String received = new String(packet.getData(), 0, packet.getLength());
              
                    
                /*if (received.equals("end")) {
                    running = false;
                    continue;
                }*/
                socket.send(sendPacket);
	    }
                
	}
	catch( Exception e ){
	    System.out.println( e ) ;
	}
    }
}

