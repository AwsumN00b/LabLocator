package com.example.busylabs;

import android.content.Context;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.util.Log;
import android.widget.Toast;

import com.example.wifiscanner.ApData;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class ScanThread extends Thread {

    static int MAX_ITERATIONS = 2400;

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

            ApData apData = new ApData("LG25");

            apData.updateSSID(wifiInfo.getSSID());
            apData.updateBSSID(wifiInfo.getBSSID());
            apData.updateRSSI(wifiInfo.getRssi());

            apData.buildVisibleApList(wifiManager);

            String apDataString = apData.toString();

            try {
                Thread.sleep(30000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            writeToFile("output_scan.txt", apDataString);
            mainActivity.updateTextView(apDataString);
        }
    }

    private void writeToFile(String fileName, String data) {
        File path = mainActivity.getApplicationContext().getFilesDir();
        try {
            FileOutputStream writer = new FileOutputStream(new File(path, fileName), true);
            writer.write(data.getBytes());
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
