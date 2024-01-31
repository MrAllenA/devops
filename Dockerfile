# Use a base image
FROM ubuntu:latest

RUN apt-get update && apt-get install fortune-mod cowsay -y && apt-get install netcat -y
ENV PATH="/usr/games:$PATH"

# Set the working directory
WORKDIR /app/wisecow

# Copy the shell script into the image
COPY wisecow/ /app/wisecow

RUN ls
RUN pwd
# Make the script executable (if needed)
RUN chmod +x /app/wisecow/wisecow.sh
# Define the default command to run when the container starts
CMD ["sh", "-c", "./wisecow.sh"]

