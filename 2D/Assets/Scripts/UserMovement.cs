using UnityEngine;
using System.Collections;

public class UserMovement : MonoBehaviour {

	public float speed;
	public float xmin = -1.5f;
	public float xmax = 1.5f;
	public float ymin = -2.8f;
	public float ymax = 2.8f;


	public float dragSpeed = 0.5f;
	private Vector3 dragOrigin;

	// Update is called once per frame
	void FixedUpdate () 
	{
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");



		Vector3 movement = new Vector3 (moveHorizontal, moveVertical, 0.0f);
		rigidbody.velocity = movement * speed * Time.deltaTime;
	

		rigidbody.position = new Vector3
		(
			Mathf.Clamp (rigidbody.position.x, xmin, xmax),
			Mathf.Clamp (rigidbody.position.y, ymin, ymax),
			-10f
		);
	}

	void Update()
	{
		if (Input.GetMouseButtonDown (0)) {
			dragOrigin = Input.mousePosition;
			return;
		}

		if (!Input.GetMouseButton (0)) {
			return;
		}

		Vector3 pos = Camera.main.ScreenToViewportPoint (Input.mousePosition - dragOrigin);
		Vector3 move = new Vector3 (pos.x * dragSpeed, pos.y * dragSpeed, 0);

		transform.Translate (move, Space.World);
	}
}