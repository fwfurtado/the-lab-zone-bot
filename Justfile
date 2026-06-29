image := "the-lab-zone-slack-bot"
tag := "latest"

default:
    @just --list

build:
    docker build -t {{image}}:{{tag}} .

build-tag image_name tag_name:
    docker build -t {{image_name}}:{{tag_name}} .
