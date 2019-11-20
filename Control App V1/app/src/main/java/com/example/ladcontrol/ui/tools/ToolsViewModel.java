package com.example.ladcontrol.ui.tools;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class ToolsViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public ToolsViewModel() { //Commented out from example app
        //mText = new MutableLiveData<>();
        //mText.setValue("This is tools fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}