USER="return1225"
NAME="tkdcompetition";\
TAG=$(git rev-parse --short HEAD);\
PORT="5000";\
IMG=$(docker image ls | grep $NAME | grep $TAG | awk '{print $1}');\

if [ -z "$TAG" ]
then
    TAG=$(date +%Y%m%d%H%M);\
fi

if [ "$1" == 'build' ]
then
    echo "### Force to build image >>>";\
    docker image build . -t $USER/$NAME:$TAG;\

elif [ -z "$IMG" ]
then
    docker image pull $USER/$NAME:$TAG;\
    if [ $? -eq 1 ]
    then
        echo "### Build image >>>";\
        docker image build . -t $USER/$NAME:$TAG;\
    else
        echo "### Image downloaded :))";\
        echo $IMG;\
    fi
else
    echo "### Image found :))";\
    echo $IMG;\
fi

CTNER=$(docker container ls -a | grep $NAME | awk '{print $1}');\

if [ ! -z "$CTNER" ]
then
    echo "### Remove container before running ...";\
    docker container rm -f $CTNER;\
fi

docker container run -d \
    --name $NAME \
    -p $PORT:$PORT \
    -v $(pwd)/secrets:/home/app/secrets \
    --restart=unless-stopped \
    $USER/$NAME:$TAG;\

if [ "$1" == 'push' ] || [ "$2" == 'push' ]
then
    echo "### Push image $USER/$NAME:$TAG >>>";\
    docker image push $USER/$NAME:$TAG;\
fi
