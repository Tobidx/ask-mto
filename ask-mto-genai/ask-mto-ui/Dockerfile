# Use Node.js LTS
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY ask-mto-genai/ask-mto-ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend code
COPY ask-mto-genai/ask-mto-ui/ ./

# Build the Next.js app
RUN npm run build

# Expose the port Next.js runs on
ENV PORT=3000
EXPOSE 3000

# Start the app
CMD ["npm", "start"] 