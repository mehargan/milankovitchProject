using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RotationMotion : MonoBehaviour
{
    public Transform rotatingObject;

    public float rotatingSpeed = 180;
    
    // // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        rotatingObject.eulerAngles += new Vector3(0, rotatingSpeed, 0) * Time.deltaTime;
    }
}
