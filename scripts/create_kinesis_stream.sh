```bash
#!/bin/bash

# Usage function
usage() {
  echo "Usage: $0 -n STREAM_NAME -s SHARD_COUNT"
  exit 1
}

# Parse command-line arguments
while getopts ":n:s:" opt; do
  case $opt in
    n) STREAM_NAME="$OPTARG"
    ;;
    s) SHARD_COUNT="$OPTARG"
    ;;
    *) usage
    ;;
  esac
done

# Validate input
if [ -z "$STREAM_NAME" ] || [ -z "$SHARD_COUNT" ]; then
  usage
fi

# Create Kinesis stream
aws kinesis create-stream --stream-name $STREAM_NAME --shard-count $SHARD_COUNT

# Verify the stream creation
if [ $? -eq 0 ]; then
  echo "Kinesis stream '$STREAM_NAME' with $SHARD_COUNT shard(s) created successfully."
else
  echo "Failed to create Kinesis stream '$STREAM_NAME'."
  exit 1
fi
