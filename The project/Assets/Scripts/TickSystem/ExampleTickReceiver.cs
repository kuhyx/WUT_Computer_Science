using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExampleTickReceiver : MonoBehaviour
{
    void Awake()
    {
        TickSystem.OnTick += HandleTick;
    }

    private void HandleTick(TickSystem.OnTickEventArgs tickEventArgs)
	{
        Debug.Log($"Example of tick #{tickEventArgs.tickNumber} being handled");
	}
}
