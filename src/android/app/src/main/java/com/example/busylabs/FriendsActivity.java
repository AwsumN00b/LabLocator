package com.example.busylabs;

import android.annotation.SuppressLint;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Iterator;

public class FriendsActivity extends AppCompatActivity implements View.OnClickListener {

    String FRIENDS_URL = "http://161.35.43.33:8000/friends";

    @SuppressLint("ResourceType")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friends);
        TableLayout friendsTable = findViewById(R.id.friendsTable);
        friendsTable.setVisibility(View.INVISIBLE);

        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, FRIENDS_URL, null, response -> {
            friendsTable.setVisibility(View.VISIBLE);

            // removes loading spinner
            findViewById(R.id.loadingPanel).setVisibility(View.GONE);


            Iterator<String> keys = response.keys();
            while(keys.hasNext()) {
                String key = keys.next();

                LinearLayout div = new LinearLayout(this);
                div.setBackgroundResource(R.drawable.layout_bg);
                div.setMinimumHeight(15);
                div.setMinimumWidth(650);

                TableRow t = new TableRow(this);
                t.addView(div);
                t.setGravity(Gravity.CENTER);
                friendsTable.addView(t);

                TableRow row = createTableRow(response, key);
                friendsTable.addView(row);


            }

        }, (Response.ErrorListener) error -> Toast.makeText(this, "ERROR", Toast.LENGTH_LONG).show());

        queue.add(jsonObjectRequest);
    }

    public TableRow createTableRow(JSONObject response, String key){

        TableRow row = new TableRow(this);
        TableRow.LayoutParams lp = new TableRow.LayoutParams(
                TableRow.LayoutParams.WRAP_CONTENT,
                TableRow.LayoutParams.MATCH_PARENT
        );
        lp.setMargins(20,40,20,40);
        row.setLayoutParams(lp);

        TextView name = new TextView(this);
        TextView room = new TextView(this);
        lp.setMargins(20,15,20,15);

        name.setTextSize(25);
        room.setTextSize(25);

        name.setLayoutParams(lp);
        room.setLayoutParams(lp);


        name.setText(key);
        try {
            room.setText(response.getString(key));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        room.setBackgroundResource(R.drawable.layout_bg);
        name.setCompoundDrawablesRelativeWithIntrinsicBounds(
                R.drawable.ic_baseline_star_24,0,0,0
        );
        row.addView(name);
        row.addView(room);

        row.setGravity(Gravity.CENTER);

        return row;
    }

    @Override
    public void onClick(View view) {
        onBackPressed();
    }
}
