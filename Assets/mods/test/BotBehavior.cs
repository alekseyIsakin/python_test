using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BotBehavior : MonoBehaviour
{
    [SerializeField] Material BaseMaterials;
    [SerializeField] List<Material> Materials;
    // Start is called before the first frame update
    [SerializeField] public int id;

    internal void setID(int id)
    {
        this.id = id;
        var MatRender = GetComponentInChildren<MeshRenderer>();

        if (id >= Materials.Count)
            MatRender.material = BaseMaterials;
        else
            MatRender.material = Materials[id];
    }

    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
