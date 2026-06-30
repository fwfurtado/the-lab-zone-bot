repository := "ofwfurtado"
image := "the-lab-zone-slack-bot"
tag := "latest"

default:
    @just --list

build:
    docker build -t {{repository}}/{{image}}:{{tag}} .

build-tag tag_name:
    docker build -t {{repository}}/{{image}}:{{tag_name}} .
