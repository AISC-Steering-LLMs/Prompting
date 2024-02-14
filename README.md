__Prompt generation for moral concepts__ <be>

Method: meta-prompting, using GPT-4. I do this programmatically and by calling the model via the API. This way, I get to generate hundreds of unique pairs of prompts. See more in csv_generation.py.

To run the code as a Linux user:

- Go to https://platform.openai.com/api-keys
- Create an API key
- Copy the API key
- Open a terminal
- Type:

```
code ~/.bashrc
```
- to open your bashrc file in VS Code, or type the command for your preferred text editor instead of "code".
- Scroll to the end of your bashrc file
- Type:

```
export OPENAI_API_KEY='your_api_key_here'
```
- Save the file
- Back at your terminal, type:

```
source ~/.bashrc
```
- Having git cloned this repo from Github, for whichever Python enevirnment you are using, you will need to install the openai library eg

```
pip install openai

```
- Before the code will run, you will need to pay for at least $1 worth of api usage, otherwise you will not have api access to gpt4 which is the model currently used in the code.
- The code should now run.
- You may get an error about api versions and a suggestion to run the following on your command line:

```
openai migrate
```
- I did this and it updated my code to reflect the code to relfec the latest api changes.
