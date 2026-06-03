aws eks update-kubeconfig --region eu-west-1 --name crypto-streaming-eks

kubectl apply -f k8s/

kubectl get pods -n crypto-streaming
kubectl get svc -n crypto-streaming
kubectl get ingress -n crypto-streaming