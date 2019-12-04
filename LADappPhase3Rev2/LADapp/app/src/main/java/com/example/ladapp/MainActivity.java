package com.example.ladapp;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import static java.lang.Integer.toHexString;

/**
 * MainActivity is the default Activity of the App.
 * It is responsible for the initialization, action,
 * event handling, and backend elements that make up
 * the "Home Screen".
 *
 * @since October 19th, 2019
 * @author Brannon M. Chan (#101045946)
 * @author Erdem Yanikomeroglu (#101080085)
 * @version 3.5
 */
public class MainActivity extends AppCompatActivity {

    //Define UI Elements:
    private Switch enableSw;
    private Button btnS, btnF, btnB, btnWUp, btnWDown, btnWReset, btnAUp, btnADown, btnAReset, btnRunTask, btnClawT, btnClawR;
    private Spinner taskSpinner;
    private TextView commandStatusLabel;
    private String taskSearchKey;

    //Save Emergency Button State before entering Asynctask thread:
    private boolean prevEmergButtonState;

    //Temporary Bogus Database data string arrays:
    private static final String[] tasks1 = {"cup_d0", "cup_b0", "cup_d1", "cup_b1",
            "Phone", "House Keys"};
    private static final String[] item1 = {"HOME", "Node A", "Living Room", "Node C",
            "Kitchen", "Office", "Corridor", "HOME"};

    //Define Manual Drive Command String Constants:
    private final String stopMsg = "0x000";
    private final String fwdMsg = "0x100";
    private final String turnLeftMsg = "0x080";
    private final String turnRightMsg = "0x040";
    private final String armUpMsg = "0x020";
    private final String armDownMsg = "0x010";
    private final String wristUpMsg = "0x008";
    private final String wristDownMsg = "0x004";
    private final String clawOpenMsg = "0x002";
    private final String clawCloseMsg = "0x001";

    /**
     * Method onCreate is called upon the creation of MainActivity,
     * this method acts as this Class's constructor, as it
     * initializes & instantiates all of MainActivity's Objects,
     * and sets all UI Event Listeners.
     *
     * @param savedInstanceState the Bundle Object containing its
     *                           last saved instance state.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Initialize MainActivity UI Elements:
        btnS = findViewById(R.id.btnStop);
        btnF = findViewById(R.id.btnForward);
        btnB = findViewById(R.id.btnTurnLeft);
        enableSw = findViewById(R.id.enableSwitch);
        commandStatusLabel = findViewById(R.id.commandStatusFieldText);
        btnWUp = findViewById(R.id.wristUpButton);
        btnWDown = findViewById(R.id.wristDownButton);
        btnWReset = findViewById(R.id.resetWristPitchButton);
        btnAUp = findViewById(R.id.raiseArmButton);
        btnADown = findViewById(R.id.lowerArmButton);
        btnAReset = findViewById(R.id.resetElevationButton);
        btnRunTask = findViewById(R.id.runTaskNow);
        btnClawT = findViewById(R.id.clawTButton);
        btnClawR = findViewById(R.id.clawRButton);
        taskSpinner = findViewById(R.id.itemList);

        //Presently set reset buttons as Disabled no existing resetopcode


        //Handle if either database tables are empty:
        if(tasks1.length==0)tasks1[0]="No Items";
        if(item1.length==0)item1[0]="No locations to display";
        //Create ArrayAdapters as temp substitutes for CursorAdapter:
        ArrayAdapter<String> taskAdapter = new ArrayAdapter<String>(this,
                R.layout.support_simple_spinner_dropdown_item, tasks1);
        taskAdapter.setDropDownViewResource(R.layout.support_simple_spinner_dropdown_item);
        taskSpinner.setAdapter(taskAdapter);
        taskSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                //Retrieve database information with this task Search Key.
                taskSearchKey = (String) parent.getItemAtPosition(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                taskSearchKey = null;
            }
        });

        //Initially disable Manual Control UI Elements, Status & Switch:
        enableSw.setChecked(false);
        setEnableManualControls(false);
        commandStatusLabel.setText(getResources().getText(R.string.commandStatusIdle));
        //Respond to switch being flipped:
        enableSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                prevEmergButtonState = isChecked; //Save enable switch state for AsyncTask Thread
                setEnableManualControls(isChecked);
            }
        });
        //Respond to Emergency Stop being pressed:
        btnS.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                enableSw.setChecked(false);
                setEnableManualControls(false);
                //Send the Emergency Stop Command to the Server
                try {
                    emergencyStop();
                } catch (IOException e){
                    dispToast(e.toString());
                }
            }
        });
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FloatingActionButton fab = findViewById(R.id.newItemButton);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                createNewTask(view); //Invoke start of createTask Activity
            }
        });
    }

    /**
     * Method dispToast is a debugging method
     * used to output certain messages being
     * tested by the developer, or to output
     * error messages and exceptions to the
     * screen.
     *
     * @param message the String object to be
     *                displayed on the UI.
     */
    public void dispToast(String message){
        //Initiate Toast with Exception Msg:
        Toast toast = Toast.makeText(getApplicationContext(), message, Toast.LENGTH_LONG);
        toast.setGravity(Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL, 0, 0);
        toast.show(); //Display the exception msg
    }

