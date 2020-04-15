class RedisCacheManagement {
  /// Constructor.
  constructor() {
    const redis = require('redis');
    const client = redis.createClient(
      6380,
      'TownHallTrivia.redis.cache.windows.net',
      { auth_pass: '8A7NPLCIRpH0zBL6XbC+p1OrTsO+JTwPeCZJITIqiKc=',
        tls: { servername: 'TownHallTrivia.redis.cache.windows.net' }});
  }

  write() {
    client.set('key1', 'value', (err, reply) => { console.log(reply); });
  }

  read() {
    client.get('key1', (err, reply) => { console.log(reply); });
  }
}