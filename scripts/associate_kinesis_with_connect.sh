#!/bin/bash
INSTANCE_ID="arn:aws:connect:us-west-2:123456789012:instance/abcd1234-efgh-5678-ijkl-901234567890"
STREAM_ARN="arn:aws:kinesis:us-west-2:123456789012:stream/MyKinesisStream"
ROLE_ARN="arn:aws:iam::123456789012:role/KinesisConnectRole"

aws connect associate-kinesis-video-stream \
    --instance-id $INSTANCE_ID \
    --stream-arn $STREAM_ARN \
    --role-arn $ROLE_ARN
