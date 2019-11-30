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

public class CreateTaskActivity extends AppCompatActivity implements CompoundButton.OnCheckedChangeListener, View.OnClickListener {
    //Define this tasks UI elements:
    private ToggleButton sunBtn, monBtn, tuesBtn, wedBtn, thursBtn, friBtn, satBtn;
    private Button cancelBtn, createBtn;
    private EditText tskName, tskTime;
    private ListView dynamicTskList;
    //Define backend variables:
    private Integer newTaskDateBitMask;
    private String newTaskTime, newTaskName;

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
        dynamicTskList = findViewById(R.id.dynamicTaskLocList);
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

    //setup the ToggleButtons to the OnCheckedChangedListener
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

    @Override //Set up "Cancel" & "Create" button functionality
    public void onClick(View v) {
        //if(v.getId() == R.id.cancelButton) finish(); //finish calls onDestroy() for current activity
        if(v.getId() == R.id.createButton) createNewScheduledTask();
        finish();
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
