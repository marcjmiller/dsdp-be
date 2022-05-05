## Dependencies
- [Earthly](https://earthly.dev/get-earthly)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)


## To get started with Development
### Requirements
- Docker ([Ubuntu here](https://docs.docker.com/engine/install/ubuntu/))
- Docker-compose version 1.28.0 or later ([here](https://docs.docker.com/compose/install/))
- Earthly (instructions [here](https://earthly.dev/get-earthly))
### Running the development environment
- Clone the Repo
- Run `earthly +run-dev`
  - This is a hot-reloading backend, which means that as changes are made, the backend
reloads and applies those changes.
  - This will only run the backend environment, giving you access to the API specifically. In order to run the frontend, change directory to the frontend repo and run `yarn start`. Look in the [frontend repo](https://code.il2.dso.mil/platform-one/products/gvsc/sec/dsdp/frontend) for more information. 
## Run tests
- Run `earthly -P +all`

## Run Lint and Formatting
- Run `earthly +lint`
- Run `earthly +format`
