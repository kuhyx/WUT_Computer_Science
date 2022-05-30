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

    public void Initialize(float _viewRange, Soldier _mySoldier, Entity.Team _myTeam)
    {
        viewRange = _viewRange;
        mySoldier = _mySoldier;
        myTeam = _myTeam;
    }

    public CommunicationResult HandleCommuncation()
    {
        CommunicationResult result = new CommunicationResult();
        result.resetTTL = false;
        result.enemiesSpotted = new List<Soldier>();

        // look for soldiers in vincinity

        // send Keep Alive (myTeam) - reset TTL (myTTL)

        // look fo enemies (enemyTeam) - add Enemies to enemiesSpotted (send List<Enemies>)

        return result;
    }

    // ---------- private methods

    private Soldier[] GetSoldiersInVincinity()
    {
        //TO DO - implement
        Physics.SphereCastAll()

        return null;
    }
}
