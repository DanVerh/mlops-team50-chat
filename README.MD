### Web chat with AI-enabled message censor

# Tech spec

This is a web chat application, which

- authenticates users with Google Auth if such an option is enable during launch, otherwise accepts simple nickname as a login
- posts all chat messages to a single public channel in a format "nickname@time: message"
- for every posted message, sends a async http REST call to http://censor:80 endpoint with the text of the message as input, and receives True or False as an output.
- if True is received, puts green ok mark near the message, if False is received, puts red cross mark near the message, if no response is received for 1 second - puts red question mark near the message
- persist users and messages to some simple database which can be run locally or in google cloud
- written with modern python libraries like fastapi or similar
- has documentation, poetry configuration and dockerfile
- has github action to lint and run tests on each pull request and to deploy to google cloud on each release
