package com.example.wifiscanner;

import java.util.HashMap;
import java.util.Map;

public class WifiInfo {

    WifiInfo wifiInfo = new WifiInfo();

    String location;
    String ssid;
    String mac;
    Map<String, String> visibleAPs = new HashMap<>();

}
