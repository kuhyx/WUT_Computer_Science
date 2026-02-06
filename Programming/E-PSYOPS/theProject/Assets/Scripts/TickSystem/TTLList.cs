using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class TTLList<T> where T : UnityEngine.Object
{
    private Dictionary<T, int> dict = new Dictionary<T, int>();
    public List<T> viewList;//DO NOT EDIT (FOR DEBUG PURPOSES ONLY)
    bool isSquad = false;
    int basicTTL = 5;

    // ---------- methods

    public void Initialize(bool squad, int bTTL)
    {
        isSquad = squad;
        basicTTL = bTTL;
    }

    public void AddToList(T obj)
    {
        if (dict.ContainsKey(obj))
            dict[obj] = basicTTL;
        else
            dict.Add(obj, basicTTL);
        UpdateViewList();
    }

    public void RemoveFromList(T obj)
    {
        dict.Remove(obj);
        UpdateViewList();
    }

    public void OnTick(TickSystem.OnTickEventArgs eventArgs)
    {
        List<T> keys = new List<T>(dict.Keys);

        if (isSquad && keys.Count <= 1)
            return;

        foreach (T key in keys)
        {
            dict[key] -= 1;
            if (dict[key] <= 0 && !(isSquad && dict.Keys.Count <= 1))
            {
                dict.Remove(key);
                Debug.Log("Lost view of soldier due to TTL:", key);
                UpdateViewList();
            }
            else if (isSquad && dict.Keys.Count <= 1)
            {
                dict[key] = basicTTL;
            }
        }
    }

    public List<T> GetTList()
    {
        return new List<T>(dict.Keys);
    }

    public int GetCount()
    {
        return dict.Count;
    }

    // ---------- private methods

    // DEBUG - Changes a view list to see soldiers active in squad in inspector
    private void UpdateViewList()
    {
        viewList = new List<T>(dict.Keys);
    }
}
