// TEMP CODE JUST FOR SHOWCASE PURPOSES
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SquadManager : MonoBehaviour
{
	[SerializeField] GameObject squadPrefab;
	Squad playerSquad;
	Squad enemySquad;
	private void Awake()
	{
		enemySquad = Instantiate(squadPrefab).GetComponent<Squad>();
		enemySquad.gameObject.name = "Enemy Squad";
		enemySquad.transform.SetParent(transform);

		playerSquad = Instantiate(squadPrefab).GetComponent<Squad>();
		playerSquad.gameObject.name = "Player Squad";
		playerSquad.transform.SetParent(transform);

	}
	// Update is called once per frame
	void Update()
    {
		Debug.Log("Added initial soldiers to squad");
		// add all ally soldiers to squad
		var soldiers = FindObjectsOfType<Soldier>();
		foreach(var soldier in soldiers)
		{
			if(soldier.GetOwnTeam() == Soldier.Team.Ally)
			{
				playerSquad.TempAddSoldierToSquad(soldier);
			}
		}

        enabled = false;
    }
}
