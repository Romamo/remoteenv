from remoteenv.zoo import ZooEnv


env = ZooEnv('prefix', 'zoohost:2181')
env.start()
for k, v in env.read('mod', 'h4', 'mod/h4'):
    print(f"{k}={v}")
env.stop()