    /**
     * Method createNewTask is called when the User taps
     * the "New Scheduled Task" UI Button. This cause a new
     * activity (from "CreateNewTask.Java") to Start.
     *
     * @param view the FloatingActionButton View Object that
     *             corresponds to the "+" symbol UI button.
     */
    public void createNewTask(View view){
        Intent intent = new Intent(this, CreateTaskActivity.class);
        //add stuff here if you need to pull data from the main activity
        startActivity(intent);
    }

    /**
     * Method driveForward is called upon the User tapping
     * or holding the "Forward" drive button on the UI.
     * This will send the "Drive Forward" command to the
     * LAD Unit Via the Central Server.
     *
     * @param view the Button View Object corresponding to
     *             the "FORWARD" UI Button.
     * @throws IOException the Exception Object thrown
     *                     due to a network error.
     */
    public void driveForward(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(fwdMsg);
        //dispToast(fwdMsg);
    }

    public void runTaskNow(View view) throws IOException {  //////////////////////
        //Send the drive forwards command to the server.
        sendCommand(taskSearchKey);
        //dispToast(fwdMsg);
    }

    public void driveLeft(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(turnLeftMsg);
        //dispToast(fwdMsg);
    }

    public void driveRight(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(turnRightMsg);
        //dispToast(fwdMsg);
    }

    public void moveUpArm(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(armUpMsg);
        //dispToast(fwdMsg);
    }

    public void moveDownArm(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(armDownMsg);
        //dispToast(fwdMsg);
    }

    public void moveWristUp(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(wristUpMsg);
        //dispToast(fwdMsg);
    }

    public void moveWristDown(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(wristDownMsg);
        //dispToast(fwdMsg);
    }

    public void openClaw(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(clawOpenMsg);
        //dispToast(fwdMsg);
    }

    public void closeClaw(View view) throws IOException {
        //Send the drive forwards command to the server.
        sendCommand(clawCloseMsg);
        //dispToast(fwdMsg);
    }

    /**
     * Method emergencyStop() is called when the User
     * taps the "Stop Moving" drive button in the UI.
     * This will send a "Halt" message to the LAD Unit
     * via Central Server.
     * @throws IOException the Exception Object thrown
     *                     due to a network error.
     */
    public void emergencyStop() throws IOException {
        //Send the emergency stop command to the LAD
        sendCommand(stopMsg);
        //dispToast(stopMsg);
    }

    /**
     * Method fetchItem() is called when the User
     * taps the "Fetch" drive button in the UI.
     * This will send a "Fetch Item" message to the LAD Unit
     * via Central Server.
     * NOTE: This method may be depricated and is for dev use only.
     * @throws IOException the Exception Object thrown
     *                     due to a network error.
     */
    /**public void fetchItem(String item) throws IOException{ //Implements IOException?
        //Send fetch command to the LAD
        String fetchMsg = "item:" + item;
        sendCommand(fetchMsg);
        //dispToast(fetchMsg);
    }*/

