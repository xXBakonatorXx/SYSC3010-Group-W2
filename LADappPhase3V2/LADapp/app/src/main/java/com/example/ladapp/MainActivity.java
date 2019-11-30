package com.example.ladapp;

import java.net.*;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.Toast;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

//public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {
public class MainActivity extends AppCompatActivity {

    //Define UI Elements:
    private Switch enableSw;
    private Button btnS, btnF, btnB;
    private Spinner taskSpinner;
    private RecyclerView itemList;
    private RecyclerView.Adapter itemLocAdapter; //To get it to compile w/o implementing Adapter
    private RecyclerView.LayoutManager layoutManager;
    private String taskSearchKey;
    //Temporary Bogus Database data string arrays:
    private static final String[] tasks1 = {"Pills", "Thermometer", "TV Remote", "Ipad",
            "Phone", "House Keys"};
    private static final String[] item1 = {"HOME", "Node A", "Living Room", "Node C",
            "Kitchen", "Office", "Corridor", "HOME"};
    //Temp Bogus Cursor:
    //private Cursor databaseTasks, fetchTask;

    private String serverIP = "192.168.0.46";
    private DatagramSocket socket;

    private int serverPort = 510;
    private final int PACKETSIZE = 100;
    private InetAddress serverAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Initialize UI Elements:
        btnS = findViewById(R.id.btnStop);
        btnF = findViewById(R.id.btnForward);
        btnB = findViewById(R.id.btnBackward);
        enableSw = findViewById(R.id.enableSwitch);

        taskSpinner = findViewById(R.id.taskList);
        itemList = findViewById(R.id.itemLocList);
        itemList.setHasFixedSize(true); //Improves performance for constant layout sizes
        //use a linear layout manager:
        layoutManager = new LinearLayoutManager(this);
        itemList.setLayoutManager(layoutManager);
        //CursorAdapter taskAdapter = new CursorAdapter(this, databaseTasks, true);
        //CursorAdapter itemLocAdapter = new CursorAdapter(this, fetchTask, true);

        //Handle if either database tables are empty:
        if(tasks1.length==0)tasks1[0]="No Items";
        if(item1.length==0)item1[0]="No locations to display";
        //Create ArrayAdapters as temp substitutes for CursorAdapter:
        ArrayAdapter<String> taskAdapter = new ArrayAdapter<String>(this,
                R.layout.support_simple_spinner_dropdown_item, tasks1);
        //RecyclerView.Adapter itemLocAdapter = new RecyclerView.Adapter //Likely req. its own class
        //extension to implement this way. Maybe CursorAdapter will work w/o its own class ext?
        taskAdapter.setDropDownViewResource(R.layout.support_simple_spinner_dropdown_item);
        taskSpinner.setAdapter(taskAdapter);
        itemList.setAdapter(itemLocAdapter);
        taskSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                //Retrieve database information with this task Search Key.
                taskSearchKey = (String) parent.getItemAtPosition(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                //After no selection is made, close drop down menu???
            }
        });

        //Initially disable Manual Control UI Elements & Switch:
        enableSw.setChecked(false);
        enableManualControls(false);
        //Respond to switch being flipped:
        enableSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                enableManualControls(isChecked);
            }
        });
        //Respond to Emergency Stop being pressed:
        btnS.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                enableSw.setChecked(false);
                enableManualControls(false);
                //Send the Emergency Stop Command to the Server
                //Asdf...
            }
        });
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FloatingActionButton fab = findViewById(R.id.floatingActionButton);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /*Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();*/
                createNewTask(view); //Invoke start of createTask Activity
            }
        });
    }

    //Handle Call when the user taps the "New Scheduled Task" Button
    public void createNewTask(View view){
        Intent intent = new Intent(this, CreateTaskActivity.class);
        //add stuff here if you need to pull data from the main activity
        startActivity(intent);
    }

    public void driveForward(View view){
        //Send the drive forwards command to the server.
        sendCommand("manual:goForward");
    }

    public void driveBackward(View view){
        //Send the drive backwards command to the server.
        sendCommand("manual:goBackward");
    }

    public void stopDriving(View view) {
        //Send the stop driving command to the server.
        sendCommand("manual:stop");
    }

    public void fetchItem(String item) {
        sendCommand("item:" + item);
    }

    public boolean sendCommand(String msg) {
        try {
            serverAddress = InetAddress.getByName(serverIP);
            this.socket = new DatagramSocket();
            byte [] data = msg.getBytes();
            DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, this.serverPort);
            this.socket.send(packet);
            return true;
        } catch(Exception e) {
            Context context = getApplicationContext();
            CharSequence toastText = (CharSequence)e;
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, toastText, duration);
            toast.show();
            return false;
        }
    }

    public void enableManualControls(Boolean changeTo){
        //Enables all 3 Control UI Buttons
        btnB.setEnabled(changeTo);
        btnF.setEnabled(changeTo);
        btnS.setEnabled(changeTo);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

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
}
