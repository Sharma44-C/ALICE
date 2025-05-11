@app.route('/api', methods=['GET'])
def api():
    user_query = request.args.get('query')
    session_id = request.args.get('sessionId')

    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    if not session_id:
        return jsonify({"error": "No sessionId provided"}), 400

    # Save user message
    save_message(session_id, user_query, is_bot=False)

    # Get recent conversation history for this session
    conversation_history = get_last_messages(session_id, 15)
    full_message = "Conversation so far:\n{}\n\nUser: {}".format(
        '\n'.join(reversed(conversation_history)), user_query)

    # Get response from messageHandler
    response = messageHandler.handle_text_message(full_message, user_query)

    # Save bot response
    save_message(session_id, response, is_bot=True)

    return jsonify({"response": response})
