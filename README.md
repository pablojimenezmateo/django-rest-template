# Django REST Template

This is a template project for building RESTful APIs using Django and Django REST Framework.

## Getting Started

To get started with this project, follow these steps:

1. Install [docker](https://www.docker.com/)
2. Clone the repository: `git clone https://github.com/pablojimenezmateo/django-rest-template.git`
3. Copy the infra/dev/sample.env to infra/dev/.env and modify as you like
4. Run `make` on the root of the repository
5. Open http://localhost:8181/admin or http://localhost:8181/swagger

## Features

- Docker compose with all the necessary services
- User authentication using tokens
- Custom logging to files
- Celery worker
- Postgres database
- Swagger
- Optional [frontend project](https://github.com/pablojimenezmateo/react-vite-template.git)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for more information.
