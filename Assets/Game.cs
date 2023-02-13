using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Game : MonoBehaviour
{

    [SerializeField] UdpSocket udpSocket = null;
    [SerializeField] Canvas canvasMainMenu = null;
    [SerializeField] MapBuilder mapBuilder = null;
    private TMP_Text InputLevel = null;

    private void Start()
    {
        var objects = GameObject.FindGameObjectsWithTag("UI_inputText");
        foreach (var obj in objects)
        {
            if (obj.name == "InputLevel")
                InputLevel = obj.GetComponent<TMP_Text>();
        }

        udpSocket.receiveMapInfo += (e) => { mapBuilder.build_map(e.data); };
    }

    public void RunServer()
    {
        var sceneName = InputLevel.text;

        canvasMainMenu.enabled = false;

        udpSocket.RunServer();
        udpSocket.SendData(sceneName);
    }
}