    /**
     * Method sendCommand takes the text or
     * exception error message given to it as input
     * and sends the command via Wireless UDP to
     * the Central Server.
     * @param msg the String Command to send to server.
     * @throws IOException the Exception Object thrown
     *                     due to a network error.
     */
    public void sendCommand(String msg) throws IOException{
        try {
            //Attempt sending the given command:
            dispToast(msg);
            new NetworkingAsyncTask().execute(msg);
            //Set the command status back to Idle message:
            commandStatusLabel.setText(getResources().getText(R.string.commandStatusIdle));
        } catch(Exception e) {
            e.printStackTrace();
            dispToast(e.toString());
        }
    }

    /**
     * Method setEnableManualControls is used to enable or
     * disable the FORWARD, BACKWARD, and STOP MOVING
     * UI Button Elements as a redundant safety feature
     * when the STOP MOVING Button is tapped/pressed.
     * @param changeTo the Boolean value to set Manual Drive
     *                 Control Buttons to.
     */
    public void setEnableManualControls(Boolean changeTo){
        //Enables all Control UI Buttons
        btnB.setEnabled(changeTo);
        btnF.setEnabled(changeTo);
        btnS.setEnabled(changeTo);
        //Other UI Elements:
        btnADown.setEnabled((changeTo));
        btnAReset.setEnabled((changeTo));
        btnAUp.setEnabled((changeTo));
        btnWDown.setEnabled((changeTo));
        btnWReset.setEnabled((changeTo));
        btnWUp.setEnabled((changeTo));
        btnClawR.setEnabled((changeTo));
        btnClawT.setEnabled((changeTo));
        btnClawT.setEnabled((changeTo));
    }

    /**
     * Method onCreateOptionsMenu was an autogenerated
     * event handling method that handles the default
     * "Settings" menu feature.
     * Consider DEPRECATING.
     *
     * @param menu the corresponding Menu Object
     * @return Always returns true.
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    /**
     * Method onOptionsItemSelected was an autogenerated
     * even handling method that handles the default
     * "Settings" Menu feature.
     * Consider DEPRECATING.
     *
     * @param item the MenuItem Object
     * @return true - If item's id matches
     *                "...action_settings".
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    //Class to handle networking thread
    //Implement the AsyncTask class for networking functionality:
    private class NetworkingAsyncTask extends AsyncTask<String, String, String> {

        //Define Android Networking Capability:
        private DatagramSocket UDPsocket;
        private DatagramPacket UDPpacket;

        //Define Network Parameters:
        private final int serverPort = 8888;
        private final String serverIP = "192.168.31.126";
        private InetAddress serverAddress;
        private byte [] data;
        private String commMsg, result;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            //Show the user is sending the command and disable send functions until completed:
            commandStatusLabel.setText(getResources().getText(R.string.commandStatusPreExec));
            setEnableManualControls(false);
        }

        @Override
        protected String doInBackground(String... param) {
            //Show the user this new status
            commMsg = param[0]; //Assuming this is how you get the sendCommand Input
            result = "s"; //Init the result from Asynctask
            try { //Ported over from method sendCommand
                //Set server IP
                serverAddress = InetAddress.getByName(serverIP);
                UDPsocket = new DatagramSocket();
                data = commMsg.getBytes();
                UDPpacket = new DatagramPacket(this.data, data.length, serverAddress, this.serverPort); //this.serverPort
                UDPsocket.send(UDPpacket);
            } catch(Exception e) {
                e.printStackTrace();
                result = "f"; //Set task successful flag as failed
            } //Return the data to onPostExecute method
            return result + commMsg;
        }

        //@Override //"method does not override its superclass"
        //protected void onProgressUpdate() { //Do something with this?
            //commandStatusLabel.setText(getResources().getText(R.string.commandStatusBackGround));
            //dispToast(UDPpacket.getAddress().toString());
        //}

        @Override
        protected void onPostExecute(String backResult) {
            super.onPostExecute(backResult);
            if('f' == backResult.charAt(0)){
                commandStatusLabel.setText((CharSequence) (backResult.substring(1) + " " + getResources().getText(R.string.commandStatusPostExecFail)));
            } else {
                commandStatusLabel.setText((CharSequence) (backResult.substring(1) + " " + getResources().getText(R.string.commandStatusPostExecPass)));
            }
            setEnableManualControls(prevEmergButtonState);
        }
    }
}
