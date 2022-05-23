using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Events;

public class Soldier : MonoBehaviour
{
    private Queue<Action> actions = new Queue<Action>();
    private Queue<Action> interrupts = new Queue<Action>();
    #region Action Queue Items
    abstract class Action // action "template"
	{
        public virtual void Execute(Soldier soldier, TickSystem.OnTickEventArgs tickEventArgs) { } // called by Soldier when action is supposed to be done
	}

    private class Movement : Action 
    {
		public override void Execute(Soldier soldier, TickSystem.OnTickEventArgs tickEventArgs)
		{//TO DO: CALL PROPER FUNCTION TO MOVE
            throw new System.NotImplementedException($"(tick: {tickEventArgs.tickNumber}) Trying to teleport to {soldier.movementDestination}");
			//??tileMap.Teleport(movementDestination)
		}
	}
    private class TryAttack : Action
    {
        public override void Execute(Soldier soldier, TickSystem.OnTickEventArgs tickEventArgs)
        {
            //Debug.LogWarning($"(tick: {tickEventArgs.tickNumber}) Looking for enemy in range");
            if(soldier.TryAttackEnemy())
                soldier.lastAttackTick = tickEventArgs.tickNumber;
        }
    }
	#endregion

	#region Handling Incoming Orders (Interrupts) 
    public void HandleMovementOrder(Vector2Int destination)
	{
        movementDestination = destination;
        interrupts.Enqueue(new Movement()); // force soldier to find path to the new destination
	}
	#endregion
	public enum SoldierType
    {
        Ally,
        Enemy
    }
    [Header("Values")]
    [SerializeField] private float maxHealthPoints = 10;
    [SerializeField] private float healthPoints = 1;
    [SerializeField] private float rangeAttack = 100;
    [SerializeField] private float rangeView = 1;
    [SerializeField] private float damageAttack = 1;
    [SerializeField] private int speedAttack = 1; // ticks between attacks
    [SerializeField] private int lastAttackTick = -1;
    [Header("References")]
    [SerializeField] private TMP_Text nameText = null;
    [SerializeField] private TMP_Text healthPointsText = null;
    [Header("Do-not-change-in-game values")]
    [SerializeField] private Soldier target;
    [SerializeField] private SoldierType enemyType;
    [SerializeField] private SoldierType ourType;

    [SerializeField] private Vector2Int movementDestination = Vector2Int.zero;

    // variables not visible in inspector

    [HideInInspector] public UnityEvent onDeath = new UnityEvent();

    public SoldierType TempGetOwnType()
	{
        return ourType;
	}

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
        onDeath.Invoke();

        Debug.Log("Soldier: " + ourType.ToString() + " has died", gameObject);
    }

    private void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
        ref Queue<Action> queueToHandle = ref interrupts;
        if (interrupts.Count < 1) // if no interrupt actions to do, handle regular queue
            queueToHandle = actions;

        if(queueToHandle.Count > 0)
            queueToHandle.Dequeue().Execute(this, tickEventArgs);
        else
		{
            if(lastAttackTick + speedAttack <= tickEventArgs.tickNumber)
			{
                queueToHandle.Enqueue(new TryAttack());
                queueToHandle.Dequeue().Execute(this, tickEventArgs);
            }
		}
	}

    bool TryAttackEnemy () //returns true if an enemy was attacked
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
        
        return target != null;
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
