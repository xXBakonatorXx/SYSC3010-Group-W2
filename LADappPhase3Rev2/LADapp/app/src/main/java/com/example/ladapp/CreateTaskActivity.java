package com.example.ladapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ToggleButton;

/**
 * CreateTaskActivity is the Task Creation Activity
 * of the App. It is responsible for the initialization,
 * action, event handling, and backend elements that make up
 * the "Create New Scheduled Task Screen".
 *
 * @since October 19th, 2019
 * @author Brannon M. Chan (#101045946)
 * @version 3.3
 */
public class CreateTaskActivity extends AppCompatActivity implements CompoundButton.OnCheckedChangeListener, View.OnClickListener {

    //Define this tasks UI elements:
    private ToggleButton sunBtn, monBtn, tuesBtn, wedBtn, thursBtn, friBtn, satBtn;
    private Button cancelBtn, createBtn;
    private EditText tskName, tskTime;

    //Define backend variables:
    private Integer newTaskDateBitMask;
    private String newTaskTime, newTaskName;

    /**
     * Method onCreate is called upon the creation of CreateTaskActivity,
     * this method acts as this Class's constructor, as it
     * initializes & instantiates all of CreateTasActivity's Objects,
     * and sets all UI Event Listeners.
     *
     * @param savedInstanceState the Bundle Object containing its
     *                           last saved instance state.
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_task);

        //Initialize (hook-up) UI Elements:
        sunBtn = findViewById(R.id.sundayButton);
        monBtn = findViewById(R.id.mondayButton);
        tuesBtn = findViewById(R.id.tuesdayButton);
        wedBtn = findViewById(R.id.wednesdayButton);
        thursBtn = findViewById(R.id.thursdayButton);
        friBtn = findViewById(R.id.fridayButton);
        satBtn = findViewById(R.id.saturdayButton);
        cancelBtn = findViewById(R.id.cancelButton);
        createBtn = findViewById(R.id.createButton);
        tskName = findViewById(R.id.taskNameBox);
        tskTime = findViewById(R.id.taskTimeBox);

        //Hook up the ToggleButtons to the Listener
        sunBtn.setOnCheckedChangeListener(this);
        monBtn.setOnCheckedChangeListener(this);
        tuesBtn.setOnCheckedChangeListener(this);
        wedBtn.setOnCheckedChangeListener(this);
        thursBtn.setOnCheckedChangeListener(this);
        friBtn.setOnCheckedChangeListener(this);
        satBtn.setOnCheckedChangeListener(this);

        //Hookup Button listeners
        cancelBtn.setOnClickListener(this);
        createBtn.setOnClickListener(this);

        //Get the Intent that started this create task activity:
        Intent intent = getIntent();
        //You may now get whatever data you associated with the intent
    }

    /**
     * Method onCheckedChanged is the abstracted version of
     * each ToggleButton Object's setOnCheckedChangeListener
     * parameter, which is the date Button's Event Handler.
     * This is referenced in the setup method (onCreate).
     *
     * @param buttonView the CompoundButton Object that corresponds
     *                   to the original date ToggleButton Object pressed.
     * @param isChecked the Boolean value returned from our ToggleButton
     *                  Object's isChecked state.
     */
    @Override //Implement the ToggleButton Listener:
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
        newTaskDateBitMask = 0; //Clear bitmask. then set as appropriate:
        if(sunBtn.isChecked()) newTaskDateBitMask += 1000000;
        else if(monBtn.isChecked()) newTaskDateBitMask += 100000;
        else if(tuesBtn.isChecked()) newTaskDateBitMask += 10000;
        else if(wedBtn.isChecked()) newTaskDateBitMask += 1000;
        else if(thursBtn.isChecked()) newTaskDateBitMask += 100;
        else if(friBtn.isChecked()) newTaskDateBitMask += 10;
        else if(satBtn.isChecked()) newTaskDateBitMask += 1;
    }

    /**
     * Method onClick is the abstraced version of the
     * Event Handler for both the "Create" and "Cancel" UI Buttons.
     * @param view
     */
    @Override //Set up "Cancel" & "Create" button functionality
    public void onClick(View view) {
        if(view.getId() == R.id.createButton) createNewScheduledTask();
        finish(); //finish calls onDestroy() for current activity
    }

    public void createNewScheduledTask() {
        //Take User's specified data and send to the Server:
        //Get clients' data ready:
        newTaskTime = tskTime.getText().toString();
        newTaskName = tskName.getText().toString();
        //throw in newTaskDateBitmask
        //get a JSON Parser Object ready
        //Put the data in!
        //Send it!
    }

}
