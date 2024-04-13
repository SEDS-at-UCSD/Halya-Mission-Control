import logo from './logo.svg';
import './App.css';
import mqtt from "mqtt";
import { useState, useEffect } from "react";
import Toolbar from './toolbar.js'

function App() {
  const connectionurl = "ws://169.254.32.191:9002";
  const topics_list = [];

  const video_feed_links = [
    "http://localhost:6969/video_feed/0",
    "http://localhost:6969/video_feed/1",
    "http://localhost:6969/video_feed/0",
    "http://localhost:6969/video_feed/1",
    "http://localhost:6969/video_feed/0"
  ]

  const [feedAmount, setFeedAmount] = useState(4);

  const [client, setClient] = useState(null);
  const [connectStatus, setConnectStatus] = useState("Not connected");
  const [boardData, setBoardData] = useState({});
  const [isSub, setIsSub] = useState(false);
  const [feedStates, setFeedStates] = useState([0,1,2,3]);
  const [focusedDiv, setFocusedDiv] = useState(null);

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

  const handleFocus = (index) => {
    setFocusedDiv(index);
  };

  return (
    <div className="App">
      <div 
        className="top_bar"
        onClick={()=>handleFocus(null)}>
        <Toolbar />
      </div>
      <div className="image_grid">
        {/* Always show the first image */}
        <div
          className={`image_container ${focusedDiv === 0 ? 'focused' : ''}`}
          onClick={() => handleFocus(0)}
          tabIndex="0" // Make div focusable
        >
          <img src={video_feed_links[feedStates[0]]} alt="Video Stream" />
        </div>

        {/* Conditionally show the second image */}
        {feedAmount >= 2 && (
          <div
            className={`image_container ${focusedDiv === 1 ? 'focused' : ''}`}
            onClick={() => handleFocus(1)}
            tabIndex="0"
          >
            <img src={video_feed_links[feedStates[1]]} alt="Video Stream" />
          </div>
        )}

        {/* Conditionally show the third and fourth images */}
        {feedAmount === 4 && [
          <div
            className={`image_container ${focusedDiv === 2 ? 'focused' : ''}`}
            onClick={() => handleFocus(2)}
            tabIndex="0"
            key="image3"
          >
            <img src={video_feed_links[feedStates[2]]} alt="Video Stream" />
          </div>,
          <div
            className={`image_container ${focusedDiv === 3 ? 'focused' : ''}`}
            onClick={() => handleFocus(3)}
            tabIndex="0"
            key="image4"
          >
            <img src={video_feed_links[feedStates[3]]} alt="Video Stream" />
          </div>,
        ]}
      </div>
    </div>
  );
}

export default App;
