package com.example.busylabs;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.android.volley.Request;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.Locale;

public class RoomActivity extends AppCompatActivity implements View.OnClickListener {

    TextView roomNameTextView;
    String roomName;
    ImageView roomMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);
        roomName = getIntent().getExtras().getString("roomName");
        roomNameTextView = findViewById(R.id.textView_room_name);
        roomNameTextView.setText(roomName);

        roomMap = findViewById(R.id.room_map);

        Drawable id = getResources().getDrawable(getResources().getIdentifier(roomName.toLowerCase()+"_map", "drawable", getPackageName()));

        roomMap.setImageDrawable(id);
        getRoomPopulation();
        findViewById(R.id.room_info).setVisibility(View.INVISIBLE);
        findViewById(R.id.room_progressBar).setVisibility(View.VISIBLE);
    }
    @Override
    public void onClick(View view) {
        onBackPressed();
    }

    public void updateTextViewRoomPopulation(String string) {
        TextView textView = findViewById(R.id.roomPopulation);
        textView.setText(string);
        findViewById(R.id.room_info).setVisibility(View.VISIBLE);
        findViewById(R.id.room_progressBar).setVisibility(View.GONE);
    }

//    public void showFriendsInRoom()

    public void getFriendsInRoom() {
        String FRIENDS_URL = "http://161.35.43.33:8000/friends";


        StringRequest request = new StringRequest(
                Request.Method.GET,
                FRIENDS_URL,
                this::updateTextViewRoomPopulation,
                Throwable::printStackTrace
        );
        Volley.newRequestQueue(getApplicationContext()).add(request);

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