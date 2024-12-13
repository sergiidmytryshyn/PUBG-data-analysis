import discord
from discord.ext import commands
import requests
import time
from PIL import Image, ImageDraw
import ast
import plot_stats

INVOKE_LINK = "" # get your own
DB_KEY = "" # get your own
DS_TOKEN = "" # get your own
 
def send_api_request(req_type, api_request, body):
  headers = {
      'Authorization': f'Bearer {DB_KEY}'
  }

  full_url = f"{INVOKE_LINK}{api_request}"

  if req_type == "GET":
    response = requests.get(full_url, json=body, headers=headers)
  elif req_type == "POST":
    response = requests.post(full_url, json=body, headers=headers)

  return response.json()

def plot_trace(tel_data):
    # на стороні бота
    image = Image.open(f"maps/{tel_data['map']}.png")
    trace = []
    kills = []
    blue_zones = []
    draw = ImageDraw.Draw(image)
    a = 1

    if tel_data['map'] == "Savage_Main":
        a = 2
    elif tel_data['map'] == "Summerland_Main":
        a = 4
    elif tel_data['map'] == "Chimera_Main":
        a = 8/3


    for x_y in tel_data["blue_zones"]:
        blue_zones.append((a*x_y[0]//1000, a*x_y[1]//1000, a*x_y[2]//1000))

    for x_y in tel_data["trace"]:
        trace.append((a*x_y[0]//1000, a*x_y[1]//1000))

    for x_y in tel_data["kills"]:
        kills.append((a*x_y[0]//1000, a*x_y[1]//1000))


    draw.line(trace, fill="green", width=4)

    died = (a*tel_data['death_coords'][0]//1000, a*tel_data['death_coords'][1]//1000)
    landing = (a*tel_data['landing'][0]//1000, a*tel_data['landing'][1]//1000)

    for x,y,radius in blue_zones:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=None, outline="blue", width=2)

    x,y= landing
    radius = 4
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="orange")

    for x, y in kills:
        radius = 4
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="black")

    x,y= died
    radius = 4
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="red")



    output_path = f"images/{tel_data['map']}-trace-{tel_data['id']}.png"
    image.save(output_path, format="PNG", quality=100)
    return output_path

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def global_stats(ctx, player_name, refresh):
    job_run_id = send_api_request("POST", "/api/2.1/jobs/run-now", {"job_id": 629186380621308, "job_parameters": {"player_name": player_name, "refresh": refresh}})["run_id"]
    task_run_id = send_api_request("GET", "/api/2.1/jobs/runs/get", {"run_id": job_run_id})["tasks"][0]["run_id"]
    time.sleep(30)
    raw_result = send_api_request("GET", "/api/2.1/jobs/runs/get-output", {"run_id": task_run_id})["notebook_output"]["result"]
    if refresh != "refresh":
        idx = raw_result.find("created_at") 
        raw_result = raw_result[:idx - 3]
        raw_result += "}"
    data = ast.literal_eval(raw_result)
    html_path, image_path = plot_stats.plot(player_name, data)
    await ctx.send("Your statistics are ready!", file=discord.File(image_path))
    await ctx.send("Interactive version!", file=discord.File(html_path))


@bot.command()
async def get_matches(ctx, player_name):
    job_run_id = send_api_request("POST", "/api/2.1/jobs/run-now", {"job_id": 970727315602686 , "job_parameters": {"player_name": player_name}})["run_id"]
    task_run_id = send_api_request("GET", "/api/2.1/jobs/runs/get", {"run_id": job_run_id})["tasks"][0]["run_id"]
    time.sleep(30)
    raw_result = send_api_request("GET", "/api/2.1/jobs/runs/get-output", {"run_id": task_run_id})["notebook_output"]["result"]
    #result = '\n'.join(raw_result.replace("'", "").split(', '))
    await ctx.send(raw_result)

@bot.command()
async def match_recap(ctx, player_name, game_mode, match_id):
    job_run_id = send_api_request("POST", "/api/2.1/jobs/run-now", {"job_id": 14889150821369  , "job_parameters": {"player_name": player_name, "game_mode": game_mode, "match_id": match_id}})["run_id"]
    task_run_id = send_api_request("GET", "/api/2.1/jobs/runs/get", {"run_id": job_run_id})["tasks"][0]["run_id"]
    time.sleep(30)
    raw_result = send_api_request("GET", "/api/2.1/jobs/runs/get-output", {"run_id": task_run_id})["notebook_output"]["result"]
    data = ast.literal_eval(raw_result)
    output_path = plot_trace(data)
    await ctx.send('Your recap is ready!', file=discord.File(output_path))

bot.run(DS_TOKEN)
