using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using System.IO;
using Newtonsoft.Json.Linq;

public class MapBuilder : MonoBehaviour
{
    JObject map_def;
    static MapBuilder()
    {
    }
    public void Start()
    {
        map_def = JObject.Parse(File.ReadAllText(Application.dataPath + @"\mods\test\entity_list.json"));
    }
    public void build_map(byte[] data)
    {
        print(123);
    }
}
