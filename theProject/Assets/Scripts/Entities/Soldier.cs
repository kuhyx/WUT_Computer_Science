using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Events;

public class Soldier : Entity
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

    [Header("Soldier Values")]
    [SerializeField] private float rangeAttack = 100;
    [SerializeField] private float rangeView = 1;
    [SerializeField] private float damageAttack = 1;
    [SerializeField] private int speedAttack = 1; // ticks between attacks
    [SerializeField] private int lastAttackTick = -1;
    [Header("References")]
    [Header("Do-not-change-in-game values")]
    [SerializeField] private Entity target;
    [SerializeField] private Team enemyType;

    [SerializeField] private Vector2Int movementDestination = Vector2Int.zero;
	
    // Start is called before the first frame update
    protected override void Start(){
        base.Start();
        SetEnemyTag();
    }

    public void SetEnemyTag()
    {
        if(myTeam == Team.Ally) enemyType = Team.Enemy;
        else enemyType = Team.Ally;
    }

    void Awake()
    {
        TickSystem.OnTick += HandleTick;
    }

	protected override void Die()
	{
        TickSystem.OnTick -= HandleTick;
        base.Die();
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
        Entity[] soldiers = GameObject.FindObjectsOfType<Entity>();

        List<Entity> enemiesList = new List<Entity>();

        foreach (Entity obj in soldiers)
        {
            if (obj.GetOwnTeam() == enemyType)
                enemiesList.Add(obj);
        }

        Debug.Log(soldiers.Length);
        Debug.Log(enemiesList.Count);
        Entity[] enemies = enemiesList.ToArray();

        // We have not found enemy yet so the distance to enemy is "infinite"
        float shortestDistance = Mathf.Infinity;
        Entity nearestEnemy = null;
        foreach (Entity enemy in enemies)
        {
            // Go through each enemy existing
            // Calculate distance to this enemy
            float distanceToEnemy = Vector3.Distance(transform.position,
                enemy.transform.position);
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
}
