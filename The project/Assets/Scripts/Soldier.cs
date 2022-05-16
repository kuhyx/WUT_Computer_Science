using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Soldier : MonoBehaviour
{
    public enum SoldierType
    {
        Ally,
        Enemy
    } 
    [SerializeField] private Transform target; 
    [SerializeField]  private SoldierType enemyType;
    [SerializeField]  private SoldierType ourType;
    [SerializeField]  private float healthPoints = 1;
    [SerializeField]  private float rangeAttack = 1;
    [SerializeField]  private float rangeView = 1;
    [SerializeField]  private float damageAttack = 1;
    [SerializeField]  private float speedAttack = 1;
    // Start is called before the first frame update
    void Start(){
        setEnemyTag();
    }

    public void setOwnTag(SoldierType type)
    {
        ourType = type;
    }

    public void setEnemyTag()
    {
        if(ourType == SoldierType.Ally) enemyType = SoldierType.Enemy;
        else enemyType = SoldierType.Ally;
    }

    void Awake()
    {
        TickSystem.OnTick += HandleTick;
    }
    private void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
        UpdateTarget();
	}

    void UpdateTarget ()
    {
        // Enemies are the game objects tagged with the "Enemy"
        GameObject[] enemies = GameObject.FindGameObjectsWithTag(enemyType);
        Debug.Log(enemies.Length);
        // We have not found enemy yet so the distance to enemy is "infinite"
        float shortestDistance = Mathf.Infinity; 
        GameObject nearestEnemy = null;
        foreach ( GameObject enemy in enemies)
        {
            // Go through each enemy existing
            // Calculate distance to this enemy
            float distanceToEnemy = Vector3.Distance(transform.position, enemy.transform.position);
            if (distanceToEnemy < shortestDistance) 
            {
                shortestDistance = distanceToEnemy;
                nearestEnemy = enemy; 
            }
        }

        if (nearestEnemy != null && shortestDistance <= rangeAttack)
        {
            target = nearestEnemy.transform;
        }
    }

    // Update is called once per frame
    void Update()
    {
       if (target == null) return; 
    }

    /* https://www.youtube.com/watch?v=QKhn2kl9_8I 08:54 Soldier attack
    void OnDrawGizmosSelected ()
    {

    }
    */
}
