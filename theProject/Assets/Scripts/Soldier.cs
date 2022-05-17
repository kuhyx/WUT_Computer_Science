using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class Soldier : MonoBehaviour
{
    public enum SoldierType
    {
        Ally,
        Enemy
    } 
    [SerializeField] private Soldier target; 
    [SerializeField] private SoldierType enemyType;
    [SerializeField] private SoldierType ourType;
    [SerializeField] private float maxHealthPoints = 10;
    [SerializeField] private float healthPoints = 1;
    [SerializeField] private float rangeAttack = 100;
    [SerializeField] private float rangeView = 1;
    [SerializeField] private float damageAttack = 1;
    [SerializeField] private float speedAttack = 1;

    [SerializeField] private TMP_Text nameText = null;
    [SerializeField] private TMP_Text healthPointsText = null;
    // Start is called before the first frame update
    void Start(){
        healthPoints = maxHealthPoints; // initialize health
        UpdateHPDisplay();
        setEnemyTag();

        Debug.Log("Soldier: " + ourType.ToString() + " has appeared", gameObject);

        switch (ourType)
        {
            case SoldierType.Ally:
                nameText.text = "Ally";
                nameText.color = Color.blue;
                break;
            case SoldierType.Enemy:
                nameText.text = "Enemy";
                nameText.color = Color.red;
                break;
            default:
                nameText.text = "how did we get here (forever)";
                nameText.color = new Color(255, 192, 203);
                break;
        }
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

    private void OnDestroy()
    {
        TickSystem.OnTick -= HandleTick;

        Debug.Log("Soldier: " + ourType.ToString() + " has died", gameObject);
    }

    private void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
        UpdateTarget();
        // ADD TICK SYSTEM PREFAB ON SCENE
	}

    void UpdateTarget ()
    {
        // Enemies are the game objects tagged with the "Enemy"
        //GameObject[] enemies = GameObject.FindGameObjectsWithTag(enemyType);
        Soldier[] soldiers = GameObject.FindObjectsOfType<Soldier>();

        List<Soldier> enemiesList = new List<Soldier>();

        foreach (Soldier obj in soldiers)
        {
            if (obj.ourType == enemyType)
                enemiesList.Add(obj);
        }

        Soldier[] enemies = enemiesList.ToArray();

        // We have not found enemy yet so the distance to enemy is "infinite"
        float shortestDistance = Mathf.Infinity; 
        Soldier nearestEnemy = null;
        foreach ( Soldier enemy in enemies)
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
            target = nearestEnemy;
        }
        else
            target = null;

        if (target != null)
            target.ReduceHP(damageAttack);
    }

    // Update is called once per frame
    void Update()
    {
       //if (target == null) return; 
    }

    /* https://www.youtube.com/watch?v=QKhn2kl9_8I 08:54 Soldier attack
    void OnDrawGizmosSelected ()
    {

    }
    */

    private void ReduceHP(float damage)
    {
        healthPoints -= damage;

        if (healthPoints <= 0)
            Destroy(gameObject);

        UpdateHPDisplay();
        Debug.Log("I took damage, oh  my HP is now: " + healthPoints + " noooo!!!!", gameObject);
    }

    private void UpdateHPDisplay()
	{
        healthPointsText.text = healthPoints.ToString() + "/" + maxHealthPoints.ToString();
    }
}
