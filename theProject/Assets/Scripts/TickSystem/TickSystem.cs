using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class TickSystem : MonoBehaviour
{
    public class OnTickEventArgs : EventArgs
    {
        public int tickNumber;
    }

    public static Action<OnTickEventArgs> OnTick;

    private const float TICK_PERIOD = 0.2f; // seconds between ticks
    private int tick; // keep track of total ticks that have happened
    public static TickSystem Instance;

    private void Awake() // needs to be called by a scene initializer
    {
        if (Instance != null) // a TickSystem already exitst
        {
            Debug.LogError("A TickSystem already exists, FIX YOUR TIME SPAWNING");
            Destroy(gameObject);
        }//else this is the first TickSystem that has awoken in this scene
        Instance = this;
        tickTimer = 0f;
        tick = 0;
    }

    private float tickTimer = 0f;

    // Update is called once per frame
    void Update()
    {
        tickTimer += Time.deltaTime;
        if (tickTimer >= TICK_PERIOD)
        {
            tickTimer -= TICK_PERIOD;
            tick++;

            OnTick?.Invoke(new OnTickEventArgs { tickNumber = tick });
        }
    }
}

