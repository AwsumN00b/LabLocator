package com.example.wifiscanner;

import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;

import androidx.annotation.NonNull;

import java.util.ArrayList;
import java.util.List;

public class ScanData {

    public String timestamp;
    String location;
    String ssid;
    String bssid;
    int rssi;
    public List<AccessPoint> apList = new ArrayList<>();

    public ScanData(String location) {
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

    public void buildApList(WifiManager wifiManager) {

        boolean scanSuccess = wifiManager.startScan();

        if (scanSuccess) {
            List<ScanResult> availNetworks = wifiManager.getScanResults();

            if (availNetworks.size() > 0) {

                for (int i = 0; i < availNetworks.size(); i++) {
                    ScanResult currentScan = availNetworks.get(i);
                    if (currentScan.SSID.equals("eduroam") || currentScan.SSID.equals("DCU-Guest-WiFi")) {
                        AccessPoint accessPoint = new AccessPoint(currentScan.SSID, currentScan.BSSID, currentScan.level);
                        apList.add(accessPoint);
                    }
                }
            }
        }
    }

    private String toApListString(List<AccessPoint> apList) {
        StringBuilder stringBuilder = new StringBuilder();
        for (AccessPoint item : apList) {
            stringBuilder.append(item.toString());
            stringBuilder.append("|");
        }

        return stringBuilder.toString();
    }

    @NonNull
    public String toString() {

        return String.format("%s,", this.location) +
                String.format("%s,", this.timestamp) +
                String.format("%s,", this.ssid) +
                String.format("%s,", this.bssid) +
                String.format("%s,", this.rssi) +
                String.format("%s\n", toApListString(this.apList));
    }
}
