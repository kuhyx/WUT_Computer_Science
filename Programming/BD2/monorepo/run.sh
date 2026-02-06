#!/bin/sh
cd apps/backend
npx prisma generate
cd ../../
nx run-many --target=serve --projects=frontend,backend --parallel
