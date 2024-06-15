# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# TODO: Delete these comments
# # Remove the build folder if it exists
# RUN rm -rf build

# # Build the React app
# RUN npm run build

# Serve the React app
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
