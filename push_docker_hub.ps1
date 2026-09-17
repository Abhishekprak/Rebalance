$version="4"
$imageName = "kaushiknifty/nifty-rebalance:$version"
# $gcrImageName = "asia-south1-docker.pkg.dev/nifty-shloka-stf/nifty-shloka-stf/nifty-stf:$version"

docker build -t $imageName .

# gcloud auth configure-docker asia-southeast1-docker.pkg.dev

# docker tag $imageName $gcrImageName

# # Push the Docker image to the registry
# docker push $gcrImageName

docker push $imageName