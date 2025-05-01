FROM node:alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

FROM node:alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build


CMD ["serve", "-s", "build", "-l", "3000"]