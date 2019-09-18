/**
 * UDPSender sends n number of String "MessageN",
 * where N is the number of messages to the target 
 * IP via UDP Protocol.
 * @author Brannon Chan (#101045946)
 **/

import java.net.*;
import java.util.Scanner;

public class UDPSender {

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
			 int n			  = Integer.parseInt( args[2] );
	         socket = new DatagramSocket() ;
     
	         Scanner in; //Initialize scanner
	         in = new Scanner (System.in);
	         String message = null;
			 //String message = "Message";
			 int currentN = 1;
	         while ( currentN <= n )
	         {
	        		 //System.out.println("Enter text to be sent, ENTER to quit ");
	        		 //message = in.nextLine();
					 message = "Message" + String( currentN ); //Append the current message number to String message
	        		 //if (message.length()==0) break; //Now redudant break condition
	        		 byte [] data = message.getBytes() ;
	        		 DatagramPacket packet = new DatagramPacket( data, data.length, host, port ) ;
	        		 socket.send( packet ) ;
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

