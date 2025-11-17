"""Valetudo MQTT Client"""

import json
import logging
from typing import Callable, Dict, Any, Optional
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class ValetudoMQTTClient:
    """Client for Valetudo MQTT interface"""

    def __init__(
        self,
        broker: str,
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_topic: str = "valetudo"
    ):
        """Initialize Valetudo MQTT client

        Args:
            broker: MQTT broker address
            port: MQTT broker port
            username: MQTT username (optional)
            password: MQTT password (optional)
            base_topic: Base topic for Valetudo messages
        """
        self.broker = broker
        self.port = port
        self.base_topic = base_topic

        self.client = mqtt.Client()

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        # Message handlers
        self.handlers: Dict[str, Callable] = {}

        logger.info(f"Initialized Valetudo MQTT client: {broker}:{port}")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to MQTT broker"""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            # Subscribe to all Valetudo topics
            topics = [
                f"{self.base_topic}/state",
                f"{self.base_topic}/map",
                f"{self.base_topic}/attributes",
            ]
            for topic in topics:
                client.subscribe(topic)
                logger.debug(f"Subscribed to {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects from MQTT broker"""
        if rc != 0:
            logger.warning(f"Unexpected disconnect from MQTT broker: {rc}")

    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received"""
        topic = msg.topic
        try:
            payload = json.loads(msg.payload.decode())
            logger.debug(f"Received message on {topic}: {payload}")

            # Call registered handlers
            for pattern, handler in self.handlers.items():
                if pattern in topic:
                    handler(topic, payload)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            logger.info("MQTT client started")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT client disconnected")

    def register_handler(self, topic_pattern: str, handler: Callable[[str, Dict[str, Any]], None]):
        """Register a message handler for a topic pattern

        Args:
            topic_pattern: Topic pattern to match (e.g., "state", "map")
            handler: Callback function (topic, payload) -> None
        """
        self.handlers[topic_pattern] = handler
        logger.debug(f"Registered handler for pattern: {topic_pattern}")

    def publish(self, topic_suffix: str, payload: Dict[str, Any]):
        """Publish a message to Valetudo

        Args:
            topic_suffix: Topic suffix (e.g., "command")
            payload: JSON payload to publish
        """
        topic = f"{self.base_topic}/{topic_suffix}"
        message = json.dumps(payload)
        self.client.publish(topic, message)
        logger.debug(f"Published to {topic}: {payload}")

    # Convenience methods for common subscriptions

    def on_state_change(self, handler: Callable[[Dict[str, Any]], None]):
        """Register handler for state changes

        Args:
            handler: Callback function (state_data) -> None
        """
        def wrapper(topic, payload):
            handler(payload)
        self.register_handler("state", wrapper)

    def on_map_update(self, handler: Callable[[Dict[str, Any]], None]):
        """Register handler for map updates

        Args:
            handler: Callback function (map_data) -> None
        """
        def wrapper(topic, payload):
            handler(payload)
        self.register_handler("map", wrapper)

    def on_attributes_change(self, handler: Callable[[Dict[str, Any]], None]):
        """Register handler for attribute changes

        Args:
            handler: Callback function (attributes_data) -> None
        """
        def wrapper(topic, payload):
            handler(payload)
        self.register_handler("attributes", wrapper)
