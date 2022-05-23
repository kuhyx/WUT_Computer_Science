using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Formation : MonoBehaviour
{
    [SerializeField] Squad squad;

    void Awake()
    {
        this.squad = squad.GetComponent<Squad>();
    }

    public Dictionary<Entity, Vector2Int> calculatePositions(Vector2Int coordinates)
    {
        List<Entity> soldiers = this.squad.GetSoldiers();
        Dictionary<Entity, Vector2Int> soldierNewCoordinate = new Dictionary<Entity, Vector2Int>();
        int soldierNumber = 0;
        foreach (Entity Entity in soldiers)
        {
            soldierNewCoordinate.Add(Entity, calculateSoldierCoordinates(soldierNumber, coordinates));
        }
        return soldierNewCoordinate;
    }

    // https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/in-parameter-modifier
    private Vector2Int calculateSoldierCoordinates(in int soldierNumber, in Vector2Int coordinates)
    {
        // Horizontal line we change x
        Vector2Int soldierCoordinates = new Vector2Int(coordinates.x + soldierNumber,  coordinates.y);
        return soldierCoordinates;
    }


}
