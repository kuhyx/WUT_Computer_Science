using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[RequireComponent]
public class SoldierSpawning : MonoBehaviour
{
	[SerializeField] int spawnInterval = 20; // ticks between spawning soldiers
	[SerializeField] int lastSpawnTick = 0;
	[SerializeField] Squad squad;
	[SerializeField] TilemapManager tilemapManager;
	[SerializeField] Vector2Int spawnCoords = Vector2Int.one * -1;
	public Vector2Int GetSpawnCoords() { return spawnCoords; }
	public void SetSpawnCoords(Vector2Int newSpawnCoords) { spawnCoords = newSpawnCoords; }

	private void Awake()
	{
		squad = GetComponent<Squad>();
		TickSystem.OnTick += HandleTick;
		tilemapManager = FindObjectOfType<TilemapManager>();//DEPENDENCY_INJECTION
	}

	private void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
		if (lastSpawnTick + spawnInterval > tickEventArgs.tickNumber)
			return;

		Soldier spawnedSoldier = tilemapManager.SpawnSoldier(spawnCoords.x, spawnCoords.y, squad.GetOwnTeam() == Entity.Team.Ally) as Soldier;
		if (spawnedSoldier == null)
			return;
		// managed to spawn the soldier
		lastSpawnTick = tickEventArgs.tickNumber;
		squad.AddSoldierToSquad(spawnedSoldier);
	}
}
