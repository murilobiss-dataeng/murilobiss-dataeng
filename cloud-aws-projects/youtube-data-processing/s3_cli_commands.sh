# To copy all JSON Reference data to same location:
aws s3 cp . s3://bucket-to-write/youtube/ --recursive --exclude "*" --include "*.json"

# To copy all data files to its own location, following Hive-style patterns:
aws s3 cp CAvideos.csv s3://bucket-to-write/youtube/region=ca/
aws s3 cp DEvideos.csv s3://bucket-to-write/youtube/region=de/
aws s3 cp FRvideos.csv s3://bucket-to-write/youtube/region=fr/
aws s3 cp GBvideos.csv s3://bucket-to-write/youtube/region=gb/
aws s3 cp INvideos.csv s3://bucket-to-write/youtube/region=in/
aws s3 cp JPvideos.csv s3://bucket-to-write/youtube/region=jp/
aws s3 cp KRvideos.csv s3://bucket-to-write/youtube/region=kr/
aws s3 cp MXvideos.csv s3://bucket-to-write/youtube/region=mx/
aws s3 cp RUvideos.csv s3://bucket-to-write/youtube/region=ru/
aws s3 cp USvideos.csv s3://bucket-to-write/youtube/region=us/