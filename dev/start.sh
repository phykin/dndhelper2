#!/usr/bin/bash

docker compose -f docker-compose.yml up -d --build && docker compose -f docker-compose.yml logs --follow