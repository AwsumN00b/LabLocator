package com.example.busylabs;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.wifiscanner.ScanData;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    //    private final String ROOM_REQUEST_URL = "http://localhost:8000/room";

    private final List<String> permissions = Arrays.asList(
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_WIFI_STATE,
            Manifest.permission.CHANGE_WIFI_STATE,
            Manifest.permission.INTERNET
    );

    private String androidId;
    private boolean isGettingLocation = false;

    ScanThread scanThread;
    public String currentRoom = "";

    @SuppressLint("HardwareIds")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        checkPermissions();

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
        Button l129Button = findViewById(R.id.labListButtonL129);
        l129Button.setOnClickListener(this);
        Button l125Button = findViewById(R.id.labListButtonL125);
        l125Button.setOnClickListener(this);
        Button l128Button = findViewById(R.id.labListButtonL128);
        l128Button.setOnClickListener(this);
        Button lg27Button = findViewById(R.id.labListButtonLG27);
        lg27Button.setOnClickListener(this);

        FloatingActionButton friendsListButton = findViewById(R.id.friendsListButton);
        friendsListButton.setOnClickListener(this);

        //        setContentView(R.layout.activity_main);
        // above line prevents friends button from functioning correctly

        getBestRoomData();
    }



    @Override
    public void onClick(View view) {

        if (R.id.refreshRoomButton == view.getId()) {
            scanApList();
            return;
        } else if (R.id.friendsListButton == view.getId()){
            Intent friendsIntent = new Intent(this, FriendsActivity.class);
            startActivity(friendsIntent);
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

    public void updateTextViewLeastBusyLab(String string) {
        TextView textView = findViewById(R.id.quietRoomValueTextView);
        textView.setText(string.replace("\"", ""));
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
                updateUserCurrentRoom(scanData);
            } catch (JSONException | IOException e) {
                e.printStackTrace();
            }
            this.isGettingLocation = false;
        });

        thread.start();
    }

    public void updateUserCurrentRoom(ScanData scanData) throws IOException, JSONException {
        String ROOM_REQUEST_URL = "http://161.35.43.33:8000/room";
        List<String> aplist = scanData.toApListString();

        JSONObject jsonBody = new JSONObject();
        jsonBody.put("device_id", this.androidId);
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
                    updateTextViewCurrentLocation("N/A");
                    error.printStackTrace();
                }
        );

        Volley.newRequestQueue(getApplicationContext()).add(request);
    }

    public void getBestRoomData() {
        String ROOM_DATA_URL = "http://161.35.43.33:8000/room/quiet";

        StringRequest request = new StringRequest(
                Request.Method.GET,
                ROOM_DATA_URL,
                this::updateTextViewLeastBusyLab,
                Throwable::printStackTrace
        );

        Volley.newRequestQueue(getApplicationContext()).add(request);
    }

    private void checkPermissions() {
        for (String perm : this.permissions) {
            if (ActivityCompat.checkSelfPermission(this, perm)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{perm}, 1);
            }
        }
    }
}

