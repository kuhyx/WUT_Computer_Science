#!/bin/sh
pnpm i
nx run-many --target=serve --projects=frontend,backend --parallel
