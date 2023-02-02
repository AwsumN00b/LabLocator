package com.example.wifiscanner;

import android.net.wifi.ScanResult;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;

import androidx.annotation.NonNull;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ApData {

    String timestamp;
    String location;
    String ssid;
    String bssid;
    int rssi;
    Map<String, String> visibleApList = new HashMap<>();

    public ApData(String location) {
        long ts = System.currentTimeMillis() / 1000;
        this.timestamp = Long.toString(ts);
        this.location = location;
    }

    public void updateSSID(String ssid) {
        this.ssid = ssid;
    }

    public void updateBSSID(String bssid) {
        this.bssid = bssid;
    }

    public void updateRSSI(int rssi) {
        this.rssi = rssi;
    }

    public void buildVisibleApList(WifiManager wifiManager) {

        List<ScanResult> availNetworks = wifiManager.getScanResults();

        if (availNetworks.size() > 0) {

            for (int i = 0; i < availNetworks.size(); i++) {
                visibleApList.put(
                        availNetworks.get(i).BSSID, availNetworks.get(i).SSID
                );
            }
        }
    }

    @NonNull
    public String toString() {

        return String.format("Location: %s|", this.location) +
                String.format("Time: %s|", this.timestamp) +
                String.format("SSID: %s|", this.ssid) +
                String.format("BSSID: %s|", this.bssid) +
                String.format("RSSI: %s|", this.rssi) +
                String.format("AP List: %s\n", this.visibleApList.toString());
    }
}
