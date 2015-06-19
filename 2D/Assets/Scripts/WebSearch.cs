using UnityEngine;
using System.Collections;
using System.Net;
using System;
using Newtonsoft.Json;



public class webFetch : MonoBehaviour
{

    public GameObject carOnScene;
    public car[] ourClassArray;
    Competition competition;


    //start will invoke the deserialize function to repeat itself
    //the frequency of the repetition can be controlled. 
    void Start()
    {
        InvokeRepeating("deserialize", 2, 20);
    }


    public void deserialize()
    {
        var client = new WebClient();

        //view the url as a json string
        string jsonFile = client.DownloadString("http://www.worldsolarchallenge.org/api/positions");

        //de-serialize the array of objects into a list of carAttrs
        car[] carArray = JsonConvert.DeserializeObject<car[]>(jsonFile);

        //make an array of cars that only contains our class_id (which is 3)
        int m = 0;
        for (int i = 0; i < carArray.Length; i++)
        {
            if (carArray[i].class_id == 3)
            {
                ourClassArray[m] = carArray[i];
                Debug.Log(ourClassArray[m].car_name);
                m++;
            }

        }

        competition = new Competition(ourClassArray);

        for (int i = 0; i < ourClassArray.Length; i++)
        {
            Vector2 location = new Vector2(
                0.452848667f * ourClassArray[i].lng - 60.65497f,
                0.504190f * ourClassArray[i].lat + 11.7852f
            );

            Instantiate(carOnScene, location, Quaternion.identity);
        }
    }

}

//to display the 3 ppl behind and infront of us
public class Competition : MonoBehaviour {

	public car[] rivals;
	public int[] distToRival; //in KM, according to wsc file on website

	public Competition(ref car[] allCars){
		//first, find the index out of all the competitors where U of T occurs
		int UofT_Index;
		for(int i = 0 ; i < allCars.Length ; i++){
			if (allCars[i].name == "Blue Sky Solar Racing"){
				UofT_Index = i;
			}
		}

		//next, go 3 below and store the rivals in a new array until you get to 3 above u of t
		//in the distToRival array, subtract the dist to adelaide members of both
		int s = 0;
		for(int j = UofT_Index - 3 ; j < UofT_Index - 3 || j >= 0 ; j++, s++){
			if (allCars[j].name != UofT){
				rivals[s] = allCars[j];
				distToRival[s] = allCars[UofT_Index].dist_adelaide - allCars[j].dist_adelaide;
			}
		}
	}
}


public class car : MonoBehaviour {
	
	public string id { get; set; }
	public string name { get; set; }
	public int number { get; set; }
	public string car_name { get; set; }
	public string country { get; set; }
	public int class_id { get; set; }
	public double lat { get; set; }
	public double lng { get; set; }
	public string gps_when { get; set; }
	public double dist_darwin { get; set; }
	public double dist_adelaide { get; set; }
	public string gps_age { get; set; }
	
}


