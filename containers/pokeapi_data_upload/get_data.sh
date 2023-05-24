#https://github.com/pokeapi/ditto
# TODO json logging
ditto clone --src-url='https://pokeapi.co' --dest-dir $DATA_DIR
ditto analyze --data-dir $DATA_DIR
# ditto transform --base-url $BASE_URL
aws s3 cp $DATA_DIR $S3_URI --recursive