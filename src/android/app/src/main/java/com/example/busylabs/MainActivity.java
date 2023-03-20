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
    Intent intent = new Intent(this, RoomActivity.class);

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

        switch (view.getId()) {
            case R.id.labListButtonLG25:
                launchRoomActivity("LG25");
            case R.id.labListButtonLG26:
                launchRoomActivity("LG26");
            case R.id.labListButtonL101:
                launchRoomActivity("L101");
            case R.id.labListButtonL114:
                launchRoomActivity("L114");
        }
    }


    public void updateTextViewCurrentLocation(String string) {
        TextView textView = findViewById(R.id.textViewCurrentLocation);
        textView.setText(string);
    }

    public void launchRoomActivity(String roomName) {
        Bundle bundle = new Bundle();
        bundle.putString("roomName", roomName);
        Intent intent = new Intent(MainActivity.this, RoomActivity.class);
        intent.putExtras(bundle);
        startActivity(intent);
    }

    public void runScanThread() {
        scanThread.start();
    }
}