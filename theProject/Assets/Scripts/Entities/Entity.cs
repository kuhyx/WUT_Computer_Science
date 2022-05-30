using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Events;

public class Entity : MonoBehaviour
{
	public enum Team
    {
        Ally,
        Enemy
    } 
    [Header("Values")]
    [SerializeField] protected Team myTeam;
    [SerializeField] protected float maxHealthPoints = 100;
    [SerializeField] protected float healthPoints = 100;

    [SerializeField] protected TMP_Text nameText = null;
    [SerializeField] protected TMP_Text healthPointsText = null;

    [HideInInspector] public UnityEvent<Entity> OnDeath = new UnityEvent<Entity>();

    [SerializeField] protected Vector2Int tileCoord;

    [SerializeField] protected Vector3 WORLD_SPACE_OFFSET = new Vector3(0.5f, 0.5f, 0.5f);

    public Team GetOwnTeam()
	{
        return myTeam;
	}

    public Vector2Int GetTileCoord()
    {
        return tileCoord;
    }

    // Start is called before the first frame update
    protected virtual void Start(){
        healthPoints = maxHealthPoints; // initialize health
        UpdateHPDisplay();

        Debug.Log("Entity: " + myTeam.ToString() + " has appeared", gameObject);

        switch (myTeam)
        {
            case Team.Ally:
                nameText.text = "Ally";
                nameText.color = Color.blue;
                break;
            case Team.Enemy:
                nameText.text = "Enemy";
                nameText.color = Color.red;
                break;
            default:
                nameText.text = "how did we get here (forever)";
                nameText.color = new Color(255, 192, 203);
                break;
        }
    }

    protected virtual void Awake()
    {
        TickSystem.OnTick += HandleTick;
    }

    protected virtual void Die()
    {
        TickSystem.OnTick -= HandleTick;
        OnDeath.Invoke(this);
        Destroy(gameObject);
    }

    public void SetOwnTeam(Team type)
    {
        myTeam = type;
    }

    public void ReduceHP(float damage)
    {
        healthPoints -= damage;

        if (healthPoints <= 0)
            Die();

        UpdateHPDisplay();
        Debug.Log("I took damage, my HP is now: " + healthPoints + " noooo!!!!", gameObject);
    }

    protected virtual void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
        
	}

    private void OnDestroy()
    {
        Debug.Log("Soldier: " + myTeam.ToString() + " has died", gameObject);
    }


    protected void UpdateHPDisplay()
	{
        healthPointsText.text = healthPoints.ToString() + "/" + maxHealthPoints.ToString();
    }
    public void SetTileCoords(Vector2Int tileCoordinates)
    {
        tileCoord = tileCoordinates;
    }
}
