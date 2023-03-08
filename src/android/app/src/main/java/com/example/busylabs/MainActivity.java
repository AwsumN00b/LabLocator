package com.example.busylabs;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    ScanThread scanThread;
    Button scanButton;
    public String room = "LG27";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        scanThread = new ScanThread(this);

        Button lg25Button = (Button) findViewById(R.id.labListButtonLG25);
        lg25Button.setOnClickListener(this);
        Button lg26Button = (Button) findViewById(R.id.labListButtonLG26);
        lg26Button.setOnClickListener(this);
        Button l101Button = (Button) findViewById(R.id.labListButtonL101);
        l101Button.setOnClickListener(this);
        Button l114Button = (Button) findViewById(R.id.labListButtonL114);
        l114Button.setOnClickListener(this);

        scanThread.toggleThread();
        setContentView(R.layout.activity_main);
    }

    @Override
    public void onClick(View view) {

        switch (view.getId()) {
            case R.id.labListButtonLG25:
                // goto fragment
            case R.id.labListButtonLG26:
                // goto fragment
            case R.id.labListButtonL101:
                // goto fragment
            case R.id.labListButtonL114:
                // goto fragment
        }

    }


    public void updateTextViewCurrentLocation(String string) {
        TextView textView = findViewById(R.id.textViewCurrentLocation);
        textView.setText(string);
    }
}