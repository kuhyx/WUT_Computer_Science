using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Collections.Specialized;

// normal C# object
public class Pathfinding : MonoBehaviour
{
	readonly int EMPTY_TILE_COST = 1;
	readonly int UNREACHABLE = int.MaxValue;
	readonly int OCCUPIED_TILE_COST = int.MaxValue;

	OrderedDictionary resolvedNodes;
	OrderedDictionary nodesToExplore;
	// returns true if a valid path was found

	static public Pathfinding Instance;

	private void Awake()
	{
		Instance = this;
	}

	public bool FindPath(Vector2Int startCoords, Vector2Int endCoords, out List<Vector2Int> path, int maxPathPointDistanceFromStart = int.MaxValue)
	{
		path = new List<Vector2Int>();
		if (TilemapManager.ins.GetTileState(endCoords.x, endCoords.y) == TilemapManager.TileState.outOfBounds)
		{
			return false;
		}

		resolvedNodes = new OrderedDictionary();
		nodesToExplore = new OrderedDictionary();
		PathNode finalNode = null;
		// List<PathNode> finalNodes? // keep track of nodes that are at the edge of soldier's vision, so they can become a destination now
        nodesToExplore.Add(startCoords, new PathNode(null, startCoords, 0));
		
		while (nodesToExplore.Count > 0)
		{
			PathNode currentNode = (PathNode)nodesToExplore[0];
			if(currentNode.Coords == endCoords)
			{// found path
				finalNode = currentNode; // this node is the destination node, do not search for paths from it
				nodesToExplore.Remove(currentNode.Coords);
				resolvedNodes.Add(currentNode.Coords, currentNode);
				continue; // there might be a quicker path, so continue exploring nodes
			}

			foreach (Vector2Int targetCoord in GetNeighbors(currentNode.Coords))
			{
				int newCost = GetTargetCost(currentNode.Cost, targetCoord);
				if (nodesToExplore.Contains(targetCoord)) // do not add a tile to be explored twice
				{// check if found cheaper path
					PathNode neighbor = (PathNode)nodesToExplore[targetCoord];
					if (neighbor.Cost > newCost && newCost > 0)
					{
						nodesToExplore.Remove(targetCoord);
						nodesToExplore.Add(targetCoord, new PathNode(currentNode, targetCoord, newCost));
					}
					continue;
				}
				if (resolvedNodes.Contains(targetCoord))
				{// check if found cheaper path
					PathNode neighbor = (PathNode)resolvedNodes[targetCoord];
					if (neighbor.Cost > newCost && newCost > 0)
						nodesToExplore.Add(targetCoord, new PathNode(currentNode, targetCoord, newCost));
					continue;
				}// not evaluated previously: add to be explored
				nodesToExplore.Add(targetCoord, new PathNode(currentNode, targetCoord, newCost));
			}

			resolvedNodes.Add(currentNode.Coords, currentNode);
			nodesToExplore.Remove(currentNode.Coords);
		}
		// all nodes explored, find path
		if(finalNode == null)
		{// did not find final node, decide where to go for a temporary step

		}
		path = ConstructPath(finalNode);
		if (path.Count < 1)
			return false;
		return true;
	}

	private class PathNode
	{
		public PathNode Previous;
		public Vector2Int Coords;
		public int Cost;

		public PathNode(PathNode previous, Vector2Int corods, int cost)
		{
			Previous = previous;
			Coords = corods;
			Cost = cost;
		}
	}
	
	private int GetTargetCost(int cost, Vector2Int targetCoords)
	{
		TilemapManager.TileState targetState = TilemapManager.ins.GetTileState(targetCoords.x, targetCoords.y);
		if(targetState == TilemapManager.TileState.free)
		{
			return cost + EMPTY_TILE_COST;		
		}// tile occupied or out of bounds
		return OCCUPIED_TILE_COST;

	}

	// get movable neighbor coordinates
	private List<Vector2Int> GetNeighbors(Vector2Int coords)
	{
		List<Vector2Int> final = new List<Vector2Int>();
		List<Vector2Int> neighbors = new List<Vector2Int>();
		neighbors.Add(coords + Vector2Int.up);
		neighbors.Add(coords + Vector2Int.down);
		neighbors.Add(coords + Vector2Int.left);
		neighbors.Add(coords + Vector2Int.right);
		foreach(Vector2Int neighbor in neighbors)
		{
			if(TilemapManager.ins.GetTileState(neighbor.x, neighbor.y) != TilemapManager.TileState.outOfBounds)
			{
				final.Add(neighbor);
			}
		}
		return final;
	}

	private List<Vector2Int> ConstructPath(PathNode finalNode)
	{
		List<Vector2Int> path = new List<Vector2Int>();
		PathNode currentNode = finalNode;
		while(currentNode.Previous != null)
		{//TEMP just give next step
			path.Add(currentNode.Coords);
			currentNode = currentNode.Previous;
		}
		path.Reverse();
		//throw new System.NotImplementedException();
		return path;
	}
}
