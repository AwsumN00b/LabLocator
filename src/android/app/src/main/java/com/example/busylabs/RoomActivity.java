package com.example.busylabs;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class RoomActivity extends AppCompatActivity implements View.OnClickListener {

    TextView roomNameTextView;
    String roomName;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);
        roomName = getIntent().getExtras().getString("roomName");
        roomNameTextView = findViewById(R.id.textView_room_name);
        roomNameTextView.setText(roomName);
        getRoomPopulation();
    }

    @Override
    public void onClick(View view) {
        onBackPressed();
    }

    public void updateTextViewRoomPopulation(String string) {
        TextView textView = findViewById(R.id.roomPopulation);
        textView.setText(string);
    }

    public void getRoomPopulation() {
        String ROOM_DATA_URL = "http://161.35.43.33:8000/room/" + roomName;

        StringRequest request = new StringRequest(
                Request.Method.GET,
                ROOM_DATA_URL,
                this::updateTextViewRoomPopulation,
                Throwable::printStackTrace
        );

        Volley.newRequestQueue(getApplicationContext()).add(request);
    }
}