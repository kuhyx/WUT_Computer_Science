using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Formation : MonoBehaviour
{
    [SerializeField] Squad squad;

    void Awake()
    {
        this.squad = squad.GetComponent(typeof(Squad));
    }

    public Dictionary<Soldier, Vector2Int> calculatePositions(Vector2int coordinates)
    {
        List<Soldier> soldiers = this.squad.getSoldiers();
        Dictionary<Soldier, Vector2Int> soldierNewCoordinate = new Dictionary<Soldier, Vector2Int>();
        int soldierNumber = 0;
        foreach (Soldier soldier in soldiers)
        {
            soldierNewCoordinate.Add(soldier, calculateSoldierCoordinates(soldierNumber, coordinates));
            MoveSoldierS(x, y, soldierNewCoordinate.Item1, soldierNewCoordinate.Item2);
        }
        return soldierNewCoordinate;
    }

    // https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/in-parameter-modifier
    private Vector2Int calculateSoldierCoordinates(in int soldierNumber, in Vector2Int coordinates)
    {
        // Horizontal line we change x
        Vector2Int coordinates = new Vector2Int(coordinates.Item1 + soldierNumber,  coordinates.Item1);
        return coordinates;
    }


}
