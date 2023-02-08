using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Game : MonoBehaviour
{

    [SerializeField] UdpSocket udpSocket = null;
    [SerializeField] Canvas canvasMainMenu = null;


    public void RunServer()
    {
        //udpSocket.StopServer();
        //udpSocket.RunServer();
        SceneManager.LoadScene("game", LoadSceneMode.Additive);
        canvasMainMenu.enabled = false;
    }


}
