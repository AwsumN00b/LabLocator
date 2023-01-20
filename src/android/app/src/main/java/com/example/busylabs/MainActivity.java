package com.example.busylabs;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.wifiscanner.ApData;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    WifiManager wifiManager;
    WifiInfo wifiInfo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        wifiInfo = wifiManager.getConnectionInfo();
    }

    @Override
    public void onClick(View view) {

    }

    public void startScan(View view) {
        ApData apData = new ApData("LG25");

        apData.updateSSID(wifiInfo.getSSID());
        apData.updateBSSID(wifiInfo.getBSSID());
        apData.updateRSSI(wifiInfo.getRssi());

        apData.buildVisibleApList(wifiManager);

        String apDataString = apData.toString();
        Log.d("Wifi Test", apDataString);
        updateTextView(apDataString);
    }

    public void updateTextView(String string) {
        TextView textView = (TextView) findViewById(R.id.textView);
        textView.setText(string);
    }
}