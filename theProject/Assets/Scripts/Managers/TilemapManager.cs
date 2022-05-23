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

    [SerializeField] private Vector2Int allyBaseCoord = Vector2Int.zero;
    [SerializeField] private Vector2Int[] soldierStartingPositions = null;

    [Header("Enemies values")]

    [SerializeField] private Vector2Int enemyBaseCoord = Vector2Int.zero;
    [SerializeField] private Vector2Int[] enemyStartingPositions = null;

    [Header("References")]

    [SerializeField] private Tilemap tilemap = null;
    [SerializeField] private GameObject soldierPrefab = null;
    [SerializeField] private GameObject basePrefab = null;

    // private (do not edit) variables

    private static TilemapManager ins;

    private Tile[,] tiles = null;

    // ---------- Unity messages

    private void Awake()
    {
        ins = this;

        tiles = new Tile[mapSize.x, mapSize.y];
    }

    private void Start()
    {
        //spawn bases
        SpawnSoldier(allyBaseCoord.x, allyBaseCoord.y, true, true);
        SpawnSoldier(enemyBaseCoord.x, enemyBaseCoord.y, false, true);

        //spawn soldiers
        foreach (Vector2Int vec in soldierStartingPositions)
            SpawnSoldier(vec.x, vec.y, true);
        foreach (Vector2Int vec in enemyStartingPositions)
            SpawnSoldier(vec.x, vec.y, false);
    }

    private void OnValidate()
    {
        for (int i=0; i< soldierStartingPositions.Length; i++)
        {
            if (soldierStartingPositions[i].x < 0)
                soldierStartingPositions[i].x = 0;
            if (soldierStartingPositions[i].y < 0)
                soldierStartingPositions[i].y = 0;
            if (soldierStartingPositions[i].x >= mapSize.x)
                soldierStartingPositions[i].x = mapSize.x - 1;
            if (soldierStartingPositions[i].y >= mapSize.y)
                soldierStartingPositions[i].y = mapSize.y - 1;
        }

        for (int i = 0; i < enemyStartingPositions.Length; i++)
        {
            if (enemyStartingPositions[i].x < 0)
                enemyStartingPositions[i].x = 0;
            if (enemyStartingPositions[i].y < 0)
                enemyStartingPositions[i].y = 0;
            if (enemyStartingPositions[i].x >= mapSize.x)
                enemyStartingPositions[i].x = mapSize.x - 1;
            if (enemyStartingPositions[i].y >= mapSize.y)
                enemyStartingPositions[i].y = mapSize.y - 1;
        }
    }

    // ---------- public functions

    public bool SpawnSoldier(int x, int y, bool isAlly, bool isBase=false)
    {
        if (GetTileState(x, y) != TileState.free)
            return false;

        if (isBase)
            tiles[x, y].standingSoldier = Instantiate(basePrefab, tilemap.CellToWorld(new Vector3Int(x, y, 0)) + WORLD_SPACE_OFFSET, Quaternion.identity).GetComponent<Soldier>();
        else
            tiles[x, y].standingSoldier = Instantiate(soldierPrefab, tilemap.CellToWorld(new Vector3Int(x, y, 0)) + WORLD_SPACE_OFFSET, Quaternion.identity).GetComponent<Soldier>();

        if (isAlly)
            tiles[x, y].standingSoldier.setOwnTag(Soldier.SoldierType.Ally);
        else
            tiles[x, y].standingSoldier.setOwnTag(Soldier.SoldierType.Enemy);

        if (tiles[x, y].standingSoldier != null)
            return true;

        tiles[x, y].standingSoldier.SetTileCoords(new Vector2Int(x, y));

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
            // change proper values
            tiles[x2, y2].standingSoldier = tiles[x1, y1].standingSoldier;
            tiles[x1, y1].standingSoldier = null;
            tiles[x2, y2].standingSoldier.SetTileCoords(new Vector2Int(x2, y2));

            // change Soldier world position
            tiles[x2, y2].standingSoldier.transform.position = tilemap.CellToWorld(new Vector3Int(x2, y2, 0));

            return true;
        }

        return false;
    }

    // ---------- public statics methods

    public static bool MoveSoldierS(int x1, int y1, int x2, int y2)
    {
        return ins.MoveSoldier(x1, y1, x2, y2);
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
