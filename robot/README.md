# Converting OWL to OBO via Robot

Ontologies expressed in an OWL format can be converted to OBO format with
a [tool called robot](http://robot.obolibrary.org/convert). While you can
download and run the Java-based application, this directory contains a simply
containerized version that avoids installing any of the Java or Robot
toolchain directly.

You can use my prebuilt version of robot via DockerHub or build it yourself.


## Building the image

You can build the docker image for robot by
```sh
cd robot
docker build -t robot .
```

## Using the image

If you built the image yourself, just replace the dockerhub reference (`alexmilowski/robot`) with the image tag you used (e.g., `robot`).

The command can be invoked with a simple docker run command:

```sh
docker run -it --rm alexmilowski/robot
```

You should map your local directory containing your files to the `/home`
directory for processing:

```sh
docker run -it --rm -v /home:`pwd` alexmilowski/robot
```

## Converting OWL to OBO

Some ontologies are only distributed in OWL format. You can convert these files into OBO format by downloading them and running the robot tool via the docker image.

For example, the [Coronavirus Infectious Disease Ontology](http://www.obofoundry.org/ontology/cido.html) is distributed in OWL format. This can be converted by:

1. Download the OWL formatted ontology via curl:

    ```sh
    curl -O https://raw.githubusercontent.com/CIDO-ontology/cido/master/src/ontology/cido.owl
    ```

1. Run the robot convert command, ensuring you map the correct directory:

    ```sh
    docker run -it --rm -v `pwd`:/home alexmilowski/robot convert --check false --input cido.owl --output cido.obo
    ```

Note: The `--check` option may or may not be necessary. See the robot documentation for more information.
