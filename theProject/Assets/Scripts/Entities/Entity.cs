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


    public Team GetOwnTeam()
	{
        return myTeam;
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

    public void SetOwnTeam(Team type)
    {
        myTeam = type;
    }

    public void ReduceHP(float damage)
    {
        healthPoints -= damage;

        if (healthPoints <= 0)
            Destroy(gameObject);

        UpdateHPDisplay();
        Debug.Log("I took damage, my HP is now: " + healthPoints + " noooo!!!!", gameObject);
    }

    protected virtual void Die()
    {
        OnDeath.Invoke(this);
        Destroy(gameObject);
    }

    private void OnDestroy()
    {
        Debug.Log("Soldier: " + myTeam.ToString() + " has died", gameObject);
    }


    protected void UpdateHPDisplay()
	{
        healthPointsText.text = healthPoints.ToString() + "/" + maxHealthPoints.ToString();
    }
}
