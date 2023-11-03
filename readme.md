apt install docker

git clone git@github.com:akayunov/test_task.git

cd test_task

docker build . -f build/Dockerfile  -t task

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

to run test: pytest tests