package com.example.busylabs;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class RoomActivity extends AppCompatActivity implements View.OnClickListener {

    TextView roomNameTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);
        String roomName = getIntent().getExtras().getString("roomName");
        roomNameTextView = findViewById(R.id.textView_room_name);
        roomNameTextView.setText(roomName);
    }

    @Override
    public void onClick(View view) {
        onBackPressed();
    }
}