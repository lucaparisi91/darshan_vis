# A setup to analysize darshan logs

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
chmod +x ./kind
sudo mv kind /bin
#kind create cluster --name io
sudo opt/bin/kind create cluster --name io --kubeconfig /home/eidf114/eidf114/lp-eidfstaff/io_benchmarks_setup/kubeconfig
```

There seems to be a bug and you need to change the version of cni conflist to 0.4.0 ( see https://github.com/containers/podman-compose/issues/752 ).
