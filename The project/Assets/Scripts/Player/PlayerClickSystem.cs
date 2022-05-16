using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerClickSystem : MonoBehaviour
{
    TilemapManager tilemapManager;
	private void Awake()
	{
        tilemapManager = FindObjectOfType<TilemapManager>();
        if(tilemapManager == null)
		{
            Debug.LogError("Tilemap Manager not found");
		}
	}
	// Update is called once per frame
	void Update()
    {
        if(Input.GetMouseButton(0))
		{
            Camera camera = Camera.main;
            RaycastHit hit;
            Ray ray = camera.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit))
            {
                Transform objectHit = hit.transform;

                TilemapManager.Tile selectedTile;
                int x, y;
                TilemapManager.TileState tileState = tilemapManager.GetTileFromWorldCoords(objectHit.position, out selectedTile, out x, out y);
                
                if(tileState == TilemapManager.TileState.outOfBounds)
				{
                    Debug.Log($"No tile was hit (hit \"coords\" {x},{y})");
                    return; // for now do nothing if a tile was not selected
				}
                // a tile was hit
                Debug.Log($"Tile {x},{y} was selected - DO MOVEMENT ORDER");
                
            }
        }            
    }
}
