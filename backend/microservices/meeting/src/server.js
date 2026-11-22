const { Eureka } = require('eureka-js-client');
const app = require('./app');

const PORT = process.env.PORT || 8083;

const eurekaClient = new Eureka({
  instance: {
    app: 'MEETING',
    vipAddress: 'MEETING',
    instanceId: `MEETING:${PORT}`,
    hostName: 'localhost',
    ipAddr: '127.0.0.1',
    port: {
      '$': PORT,
      '@enabled': 'true',
    },
    homePageUrl: `http://localhost:${PORT}/`,
    statusPageUrl: `http://localhost:${PORT}/info`,
    healthCheckUrl: `http://localhost:${PORT}/health`,
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn',
    },
  },
  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/',
  },
});

app.listen(PORT, () => {
  console.log(`Meeting service running on port ${PORT}`);

  eurekaClient.start((error) => {
    if (error) {
      console.error('Eureka registration failed:', error);
      return;
    }

    console.log(`Service MEETING registered on port ${PORT}`);
  });
});