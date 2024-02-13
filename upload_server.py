# upload_server.py
from flask import Flask, request, jsonify
import os
import discord
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest

load_dotenv()
TOKEN = os.getenv('MTIwNjk5NjgwNDA3MjI1MTM5Mg.GJumAI.HTDpo-0w7mBGdz9laWn_HM7ousQJQSjGXdbIIs')
GUILD = os.getenv('1206997917022294136')
CHANNEL_ID = os.getenv('1206998630796365836')

client = discord.Client()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            file.save(file.filename)
            send_to_discord(file.filename)
            os.remove(file.filename)
            return jsonify({'message': 'File successfully uploaded and sent to Discord.'}), 200
        return '''
        <!doctype html>
        <title>Upload File to Discord Bot</title>
        <h1>Upload a file to send to Discord</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'message': 'An error occurred while processing the request.'}), 500
        
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, id=int(CHANNEL_ID))
    print(f'{client.user} has connected to Discord!')
    print(f'Sending files to: {channel}')

def send_to_discord(filename):
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, id=int(CHANNEL_ID))

    with open(filename, 'rb') as f:
        file = discord.File(f)
        client.loop.create_task(channel.send(file=file))

if __name__ == '__main__':
    app.run(debug=True)
    client.run(TOKEN)
