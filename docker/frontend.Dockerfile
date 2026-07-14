# ============================================================================
# AudioSmith AI — Frontend Dockerfile (Production)
# ============================================================================

# Stage 1: Dependencies and Build
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

# Copy application source
COPY frontend/ .

# Disable telemetry and build
ENV NEXT_TELEMETRY_DISABLED=1
ARG BACKEND_PROXY_URL
ENV BACKEND_PROXY_URL=${BACKEND_PROXY_URL}
RUN npm run build

# Stage 2: Production Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ARG BACKEND_PROXY_URL
ENV BACKEND_PROXY_URL=${BACKEND_PROXY_URL}

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy only the necessary files for the standalone server
COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT=3000

CMD ["node", "server.js"]
