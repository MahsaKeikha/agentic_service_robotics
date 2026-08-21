def authorize(action):
    return {"allowed":False,"reason":"physical execution outside scope"} if action in {"robot_command","actuate"} else {"allowed":True}
