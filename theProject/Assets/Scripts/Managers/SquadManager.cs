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
		playerSquad = Instantiate(squadPrefab).GetComponent<Squad>();
		playerSquad.gameObject.name = "Player Squad";
		playerSquad.transform.SetParent(transform);
		playerSquad.SetOwnTeam(Entity.Team.Ally);

		enemySquad = Instantiate(squadPrefab).GetComponent<Squad>();
		enemySquad.gameObject.name = "Enemy Squad";
		enemySquad.transform.SetParent(transform);
		enemySquad.SetOwnTeam(Entity.Team.Enemy);
	}
	// Update is called once per frame
	void Update()
    {
		Debug.Log("Added initial soldiers to squad");
		// add all ally soldiers to squad
		var soldiers = FindObjectsOfType<Soldier>();
		var squads = new List<Squad>();
		squads.Add(playerSquad);
		squads.Add(enemySquad);

		foreach (var soldier in soldiers)
		{
			foreach (var squad in squads)
			{
				if (soldier.GetOwnTeam() == squad.GetOwnTeam())
				{
					squad.AddSoldierToSquad(soldier);
					soldier.OnDeath.AddListener(squad.RemoveSoldierFromSquad);
				}
			}
			enabled = false;
		}
    }
}
