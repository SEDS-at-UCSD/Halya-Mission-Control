import logo from './logo.svg';
import './App.css';
import mqtt from "mqtt";
import { useState, useEffect } from "react";
import ReactPlayer from "react-player";

function App() {
  const connectionurl = "ws://169.254.32.191:9002";
  const topics_list = []

  const [client, setClient] = useState(null);
  const [connectStatus, setConnectStatus] = useState("Not connected");
  const [boardData, setBoardData] = useState({});
  const [isSub, setIsSub] = useState(false);

  const mqttSub = (topic) => {
    if (client) {
      client.subscribe(topic, (error) => {
        if (error) {
          console.log("Subscribe to " + topic + " error", error)
          return
        }
      });
    }
  };

  const sendMessage = (topic, message) => {
    client.publish(topic,message,(error)=>{
      if (error) {
        console.log("Publish to " + topic + " error", error)
        return
      }
    })
  }

  useEffect(()=> { 
    const mqttConnect = (host, mqttOption) => {
      setConnectStatus('Connecting');
      setClient(mqtt.connect(host, mqttOption));
    };

    const initialConnectionOptions = {
      protocol: 'ws',
      clientId: 'emqx_react_' + Math.random().toString(16).substring(2, 8),
      username: 'emqx_test',
      password: 'emqx_test',
    };

    mqttConnect(connectionurl,initialConnectionOptions);
  }, []);

  useEffect(() => {
    if (client) {
      client.on('connect', () => {
        setConnectStatus('Connected');
        topics_list.forEach((topic)=>{
          mqttSub(topic);
        })
        mqttSub("switch_states_status_4");
        mqttSub("switch_states_status_5");
      });

      client.on('error', (err) => {
        console.error('Connection error: ', err);
        client.end();
      });

      client.on('reconnect', () => {
        setConnectStatus('Lost connection, attempting to reconnect');
      });

      client.on('message', (topic, message) => {
        message = JSON.parse(String(message));
        if (!isSub && topic === "topics_list") {
          message.topics.forEach((subscription)=>{
            mqttSub(subscription);
          });
          setIsSub(true);
        }
        else {
          setBoardData((prev)=>{
            return { ...prev, [topic]: message };
          })
        }
      });
    }
  }, [client]);

  return (
    <div className="App">
      <img src="http://localhost:6969/video_feed/1" alt="Video Stream" />
    </div>
  );
}

export default App;
