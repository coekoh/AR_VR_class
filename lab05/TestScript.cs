using System;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using Vuforia;

public class TestScript : MonoBehaviour
{
    public Button button;
    private Text m_LogText;
    private int dbm_val;
    public GameObject camera;
    public GameObject sphere;
    public AndroidJavaObject activity;

    //This method Instantiates the sphere and aCamera object
    GameObject createObject()
    {
        GameObject sphereCopy = (GameObject)Instantiate(sphere, camera.transform.position, camera.transform.rotation);
        sphereCopy.SetActive(true);

        return sphereCopy;
    }

    // Start is called before the first frame update
    void Start()
    {
        camera = GameObject.Find("ARCamera");
        sphere = GameObject.Find("Sphere");
        sphere.SetActive(false);
        Button btn = button.GetComponent<Button>();
        btn.onClick.AddListener(delegate { TaskOnClick(btn); });
        m_LogText = GameObject.Find("LogText").GetComponent<Text>();
        activity = new AndroidJavaClass("com.unity3d.player.UnityPlayer").GetStatic<AndroidJavaObject>("currentActivity");

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // This method gets the wifi strength and assigns it to a variable
    void GetWifiStrength()
    {
        var wifiManager = activity.Call<AndroidJavaObject>("getSystemService", "wifi");
        
        try
        {
            AndroidJavaObject wifiInfo = wifiManager.Call<AndroidJavaObject>("getConnectionInfo");
            dbm_val = wifiInfo.Call<int>("getRssi");
        }
        catch (Exception e)
        {
            m_LogText.text += "Exception " + e + "\n";
        }

        m_LogText.text = "DBM =" + dbm_val + "\n";
        //m_LogText.text = "Done\n";
    }

    // This method executes the action of creating a sphere and then setting the color of the sphere based on the wifi strength
    void TaskOnClick(Button btn)
    {
        GameObject newObject = createObject();
        Renderer renderer = newObject.GetComponent<Renderer>();
        GetWifiStrength();

        if (dbm_val < -75)
        {
            renderer.material.SetColor("_Color", Color.red);
        }

        else if(dbm_val > -50)
        {
            renderer.material.SetColor("_Color", Color.green);
        }

        else
        {
            renderer.material.SetColor("_Color", Color.yellow);
        }
    }
}
