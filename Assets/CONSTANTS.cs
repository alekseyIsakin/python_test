using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.IO;
using UnityEditor.UIElements;

public class CONSTANTS : MonoBehaviour
{
    public int field = 0;
    JObject map_def = JObject.Parse(File.ReadAllText(Application.dataPath + @"mods\test\entity_list.json"));
    static CONSTANTS()
    {
        print(123);
    }

}
