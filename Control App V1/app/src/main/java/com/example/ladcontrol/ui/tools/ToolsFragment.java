package com.example.ladcontrol.ui.tools;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;

import com.example.ladcontrol.R;
//Edited by: Brannon C. on 12th/11/2019
public class ToolsFragment extends Fragment {

    private ToolsViewModel toolsViewModel;
    private Switch enSw; //private
    private Button btnF, btnB, btnStop; //private

    //@Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        toolsViewModel =
                ViewModelProviders.of(this).get(ToolsViewModel.class);
        View root = inflater.inflate(R.layout.fragment_tools, container, false);
        final TextView textView = root.findViewById(R.id.text_tools);
        toolsViewModel.getText().observe(this, new Observer<String>() {
            @Override
            public void onChanged(@Nullable String s) {
                textView.setText(s);
            }
        });
        //root.setContentView(R.layout.fragment_tools);
        // Initialize the switch and other buttons
        btnF = (Button) root.findViewById(R.id.buttonUP);
        btnB = (Button) root.findViewById(R.id.buttonDOWN);
        btnStop = (Button) root.findViewById(R.id.buttonSTOP);
        enSw = (Switch) root.findViewById(R.id.enableSwitch);
        //Disable manual control initially
        enSw.setChecked(false);
        btnF.setEnabled(false);
        btnB.setEnabled(false);
        btnStop.setEnabled(false);
        //Respond to switch being flipped
        enSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked){
                btnF.setEnabled(isChecked); //Sexy code, doesn't need if statement :P
                btnB.setEnabled(isChecked);
                btnStop.setEnabled(isChecked);
            }});
        return root;
    }

    public void driveForward(View view){
        //Send the drive forwards command to the server.

    }

    public void driveBackward(View view){
        //Send the drive backwards command to the server.

    }

    public void emergencyStop(View view){
        //Sends an Emergency stop command to the server.
        //Do-something....
        //Also disables User Manual Control as a safety redundancy feature.
        enSw.setChecked(false);
        btnF.setEnabled(false);
        btnB.setEnabled(false);
        btnStop.setEnabled(false);
    }
}