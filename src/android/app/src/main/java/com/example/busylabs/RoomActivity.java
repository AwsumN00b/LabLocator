package com.example.busylabs;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class RoomActivity extends AppCompatActivity {

    TextView roomNameTextView = findViewById(R.id.textView_room_name);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);
        String roomName = getIntent().getExtras().getString("roomName");
        roomNameTextView.setText(roomName);
    }
}