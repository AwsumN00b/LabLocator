package com.example.busylabs;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;

import com.example.wifiscanner.AccessPoint;
import com.example.wifiscanner.ScanData;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.util.ArrayList;
import java.util.List;


public class WifiScanUnitTest {

    @Mock
    private WifiManager wifiManager;

    @Before
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void buildApList_success() {
        ScanData scanData = new ScanData();
        List<ScanResult> scanResults = new ArrayList<>();
        ScanResult result1 = mock(ScanResult.class);
        ScanResult result2 = mock(ScanResult.class);
        scanResults.add(result1);
        scanResults.add(result2);

        when(wifiManager.startScan()).thenReturn(true);
        when(wifiManager.getScanResults()).thenReturn(scanResults);
        result1.SSID = "eduroam";
        result1.BSSID = "12:34:56:78:90:AB";
        result1.level = -70;
        result2.SSID = "DCU-Guest-WiFi";
        result2.BSSID = "AB:CD:EF:12:34:56";
        result2.level = -80;

        scanData.buildApList(wifiManager);

        verify(wifiManager).startScan();
        verify(wifiManager).getScanResults();

        assert scanData.apList.size() == 2;
    }

    @Test
    public void buildApList_scanFailed() {
        ScanData scanData = new ScanData();
        when(wifiManager.startScan()).thenReturn(false);

        scanData.buildApList(wifiManager);

        verify(wifiManager).startScan();
        verify(wifiManager, Mockito.never()).getScanResults();
        assert (scanData.apList).isEmpty();
    }

    @Test
    public void buildApList_noMatches() {
        ScanData scanData = new ScanData();
        List<ScanResult> scanResults = new ArrayList<>();
        ScanResult scanResult1 = mock(ScanResult.class);
        ScanResult scanResult2 = mock(ScanResult.class);
        scanResults.add(scanResult1);
        scanResults.add(scanResult2);

        when(wifiManager.startScan()).thenReturn(true);
        when(wifiManager.getScanResults()).thenReturn(scanResults);
        scanResult1.SSID = "Invalid SSID 1";
        scanResult2.SSID = "Invalid SSID 2";

        scanData.buildApList(wifiManager);

        verify(wifiManager).startScan();
        verify(wifiManager).getScanResults();
        assert (scanData.apList).isEmpty();
    }

    @Test
    public void testToApListString() {
        ScanData scanData = new ScanData();
        scanData.apList.add(new AccessPoint("eduroam", "00:11:22:33:44:55", -50));
        scanData.apList.add(new AccessPoint("DCU-Guest-WiFi", "11:22:33:44:55:66", -60));

        List<String> expected = new ArrayList<>();
        expected.add("eduroam;00:11:22:33:44:55;-50");
        expected.add("DCU-Guest-WiFi;11:22:33:44:55:66;-60");

        assertEquals(expected, scanData.toApListString());
    }

    @Test
    public void testToString() {
        ScanData scanData = new ScanData();
        scanData.location = "DCU";
        scanData.updateSSID("eduroam");
        scanData.updateBSSID("00:11:22:33:44:55");
        scanData.updateRSSI(-50);
        scanData.apList.add(new AccessPoint("eduroam", "00:11:22:33:44:55", -50));
        scanData.apList.add(new AccessPoint("DCU-Guest-WiFi", "11:22:33:44:55:66", -60));

        String expected = "DCU,";
        expected += scanData.timestamp + ",";
        expected += "eduroam,";
        expected += "00:11:22:33:44:55,";
        expected += "-50,";
        expected += "[eduroam;00:11:22:33:44:55;-50, DCU-Guest-WiFi;11:22:33:44:55:66;-60]\n";

        assertEquals(expected, scanData.toString());
    }
}