using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Communication : MonoBehaviour
{
    public struct CommunicationResult
    {
        public bool resetTTL;
        public List<Soldier> enemiesSpotted;
    }

    private float viewRange = 5f;
    private Soldier mySoldier = null;
    private Entity.Team myTeam = Entity.Team.Ally;

    // ---------- public methods

    private void Awake()
    {
        mySoldier = GetComponent<Soldier>();
    }

    public void Initialize(float _viewRange, Entity.Team _myTeam)
    {
        viewRange = _viewRange;
        myTeam = _myTeam;
    }

    public CommunicationResult HandleCommuncation()
    {
        CommunicationResult result = new CommunicationResult();
        result.resetTTL = false;
        result.enemiesSpotted = new List<Soldier>();

        // look for soldiers in vincinity
        Soldier[] soldiersFound = GetSoldiersInVincinity();

        // send Keep Alive (myTeam) - reset TTL (myTTL)
        foreach (Soldier sold in soldiersFound)
        {
            if (sold.GetOwnTeam() == myTeam)
            {
                result.resetTTL = true;
                break;
            }
        }

        // look fo enemies (enemyTeam) - add Enemies to enemiesSpotted (send List<Enemies>)
        if (result.resetTTL)//only check for enemies if you can see your squad
        {
            foreach (Soldier sold in soldiersFound)
            {
                if (sold.GetOwnTeam() != myTeam)
                {
                    result.enemiesSpotted.Add(sold);
                }
            }
        }

        return result;
    }

    // ---------- private methods

    private Soldier[] GetSoldiersInVincinity()
    {
        List<Soldier> soldiersFound = new List<Soldier>();

        Vector2Int curPos = mySoldier.tileCoord;
        int range = mySoldier.rangeView;
        int rangeSQR = range * range;

        for (int i=curPos.x - range; i <= curPos.x + range; i++)
        {
            for (int j = curPos.y - range; j <= curPos.y + range; j++)
            {
                Vector2Int curTile = new Vector2Int(i, j);
                if ( (curTile - curPos).sqrMagnitude <= rangeSQR && curTile != curPos)//is current Tile in a circular range (and not our tile)
                {
                    Entity newSoldier = TilemapManager.GetSoldierS(i, j);

                    if (newSoldier != null && newSoldier.GetType() != typeof(Base))
                        soldiersFound.Add((Soldier)newSoldier);
                }
            }
        }

        return soldiersFound.ToArray();
    }
}
