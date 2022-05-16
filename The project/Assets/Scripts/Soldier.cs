using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Soldier : MonoBehaviour
{
    private const string enemyTag = "Enemy";
    private const float healthPoints = 1;
    private const float rangeAttack = 1;
    private const float rangeView = 1;
    private const float damageAttack = 1;
    private const float speedAttack = 1;
    // Start is called before the first frame update
    void Start(){
        InvokeRepeating("UpdateTarget", 0f, 0.5f); 
        // Call UpdateTarget method at the begining of the Start() 
        // and repeat every 0.5 second
        
    }

    void UpdateTarget ()
    {
        // Enemies are the game objects tagged with the "Enemy"
        GameObject[] enemies = GameObject.FindGameObjectsWithTag(enemyTag);
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
            target = nearestEnemey.transform;
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
