using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;
using UnityEngine.UI;
using TMPro;

public class OrbitMotion : MonoBehaviour
{
    public Transform orbitingObject; 
    public Transform orbitSun;
    public Transform planet;
    public Transform axis;

    // Create Orbit ellipse
    float orbitMajorAxis = 7;
    float orbitMinorAxis;
    float orbitFocus;
    public float eccentricity = 0.01f;

    public float omega = 290f;
    public float axisAngle = 0f;

    // Visualization parameters
    public float insolation = 1.0f;
    public float obliquity;
    public int year;
    
    public OrbitParameters orb;

    public Ellipse orbitPath;

    float orbitProgress = 0f;
    public float orbitPeriod = 10f;
    bool orbitActive = true;

    // Handle text labels
    public float textDistance = 4f;
    // public Transform seasonLabels;
    public Transform summer;
    public Transform winter;
    public Transform fall;
    public Transform spring;

    // UDP Communication
    Thread receiveThread;
    UdpClient client;
    int port;

    // UI Stuff
    public Slider solarSlider;
    public TextMeshProUGUI yearTMP; 
    public TextMeshProUGUI eccTMP;
    public TextMeshProUGUI omegaTMP;
    public TextMeshProUGUI obliqTMP;

    public Image banner;
    public Sprite bannerStart;
    public Sprite bannerSuccess;
    public Sprite bannerSuccessGlow;
    public Sprite bannerFail;
    public Sprite bannerFailGlow;

    public int gameState = 0;
    
    // Start is called before the first frame update
    void Start()
    {
        if (orbitingObject == null) {
            orbitActive = false;
            return;
        }
        GetMinorAxis();

        SetOrbitingObjectPosition();
        // SetOrbitSunPosition();
        StartCoroutine (AnimateOrbit());

        port = 5065;
        InitUDP();
    }

    private void InitUDP()
    {
        print("UDP Initializing");

        receiveThread = new Thread (new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    private void ReceiveData()
    {
        client = new UdpClient (port);

        print("UDP Thread started");

        while (true)
        {
            try 
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port);
                byte[] data = client.Receive(ref anyIP);

                string text = Encoding.UTF8.GetString(data);
                print("Received: " + text);

                // Parse received JSON
                orb = OrbitParameters.ParseJSON(text); 

                // Update parameters
                eccentricity = orb.eccen;
                omega = orb.omega;

                insolation = orb.insol;
                obliquity = orb.obliq;
                year = orb.year;

                gameState = orb.state;
            }
            catch(Exception e)
            {
                print(e.ToString());
            }
        }
    }

    void GetMinorAxis() {
        float fake_ecc = (eccentricity > 0.017f) ? 0.4f : 0.014f;
        print(">> Fake: " + fake_ecc.ToString());
        this.orbitFocus = fake_ecc * orbitMajorAxis;
        float b2 = (this.orbitMajorAxis * this.orbitMajorAxis) - (this.orbitFocus * this.orbitFocus);
        this.orbitMinorAxis = Mathf.Sqrt (b2);
    }

    void SetOrbitSunPosition() {
        orbitSun.localPosition = new Vector3(-1f * orbitFocus, 0, 0);
    }

    void SetOrbitingObjectPosition() {
        Vector2 orbitPos = orbitPath.Evaluate(orbitProgress, orbitMajorAxis, orbitMinorAxis);
        orbitingObject.localPosition = new Vector3(orbitPos.x + orbitFocus, 0, orbitPos.y);
    }

    void SetPlanetRotation() {
        planet.localRotation = Quaternion.Euler(0,180f*Time.time,0);
    }

    void SetAxisPrecession() {
        // axisAngle = ((precession / 8f) * 360f);
        axisAngle = omega + 70f;
        if (axisAngle > 360f) axisAngle = axisAngle - 360f;

        float axisXrotation = 23.5f * Mathf.Sin (axisAngle * Mathf.Deg2Rad);
        float axisZrotation = -23.5f * Mathf.Cos (axisAngle * Mathf.Deg2Rad);

        axis.localRotation = Quaternion.Euler(axisXrotation, 0, axisZrotation);
    }

    public void UpdatePrecession() {
        // Update text label positions
        summer.localPosition = new Vector3(textDistance * Mathf.Cos ((axisAngle + 180f) * Mathf.Deg2Rad), 0, textDistance * Mathf.Sin ((axisAngle + 180f) * Mathf.Deg2Rad));
        winter.localPosition = new Vector3(textDistance * Mathf.Cos (axisAngle * Mathf.Deg2Rad), 0, textDistance * Mathf.Sin (axisAngle * Mathf.Deg2Rad));
        fall.localPosition = new Vector3(textDistance * Mathf.Cos ((axisAngle + 90f) * Mathf.Deg2Rad), 0, textDistance * Mathf.Sin ((axisAngle + 90f) * Mathf.Deg2Rad));
        spring.localPosition = new Vector3(textDistance * Mathf.Cos ((axisAngle + 270f) * Mathf.Deg2Rad), 0, textDistance * Mathf.Sin ((axisAngle + 270f) * Mathf.Deg2Rad));  

        // seasonLabels.localRotation = Quaternion.Euler(0, axisAngle, 0); 
    }

    public void UpdateUI() {
        solarSlider.value = insolation;

        yearTMP.text = (year * 1000 - 2000).ToString() + " BC";
        eccTMP.text = eccentricity.ToString();
        omegaTMP.text = omega.ToString();
        obliqTMP.text = obliquity.ToString();

        // Based on game state, change banner
        if (gameState == 0) {
            banner.sprite = bannerStart;
        }
        else if (gameState == 1) {
            banner.sprite = bannerSuccessGlow;
        }
        else if (gameState == 2) {
            banner.sprite = bannerFail; 
        }
        else if (gameState == 3) {
            banner.sprite = bannerFailGlow;
        }
    }

    IEnumerator AnimateOrbit() {
        if (orbitPeriod < 0.1f) 
            orbitPeriod = 0.1f;
        float orbitSpeed = 1f / orbitPeriod;
        while (orbitActive) {
            orbitProgress += Time.deltaTime * orbitSpeed;
            orbitProgress %= 1f;

            GetMinorAxis();
            // SetOrbitSunPosition();
            SetOrbitingObjectPosition();
            SetPlanetRotation();
            SetAxisPrecession();

            UpdatePrecession();

            UpdateUI();

            yield return null;
        }

    }

}
