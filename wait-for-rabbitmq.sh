#!/bin/sh
# wait-for-rabbitmq.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z $host $port; do
  echo "RabbitMQ no está disponible - esperando..."
  sleep 2
done

echo "RabbitMQ está listo - ejecutando comando"
exec $cmd