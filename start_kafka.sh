# #!/bin/bash

# # Kafka installation directory
# KAFKA_HOME="/home/ronak/Desktop/sem_2_ubuntu/kafka_2.13-3.7.0"

# # Start Zookeeper server in a new terminal
# gnome-terminal --title="Zookeeper" -- bash -c "$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties; read -p 'Press Enter to close this terminal'"

# # Start Kafka Broker in a new terminal
# gnome-terminal --title="Kafka Broker" -- bash -c "$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties; read -p 'Press Enter to close this terminal'"


# #!/bin/bash

# # Get the current directory
# CURRENT_DIR="$(pwd)"

# # Kafka installation directory
# KAFKA_HOME="$CURRENT_DIR/kafka_2.13-3.7.0"

# # Start Zookeeper server in a new terminal
# gnome-terminal --title="Zookeeper" -- bash -c "$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties; read -p 'Press Enter to close this terminal'"

# # Start Kafka Broker in a new terminal
# gnome-terminal --title="Kafka Broker" -- bash -c "$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties; read -p 'Press Enter to close this terminal'"


#!/bin/bash

# Get the current directory
CURRENT_DIR="$(pwd)"

# Kafka installation directory
KAFKA_HOME="$CURRENT_DIR/kafka_2.13-3.7.0"

# Start Zookeeper server in a new terminal
gnome-terminal --title="Zookeeper" -- bash -c "$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties; echo 'Zookeeper started'; read -p 'Press Enter to close this terminal'"

# Wait for Zookeeper to start (assuming default port is 2181)
echo "Waiting for Zookeeper to start..."
while ! nc -z localhost 2181; do   
    sleep 1 # Wait 1 second before checking again
done
echo "Zookeeper has started"

# Start Kafka Broker in a new terminal
gnome-terminal --title="Kafka Broker" -- bash -c "$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties; echo 'Kafka Broker started'; read -p 'Press Enter to close this terminal'"

