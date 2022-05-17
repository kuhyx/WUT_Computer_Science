using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;

public class TilemapManager : MonoBehaviour
{
    public enum TileState
    {
        free,
        taken,
        outOfBounds
    }

    public struct Tile
    {
        public Soldier standingSoldier;
    }

    [Header("Common Values")]

    [SerializeField] private Vector2Int mapSize = new Vector2Int(5,5);
    [SerializeField] private Vector3 WORLD_SPACE_OFFSET = new Vector3(0.5f, 1f, 0.5f);

    [Header("Soldiers values")]

    [SerializeField] private Vector2Int soldierStartingPosition = Vector2Int.zero;

    [Header("Enemies values")]

    [SerializeField] private Vector2Int enemyStartingPosition = Vector2Int.zero;

    [Header("References")]

    [SerializeField] private Tilemap tilemap = null;
    [SerializeField] private GameObject soldierPrefab = null;

    // private (do not edit) variables

    [Header("Debug (do not change)")]

    private Tile[,] tiles = null;

    // ---------- Unity messages

    private void Awake()
    {
        tiles = new Tile[mapSize.x, mapSize.y];
    }

    private void Start()
    {
        SpawnSoldier(soldierStartingPosition.x, soldierStartingPosition.y, true);
        SpawnSoldier(enemyStartingPosition.x, enemyStartingPosition.y, false);
    }

    private void OnValidate()
    {
        if (soldierStartingPosition.x < 0)
            soldierStartingPosition.x = 0;
        if (soldierStartingPosition.y < 0)
            soldierStartingPosition.y = 0;
        if (soldierStartingPosition.x >= mapSize.x)
            soldierStartingPosition.x = mapSize.x - 1;
        if (soldierStartingPosition.y >= mapSize.y)
            soldierStartingPosition.y = mapSize.y - 1;

        if (enemyStartingPosition.x < 0)
            enemyStartingPosition.x = 0;
        if (enemyStartingPosition.y < 0)
            enemyStartingPosition.y = 0;
        if (enemyStartingPosition.x >= mapSize.x)
            enemyStartingPosition.x = mapSize.x - 1;
        if (enemyStartingPosition.y >= mapSize.y)
            enemyStartingPosition.y = mapSize.y - 1;
    }

    // ---------- public functions

    public bool SpawnSoldier(int x, int y, bool isAlly)
    {
        if (GetTileState(x, y) != TileState.free)
            return false;

        tiles[x, y].standingSoldier = Instantiate(soldierPrefab, tilemap.CellToWorld(new Vector3Int(x, y, 0)) + WORLD_SPACE_OFFSET, Quaternion.identity).GetComponent<Soldier>();

        if (isAlly)
            tiles[x, y].standingSoldier.setOwnTag(Soldier.SoldierType.Ally);
        else
            tiles[x, y].standingSoldier.setOwnTag(Soldier.SoldierType.Enemy);

        if (tiles[x, y].standingSoldier != null)
            return true;

        return false;
    }

    public bool DespawnSoldier(int x, int y)
    {
        if (GetTileState(x, y) != TileState.taken)
            return false;

        Destroy(tiles[x, y].standingSoldier.gameObject);
        tiles[x, y].standingSoldier = null;
        Debug.Log("Despaned a soldier");

        return true;
    }

    public Soldier GetSoldier(int x, int y)
    {
        if (GetTileState(x, y) != TileState.taken)
            return null;

        return tiles[x,y].standingSoldier;
    }

    public Soldier[] GetAllSoldiers()
    {
        List<Soldier> list = new List<Soldier>();

        foreach (Tile obj in tiles)
        {
            if (obj.standingSoldier != null)
                list.Add(obj.standingSoldier);
        }

        return list.ToArray();
    }

    public bool MoveSoldier(int x1, int y1, int x2, int y2)
    {
        if (GetTileState(x1, y1) == TileState.taken && GetTileState(x2, y2) == TileState.free)
        {
            tiles[x2, y2].standingSoldier = tiles[x1, y1].standingSoldier;
            tiles[x1, y1].standingSoldier = null;

            tiles[x2, y2].standingSoldier.transform.position = tilemap.CellToWorld(new Vector3Int(x2, y2, 0));

            return true;
        }

        return false;
    }

    // ---------- private methods

    private TileState GetTileState(int x, int y)
    {
        if (x < 0 || y < 0 || x >= mapSize.x || y >= mapSize.y)
            return TileState.outOfBounds;

        if (tiles[x, y].standingSoldier == null)
            return TileState.free;

        return TileState.taken;
    }

    public TileState GetTileFromWorldCoords(Vector3 worldCoords, out Tile selectedTile, out int x, out int y)
	{
        Vector3Int tilemapCoords = tilemap.WorldToCell(worldCoords);
        TileState tileState = GetTileState(tilemapCoords.x, tilemapCoords.y);
        x = tilemapCoords.x;
        y = tilemapCoords.y;

        if (tileState == TileState.outOfBounds)
        {
            selectedTile = new Tile();
            return TileState.outOfBounds;
        }
        // valid tile selected
        selectedTile = tiles[tilemapCoords.x, tilemapCoords.y];
        return tileState;
        
	}
}
