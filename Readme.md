


# A setup to analyse darshan logs

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
chmod +x ./kind
sudo mv kind /bin
#kind create cluster --name io
sudo kind create cluster --name io --kubeconfig /home/eidf114/eidf114/lp-eidfstaff/io_benchmarks_setup/kubeconfig
sudo ./install_helm.sh
```

There seems to be a bug and you need to change the version of cni conflist to 0.4.0 ( see https://github.com/containers/podman-compose/issues/752 ).

```bash
# Build the image with podman
podman build -t hello:latest .

# Save the image to a tar file
podman save -o hello.tar hello:latest

# Load the image into kind cluster
sudo kind load image-archive hello.tar --name io

# Verify the image is loaded
sudo podman exec io-control-plane crictl images | grep hello
```

See the output with  `kubectl logs <podname>` . This is possible as long as the pod was not previously destroyed.

# Setting up influxdb

```bash
kubectl apply -f influxdb-k8-minikube.yaml 
```

You can forward a port from the influxdb service using 

```bash
kubectl port-forward service/influxdb 8086:8086
```

Go to `localhost:8086` and follow the GUI instructions.

```bash
bucket: darshan-explorer  
```

## Setup the python interface

```bash
sudo apt-get install python3.10-venv
python3 -m venv parser_env
python3 -m pip install -r requirements.txt
source parser_env/bin/activate
```

## Upload the data

```bash
cd parser
python3 submit_darshan.py
```