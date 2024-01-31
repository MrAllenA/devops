# Use a base image
FROM ubuntu:latest

RUN apt-get update && apt-get install fortune-mod cowsay -y && apt-get install netcat -y
ENV PATH="/usr/games:$PATH"

# Set the working directory


# Copy the shell script into the image
COPY wisecow/ /wisecow

# Make the script executable (if needed)
RUN chmod +x /wisecow/wisecow.sh
# Define the default command to run when the container starts
CMD ["sh", "-c", "./wisecow.sh"]

