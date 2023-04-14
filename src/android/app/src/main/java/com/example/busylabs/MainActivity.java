package com.example.busylabs;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.wifiscanner.ScanData;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private final String ROOM_REQUEST_URL = "http://161.35.43.33:8000/room";
//    private final String ROOM_REQUEST_URL = "http://localhost:8000/room";

    private String androidId;
    private boolean isGettingLocation = false;

    ScanThread scanThread;
    public String currentRoom = "";

    @SuppressLint("HardwareIds")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.androidId = Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);

        scanThread = new ScanThread(this);
        scanApList();

        ImageButton refreshRoomButton = findViewById(R.id.refreshRoomButton);
        refreshRoomButton.setOnClickListener(this);

        Button lg25Button = findViewById(R.id.labListButtonLG25);
        lg25Button.setOnClickListener(this);
        Button lg26Button = findViewById(R.id.labListButtonLG26);
        lg26Button.setOnClickListener(this);
        Button l101Button = findViewById(R.id.labListButtonL101);
        l101Button.setOnClickListener(this);
        Button l114Button = findViewById(R.id.labListButtonL114);
        l114Button.setOnClickListener(this);

        setContentView(R.layout.activity_main);

    }


    @Override
    public void onClick(View view) {

        if (R.id.refreshRoomButton == view.getId()) {
            scanApList();
            return;
        }

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


    public void scanApList() {

        if (this.isGettingLocation) {
            return;
        }

        Thread thread = new Thread(() -> {
            this.isGettingLocation = true;
            ScanData scanData = scanThread.getData();
            System.out.println(scanData.toString());
            try {
                getRoom(scanData);
            } catch (JSONException | IOException e) {
                e.printStackTrace();
            }
        });

        thread.start();
        this.isGettingLocation = false;
    }

    public void getRoom(ScanData scanData) throws IOException, JSONException {

        List<String> aplist = scanData.toApListString();

        JSONObject jsonBody = new JSONObject();
        jsonBody.put("device_id", "TEST_ID");
        jsonBody.put("timestamp", System.currentTimeMillis() / 1000);

        JSONArray jsonArray = new JSONArray();
        for (int i = 0; i < aplist.size(); i++) {
            jsonArray.put(aplist.get(i));
        }
        jsonBody.put("aplist", jsonArray);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.PUT,
                ROOM_REQUEST_URL,
                jsonBody,
                response -> {
                    try {
                        String room = response.getString("prediction");

                        updateTextViewCurrentLocation(room);
                        this.currentRoom = room;
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                },
                error -> {
                    updateTextViewCurrentLocation("ERROR");
                    error.printStackTrace();
                }
        );

        Volley.newRequestQueue(getApplicationContext()).add(request);
    }
}
