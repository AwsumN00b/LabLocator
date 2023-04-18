package com.example.busylabs;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class FriendsActivity extends AppCompatActivity implements View.OnClickListener {

    TextView friendsTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_friends);
//        String text = "Friends List";
//        friendsTextView = findViewById(R.id.textView_friends_list);
//        friendsTextView.setText(text);
    }

    @Override
    public void onClick(View view) {
        onBackPressed();
    }
}
