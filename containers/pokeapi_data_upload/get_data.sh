ditto clone --src-url='https://pokeapi.co' --dest-dir $DATA_DIR --select ability
aws s3 cp $DATA_DIR $S3_URI --recursive