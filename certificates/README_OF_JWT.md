# Issue RSA private key + public key pair

```shell
openssl genrsa -out jprivate-key.pem 2048
```

```shell
openssl rsa -in private-key.pem -outform PEM -pubout -out public-key.pem
```
