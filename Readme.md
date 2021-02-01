##  Build the docker image:
docker image build -t todo-youtube .

## Review list of images:
docker image ls

## Run the docker container
docker run -p 5001:5000 -d todo-youtube -t