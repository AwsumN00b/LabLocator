package com.example.wifiscanner;

public class AccessPoint {

    public String ssid;
    public String bssid;
    public int signalStrength;

    public AccessPoint(String ssid, String bssid, int signalStrength) {
        this.ssid = ssid;
        this.bssid = bssid;
        this.signalStrength = signalStrength;
    }

    public String toString() {
        return String.format("%s;%s;%s", this.ssid, this.bssid, this.signalStrength);
    }

}
