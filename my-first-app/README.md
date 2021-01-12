# my-first-app

> A GitHub App built with [Probot](https://github.com/probot/probot) that A probot app testing for SP2020

## Setup

```sh
# Install dependencies
npm install

# Compile
npm run build

# Run
npm run start
```

## Docker

```sh
# 1. Build container
docker build -t my-first-app .

# 2. Start container
docker run -e APP_ID=<app-id> -e PRIVATE_KEY=<pem-value> my-first-app
```

## Contributing

If you have suggestions for how my-first-app could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the [Contributing Guide](CONTRIBUTING.md).

## License

[ISC](LICENSE) © 2020 aomsw13 <disneybabyaom@hotmail.com>
