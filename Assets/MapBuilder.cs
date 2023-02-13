using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Linq;
using System;
using Unity.VisualScripting;

public class MapBuilder : MonoBehaviour
{
    JObject map_def;
    [SerializeField] GameObject prefabFloor = null;
    [SerializeField] GameObject prefabWall = null;
    [SerializeField] GameObject prefabBot = null;

    static private byte[] FLOOR_BYTES;
    static private byte[] WALL_BYTES;
    static private byte[] INFO_BYTES;
    static private byte MAP;
    static private byte SEPARATE_BYTE;
    static private byte NEWLINE;
    static private byte NEWFLOOR;
    static private byte ENDMAP;

    static private byte BOT_SECTION;
    static private byte BOT_ID;
    static private byte BOT_START;
    static private byte BOT_END_SECTION;

    private Vector3 position = Vector3.zero;
    private Vector3 cellSize = Vector3.one * 1;
    private byte[] mapInfo = { };
    private bool u = false;

    public void Start()
    {
        map_def = JObject.Parse(File.ReadAllText(Application.dataPath + @"\mods\test\entity_list.json"));
        MapBuilder.FLOOR_BYTES = map_def.GetValue("FLOOR").Select(x => (byte)x).ToArray();
        MapBuilder.WALL_BYTES = map_def.GetValue("WALL").Select(x => (byte)x).ToArray();
        MapBuilder.INFO_BYTES = map_def.GetValue("INFO").Select(x => (byte)x).ToArray();
        MapBuilder.MAP = (byte)map_def.GetValue("map");

        MapBuilder.SEPARATE_BYTE = (byte)map_def.GetValue("SEPARATE");
        MapBuilder.NEWLINE = (byte)map_def.GetValue("endline");
        MapBuilder.NEWFLOOR = (byte)map_def.GetValue("endfloor");
        MapBuilder.ENDMAP = (byte)map_def.GetValue("endmap");
        
        MapBuilder.BOT_SECTION = (byte)map_def.GetValue("BOT");
        MapBuilder.BOT_ID = (byte)map_def.GetValue("BOTID");
        MapBuilder.BOT_START = (byte)map_def.GetValue("BOTSTART");
        MapBuilder.BOT_END_SECTION = (byte)map_def.GetValue("ENDBOT");

    }
    public void Update()
    {
        if (mapInfo.Length != 0)
        {
            buildMap(mapInfo);
            mapInfo = Array.Empty<byte>();
            print("Map sucsefully rebuilded");
        }
    }

    public void RebuildMap(byte[] data)
    {
        print("Map must be rebuilded");
        mapInfo = data;
    }

    protected void loadBots(byte[] data, int start)
    {
        int cursor = start;
        if (data[cursor] != BOT_SECTION)
            throw new Exception($"Not a bot [{data[cursor]}]");
        cursor += 1;

        while (cursor < data.Length )
        {
            if (data[cursor] == BOT_END_SECTION)
                break;

            if (data[cursor] != BOT_ID)
                    throw new Exception($"Bad bot id [{cursor}]=>[{data[cursor]}]");
            cursor += 1;

            byte[] value = data.Skip(cursor).Take(4).ToArray();
            cursor += 4;
            int id = BitConverter.ToInt32(value);

            if (data[cursor] != BOT_START)
                throw new Exception($"Bad bot position [{cursor}]=>[{data[cursor]}]");
            cursor += 1;

            value = data.Skip(cursor).Take(4).ToArray();
            cursor += 4;
            int x_pos = BitConverter.ToInt32(value);

            value = data.Skip(cursor).Take(4).ToArray();
            cursor += 4;
            int y_pos = BitConverter.ToInt32(value);

            value = data.Skip(cursor).Take(4).ToArray();
            cursor += 4;
            int z_pos = BitConverter.ToInt32(value);

            placeBot(id, new Vector3(x_pos, y_pos, z_pos));
        }
    }
    public bool IsMap(byte[] data)
    {
        return data[0] == MAP;
    }
    protected void buildMap(byte[] data)
    {
        int i = 0;

        for (i = 0; i< data.Length; i++)
        {
            byte b = data[i];
            int first = b >> 4;

            if (b == SEPARATE_BYTE)
            {
                position.x += cellSize.x;
                continue;
            }
            if (FLOOR_BYTES.Contains((byte)first))
            {
                placeFloor(position);
                position.x += cellSize.x;
            }
            if (WALL_BYTES.Contains((byte)first))
            {
                placeWall(position);
                position.x += cellSize.x;
            }
            if (INFO_BYTES.Contains((byte)first))
            {
                if (b == NEWLINE)
                {
                    position.z += cellSize.z;
                    position.x = 0;
                }
                if (b == NEWFLOOR)
                {
                    position.y += cellSize.y;
                    position.x = 0;
                    position.z = 0;
                }
                if (b == ENDMAP)
                    break;
                continue;
            }
        }

        loadBots(data, ++i);
    }

    private void placeWall(Vector3 position)
    {
        var o = Instantiate(prefabWall, position, Quaternion.identity);
        o.transform.parent = this.transform.GetChild(0);
    }

    private void placeFloor(Vector3 position)
    {
        var o = Instantiate(prefabFloor, position, Quaternion.identity);
        o.transform.parent = this.transform.GetChild(0);
    }

    private void placeBot(int id, Vector3 position)
    {
        var o = Instantiate(prefabBot, position, Quaternion.identity);
        o.GetComponent<BotBehavior>().setID(id);
        o.transform.parent = this.transform.GetChild(1);
    }
}
