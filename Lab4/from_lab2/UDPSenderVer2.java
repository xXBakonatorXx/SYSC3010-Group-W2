/**
 * UDPSender sends n number of String "MessageN",
 * where N is the number of messages to the target 
 * IP via UDP Protocol.
 * @author Brannon Chan (#101045946)
 **/

import java.net.*;
import java.util.Scanner;
import java.util.Random;
//Version 2 for lab 4
public class UDPSenderVer2 {
	
	private final static int PACKETSIZE = 100 ;
	
	public static void main(String[] args) 
   {
	      // Check the argument length
	      if( (args.length != 3) && (Integer.parseInt( args[2] ) > 0))
	      {
	         System.out.println( "usage: java UDPSender host port n, n>0" ) ;
	         return ;
	      }
	      DatagramSocket socket = null ;
	      try
	      {
	         // Convert the arguments first, to ensure that they are valid
	         InetAddress host = InetAddress.getByName( args[0] ) ;
	         int port         = Integer.parseInt( args[1] ) ;
		 int n            = Integer.parseInt( args[2] );
	         socket = new DatagramSocket() ;
     
	         Scanner in; //Initialize scanner
	         in = new Scanner (System.in);
	         String message;
			 //String message = "Message";
			 int currentN = 1;
	         while ( currentN <= n )
	         {
				Random r = new Random();
				message = String.valueOf(r.nextInt(100));
				
	        		 //System.out.println("Enter text to be sent, ENTER to quit ");
	        		 //message = in.nextLine();
					 //message = "Message" + new String( currentN ); //Append the current message number to String message
					 //System.out.println(currentN);
					 //System.out.println(message); //For debugging
					 //message = "Message";
					 //message += String.valueOf( currentN );
	        		 //if (message.length()==0) break; //Now redudant break condition
	        		 byte [] data = message.getBytes() ;
	        		 DatagramPacket packet = new DatagramPacket( data, data.length, host, port ) ;
	        		 socket.send( packet ) ;
					 currentN++;
					 
					 DatagramPacket msgAckPacket = new DatagramPacket ( new byte[PACKETSIZE], PACKETSIZE ) ;
					 socket.receive(msgAckPacket);
                     byte [] msgAckData = msgAckPacket.getData();
					 System.out.println( new String(msgAckData).trim() ) ; //Print acknowledgment msg
	         } 
	         System.out.println ("Closing down");
	      }
	      catch( Exception e )
	      {
	         System.out.println( e ) ;
	      }
	      finally
	      {
	         if( socket != null )
	            socket.close() ;
      }
   }
}

