package com.example.wifiscanner;

import android.net.wifi.ScanResult;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;

import androidx.annotation.NonNull;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ApData {

    WifiInfo wifiInfo;

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
    }

    public void updateSSID() {
        try {
            this.ssid = wifiInfo.getSSID();
        } catch (NullPointerException e) {
            this.ssid = "ERROR";
        }
    }

    public void updateBSSID() {
        try {
            this.bssid = wifiInfo.getBSSID();
        } catch (NullPointerException e) {
            this.bssid = "ERROR";
        }
    }

    public void updateRSSI() {
        try {
            this.rssi = wifiInfo.getRssi();
        } catch (NullPointerException e) {
            this.rssi = 9999;
        }
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

        return String.format("Location: %s\n", this.location) +
                String.format("SSID: %s\n", this.ssid) +
                String.format("BSSID: %s\n", this.bssid) +
                String.format("RSSI: %s\n", this.rssi) +
                String.format("AP List: %s", this.visibleApList.toString());
    }
}
