package com.example.busylabs;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

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
        scanButton = (Button) findViewById(R.id.button_scan);

        setContentView(R.layout.activity_main);
    }

    @Override
    public void onClick(View view) {

        scanThread.toggleThread();

        if (scanThread.isRunning()) {
//            this.scanButton.setText("Stop");
            scanThread.start();
            Toast.makeText(this, "Scan has begun!", Toast.LENGTH_SHORT).show();
        }
//        else {
////            this.scanButton.setText("Start");
//        }
    }


    public void updateTextView(String string) {
        TextView textView = (TextView) findViewById(R.id.textView);
        textView.setText(string);
    }
}