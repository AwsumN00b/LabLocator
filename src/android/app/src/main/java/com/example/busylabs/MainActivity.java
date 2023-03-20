package com.example.busylabs;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    ScanThread scanThread;
    public String currentRoom = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        scanThread = new ScanThread(this);
        runScanThread();

        Button lg25Button = (Button) findViewById(R.id.labListButtonLG25);
        lg25Button.setOnClickListener(this);
        Button lg26Button = (Button) findViewById(R.id.labListButtonLG26);
        lg26Button.setOnClickListener(this);
        Button l101Button = (Button) findViewById(R.id.labListButtonL101);
        l101Button.setOnClickListener(this);
        Button l114Button = (Button) findViewById(R.id.labListButtonL114);
        l114Button.setOnClickListener(this);

        setContentView(R.layout.activity_main);

    }


    @Override
    public void onClick(View view) {

        Intent roomIntent = new Intent(this, RoomActivity.class);
        Bundle bundle = new Bundle();

        Button button = (Button) view;
        String roomName = button.getText().toString();

        bundle.putString("roomName", roomName);
        roomIntent.putExtras(bundle);
        startActivity(roomIntent);
    }


    public void updateTextViewCurrentLocation(String string) {
        TextView textView = findViewById(R.id.textViewCurrentLocation);
        textView.setText(string);
    }


    public void runScanThread() {
        scanThread.start();
    }
}