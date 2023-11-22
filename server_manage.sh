#!/bin/bash

SERVER_DIR="/home/mincraft/kosmo"
JAR_FILE="forge-1.16.5-36.2.34.jar"
SCREEN_NAME="minecraft_server"
RAM_MAX="15G"
RESTART_WARNING_TIME=300  # 5 minutes in seconds
RESTART_FINAL_WARNING_TIME=20  # 20 seconds in seconds

start_server() {
    cd "$SERVER_DIR"
    screen -dmS "$SCREEN_NAME" java -XX:+UseG1GC -Xmx14G -Xms14G -Dsun.rmi.dgc.server.gcInterval=600000 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32 -jar "$JAR_FILE" nogui
    echo "Minecraft server started in a screen session named '$SCREEN_NAME'."
}

stop_server() {
    screen -S "$SCREEN_NAME" -X stuff "stop$(printf \\r)"
    echo "Stopping Minecraft server..."
    echo "Waiting 20 seconds for shutdown..."
    sleep 20
    screen -ls | grep "$SCREEN_NAME" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Server did not stop gracefully, forcing shutdown."
        screen -S "$SCREEN_NAME" -X quit
    else
        echo "Minecraft server stopped."
    fi
}

broadcast_message() {
    screen -S "$SCREEN_NAME" -X stuff "title @a title $1$(printf \\r)"
}

server_status() {
    screen -ls | grep "$SCREEN_NAME" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Minecraft server is running."
    else
        echo "Minecraft server is not running."
    fi
}

restart_server() {
    broadcast_message '{"text":"RESTART IN 5 MIN","color":"dark_red"}'
    sleep $((RESTART_WARNING_TIME - RESTART_FINAL_WARNING_TIME))
    broadcast_message '{"text":"RESTART IN 20 seconds","color":"dark_red"}'
    sleep $RESTART_FINAL_WARNING_TIME

    stop_server
    sleep 10
    start_server
}

case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        server_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
