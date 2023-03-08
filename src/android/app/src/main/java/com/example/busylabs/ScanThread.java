package com.example.busylabs;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;

import com.example.wifiscanner.ScanData;

import java.io.File;
import java.io.FileOutputStream;

public class ScanThread extends Thread {

    static final int MAX_ITERATIONS = 100;
    static final String OUTPUT_FILE = "output_scan.csv";

    MainActivity mainActivity;
    WifiManager wifiManager;
    WifiInfo wifiInfo;

    private boolean keepRunning = false;

    public void toggleThread() {
        this.keepRunning = !this.keepRunning;
    }

    public boolean isRunning() {
        return this.keepRunning;
    }

    public ScanThread(MainActivity mainActivity) {
        this.mainActivity = mainActivity;
        this.wifiManager = (WifiManager) mainActivity.getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        this.wifiInfo = wifiManager.getConnectionInfo();
    }

    @Override
    public void run() {
        int i = 0;
        while (this.keepRunning) {

            if (++i > MAX_ITERATIONS) {
                this.keepRunning = false;
                break;
            }

            ScanData scanData = new ScanData(mainActivity.room);

            scanData.updateSSID(wifiInfo.getSSID());
            scanData.updateBSSID(wifiInfo.getBSSID());
            scanData.updateRSSI(wifiInfo.getRssi());

            scanData.buildApList(wifiManager);


            if (!scanData.apList.isEmpty()) {
                String apDataString = scanData.toString();
                writeToFile(apDataString);
                mainActivity.updateTextViewCurrentLocation(apDataString);
            }

            try {
                Thread.sleep(30000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void writeToFile(String data) {
        File path = mainActivity.getApplicationContext().getFilesDir();
        try {
            FileOutputStream writer = new FileOutputStream(new File(path, OUTPUT_FILE), true);
            writer.write(data.getBytes());
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
