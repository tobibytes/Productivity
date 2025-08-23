FROM node:20-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; elif [ -f pnpm-lock.yaml ]; then corepack enable && pnpm i --frozen-lockfile; else npm ci; fi
COPY . .
EXPOSE 3000
CMD ["npm","run","dev"]
