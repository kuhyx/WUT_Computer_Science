using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class Base : MonoBehaviour
{
	public enum SoldierType
    {
        Ally,
        Enemy
    } 
    [SerializeField] private SoldierType ourType;
    [SerializeField] private float maxHealthPoints = 10;
    [SerializeField] private float healthPoints = 1;

    [SerializeField] private TMP_Text nameText = null;
    [SerializeField] private TMP_Text healthPointsText = null;

    public SoldierType TempGetOwnType()
	{
        return ourType;
	}

    // Start is called before the first frame update
    void Start(){
        healthPoints = maxHealthPoints; // initialize health
        UpdateHPDisplay();

        Debug.Log("Base: " + ourType.ToString() + " has appeared", gameObject);

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

    private void OnDestroy()
    {
        Debug.Log("Soldier: " + ourType.ToString() + " has died", gameObject);
    }
    private void ReduceHP(float damage)
    {
        healthPoints -= damage;

        if (healthPoints <= 0)
            Destroy(gameObject);

        UpdateHPDisplay();
        Debug.Log("I took damage, my HP is now: " + healthPoints + " noooo!!!!", gameObject);
    }

    private void UpdateHPDisplay()
	{
        healthPointsText.text = healthPoints.ToString() + "/" + maxHealthPoints.ToString();
    }
}
