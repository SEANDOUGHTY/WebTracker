using UnityEngine;
using System.Collections;

public class UserMovement : MonoBehaviour {
		
	public float speed;
	public float xmin, xmax, zmin, zmax, y;
				
		void FixedUpdate () 
		{
			float moveHorizontal = Input.GetAxis ("Horizontal");
			float moveVertical = Input.GetAxis ("Vertical");
			
			Vector3 movement = new Vector3(moveHorizontal, 0.0f, moveVertical);
			rigidbody.velocity = movement * speed * Time.deltaTime;


			rigidbody.position = new Vector3
			(
				Mathf.Clamp (rigidbody.position.x, xmin, xmax),
				y,
				Mathf.Clamp (rigidbody.position.z, zmin, zmax)
			);
	}
}
