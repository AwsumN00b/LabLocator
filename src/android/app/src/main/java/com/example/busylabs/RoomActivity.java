package com.example.busylabs;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.ImageView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.JsonRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.util.Iterator;
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
        getFriendsInRoom();
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

    public void showFriendsInRoom(JSONObject json) {

        TableLayout table = findViewById(R.id.friendsInRoom);
        TableRow.LayoutParams rowParams = new TableRow.LayoutParams(
                TableRow.LayoutParams.WRAP_CONTENT,
                TableRow.LayoutParams.MATCH_PARENT
        );
        rowParams.setMargins(15, 15, 15, 15);

        Iterator<String> keys = json.keys();
        while (keys.hasNext()){
            String name = keys.next();
            TableRow t = new TableRow(this);
            TextView user = new TextView(this);
            try {
                String room = json.getString(name);
                if(room.equals(roomName)) {
                    table.setVisibility(View.VISIBLE);
                    findViewById(R.id.view2).setVisibility(View.VISIBLE);

                    user.setText(name);
                    user.setTextSize(25);
                    t.addView(user);
                    t.setLayoutParams(rowParams);
                    t.setGravity(Gravity.CENTER_HORIZONTAL);
                    table.addView(t);
                }
                } catch (JSONException e) {
                e.printStackTrace();
            }
        }

    }

    public void getFriendsInRoom() {
        String FRIENDS_URL = "http://161.35.43.33:8000/friends";

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.GET,
                FRIENDS_URL,
                null,
                this::showFriendsInRoom,
                error -> Toast.makeText(this, "ERROR", Toast.LENGTH_SHORT).show());
        Volley.newRequestQueue(getApplicationContext()).add(jsonObjectRequest);

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