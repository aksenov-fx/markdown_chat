import json

def stream_response(client, file_path, api_params):

    try:
        stream = client.chat.completions.create(**api_params)

        with open(file_path, "a", encoding="utf-8") as f:
            
            f.write(f"\n\n<hr class=\"__AI_plugin_role-assistant\">\n\n")

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    f.write(chunk.choices[0].delta.content)
                    f.flush()

            f.write(f"\n\n<hr class=\"__AI_plugin_role-user\">\n\n# ")

    except Exception as e:
        print(f"An error occurred: {str(e)}")