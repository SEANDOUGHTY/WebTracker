using UnityEngine;
using System.Collections;

public class UofT : MonoBehaviour {

	public float longnitude, latitude;

	// Update is called once per frame
	void Update () 
	{


		Vector3 location = new Vector3(
		0.452848667f * longnitude - 60.65497f, 
		0.0f, 
		0.504190f * latitude + 11.7852f
		);

		rigidbody.position = location;
	}
}
