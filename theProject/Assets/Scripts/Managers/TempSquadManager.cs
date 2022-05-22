// TEMP CODE JUST FOR SHOWCASE PURPOSES
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TempSquadManager : MonoBehaviour
{
	Squad playerSquad;
	private void Awake()
	{
		playerSquad = FindObjectOfType<Squad>();
	}
	// Update is called once per frame
	void Update()
    {
		Debug.Log("Added initial soldeirs to squad");
		// add all ally soldiers to squad
		var soldiers = FindObjectsOfType<Soldier>();
		foreach(var soldier in soldiers)
		{
			if(soldier.TempGetOwnType() == Soldier.SoldierType.Ally)
			{
				playerSquad.TempAddSoldierToSquad(soldier);
			}
		}

        enabled = false;
    }
}
