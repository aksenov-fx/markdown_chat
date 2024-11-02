def streamer(mode, client, file_path, api_params):

    try:
        # Add the assistant marker before starting the stream
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n<hr class=\"__AI_plugin_role-assistant\">\n\n")
            f.flush()

        # ChatGPT streaming
        if mode.startswith("ChatGPT"):
            stream = client.chat.completions.create(**api_params)
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(chunk.choices[0].delta.content)
                        f.flush()

        # Claude streaming
        elif mode.startswith("Claude"):
            with client.messages.stream(**api_params) as stream:
                for text in stream.text_stream:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(text)
                        f.flush()

        # Add the user marker after the stream is complete
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n<hr class=\"__AI_plugin_role-user\">\n\n# ")
            f.flush()

    except Exception as e:
        print(f"An error occurred: {str(e)}")