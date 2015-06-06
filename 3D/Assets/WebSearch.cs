using UnityEngine;
using System.Collections;
using System.Net;
using System;


public class WebSearch : MonoBehaviour {
	public string htmlCode;
	// Use this for initialization
	void Start () 
	{
		using (WebClient client = new WebClient ())
		{
			htmlCode = client.DownloadString("http://answers.unity3d.com/questions/472729/update-scene-every-5-minutes.html");
			Console.WriteLine("hi");
		}
	}
	
	// Update is called once per frame
	void Update () {
	}
}
