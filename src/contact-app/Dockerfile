FROM node:alpine AS builder

ARG REACT_APP_API_URL
ARG REACT_APP_AUTH_TOKEN

ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_AUTH_TOKEN=$REACT_APP_AUTH_TOKEN

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

FROM nginx:alpine
RUN mkdir -p /usr/share/nginx/html/contact-bot
COPY --from=builder /app/build/ /usr/share/nginx/html/contact-bot/
COPY nginx.conf /etc/nginx/conf.d/default.conf