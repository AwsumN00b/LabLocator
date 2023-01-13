package com.example.wifiscanner;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;

import java.util.HashMap;
import java.util.Map;

public class ApData {

    WifiInfo wifiInfo;
    WifiManager wifiManager = (WifiManager)getApplicationContext().getSystemService(Context.WIFI_SERVICE);

    String location;
    String ssid;
    String bssid;
    int rssi;
    Map<String, String> visibleApList = new HashMap<>();

    public ApData(String location) {
        this.location = location;
        updateSSID();
        updateBSSID();
        updateRSSI();
        buildVisableApList();
    }

    public void updateSSID() {
        this.ssid = wifiInfo.getSSID();
    }

    public void updateBSSID() {
        this.bssid = wifiInfo.getBSSID();
    }

    public void updateRSSI() {
        this.rssi = wifiInfo.getRssi();
    }

    public void buildVisableApList() {
// Get List of Available Wifi Networks
        List<ScanResult> availNetworks = wifiManager.getScanResults();

        if (availNetworks.size() > 0) {

            // Get Each network detail
            for (int i=0; i< availNetworks.size();i++) {
                // ...
            }
        }
    }
}
