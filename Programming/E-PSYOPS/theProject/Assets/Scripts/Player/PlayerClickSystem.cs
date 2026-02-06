using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerClickSystem : MonoBehaviour
{
    [SerializeField] TilemapManager tilemapManager;

    private BetterInput bInput;
    private bool leftMouseClicked = false;
    private Vector2 mousePos = Vector2.zero;

    [SerializeField] Squad playerSquad;
    public void SetPlayerSquad(Squad newSquad) { playerSquad = newSquad; } // called by Squad Manager //DEPENDENCY_INJECTION

	private void Awake()
	{
        bInput = new BetterInput();

        bInput.Main.MouseLeftClick.started += (ctx) => { leftMouseClicked = true; };
        bInput.Main.MouseLeftClick.canceled += (ctx) => { leftMouseClicked = false; };

        bInput.Main.MousePosition.performed += (ctx) => { mousePos = ctx.ReadValue<Vector2>(); };

        tilemapManager = FindObjectOfType<TilemapManager>();
        if(tilemapManager == null)
		{
            Debug.LogError("Tilemap Manager not found");
		}
	}
	// Update is called once per frame
	void Update()
    {
        if(leftMouseClicked) // Change to new input system
		{
            leftMouseClicked = false;
            //Debug.Log("CLICK");
            Camera camera = Camera.main;
            RaycastHit hit;
            Ray ray = camera.ScreenPointToRay(mousePos);
            RaycastHit2D hit2D = Physics2D.GetRayIntersection(ray);

            Vector3 tileCoord = new Vector3(-1, -1, -1);
            bool hitted = false;

            if (Physics.Raycast(ray, out hit))
            {
                tileCoord = hit.point;
                hitted = true;
            }
            else if (hit2D.collider != null)
            {
                tileCoord = hit2D.point;
                hitted = true;
            }

            if (hitted)
            {
                Vector3 hitWorldPosition = tileCoord;

                Debug.Log($"Hit at {hitWorldPosition}");
                TilemapManager.Tile selectedTile;
                int x, y;
                TilemapManager.TileState tileState = tilemapManager.GetTileFromWorldCoords(hitWorldPosition, out selectedTile, out x, out y);
                
                if(tileState == TilemapManager.TileState.outOfBounds)
				{
                    Debug.Log($"No tile was hit (hit \"coords\" {x},{y})");
                    return; // for now do nothing if a tile was not selected
				}
                // a tile was hit
                Debug.Log($"Tile {x},{y} was selected - DO MOVEMENT ORDER");
                playerSquad.EnqueueOrder(new Squad.MovementOrder(new Vector2Int(x,y)));


            }
        }            
    }

    private void OnEnable()
    {
        bInput.Main.Enable();
    }

    private void OnDisable()
    {
        bInput.Main.Disable();
    }
}
