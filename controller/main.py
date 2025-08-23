from controller import ControllerRedisStream

crs = ControllerRedisStream()

if __name__ == "__main__":
    crs.listen()
