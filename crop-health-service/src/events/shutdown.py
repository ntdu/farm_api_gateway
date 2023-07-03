async def event_01_disconnect_redis():
    pass


events = [v for k, v in locals().items() if k.startswith("event_")]