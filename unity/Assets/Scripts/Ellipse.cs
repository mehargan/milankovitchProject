using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class Ellipse
{
    public Vector2 Evaluate(float t, float xAxis, float yAxis) {
        float angle = Mathf.Deg2Rad * 360f * t;
        float x = Mathf.Sin (angle) * xAxis;
        float y = Mathf.Cos (angle) * yAxis;

        return new Vector2(x, y);
    }
}
