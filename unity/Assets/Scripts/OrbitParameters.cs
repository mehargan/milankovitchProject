using UnityEngine;
using System;

[System.Serializable]
public class OrbitParameters
{
    public int state;
    public int year;
    public float omega; 
    public float eccen;
    public float obliq;
    public float insol;

    public static OrbitParameters ParseJSON(string json)
    {
        return JsonUtility.FromJson<OrbitParameters>(json);
    }
}