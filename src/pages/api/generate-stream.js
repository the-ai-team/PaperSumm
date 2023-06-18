import EventSource from 'eventsource';

// Event: 'checkContinue';
// Event: 'checkExpectation';
// Event: 'clientError';
// Event: 'close';
// Event: 'connect';
// Event: 'connection';
// Event: 'dropRequest';
// Event: 'request';

export default async function handler(req, res) {
  // TODO: get url and keyword from query params
  const url = 'https://arxiv.org/abs/1512.03385';
  const keyword = 'Experiment and results';

  res.writeHead(200, {
    Connection: 'keep-alive',
    'Cache-Control': 'no-cache',
    'Content-Type': 'text/event-stream',
  });
  // TODO: check if res.flushHeaders() is needed
  res.flushHeaders();

  const endpoint = process.env.SERVER_ENDPOINT;
  const address = `${endpoint}/generate?url=${encodeURIComponent(
    url
  )}&keyword=${encodeURIComponent(keyword)}`;
  console.log('address', address);
  const eventSource = new EventSource(address);

  req.on('close', () => {
    console.log('req client closed connection');
    eventSource.close();
    res.end();
    return;
  });

  req.on('connect', () => {
    console.log('req client connected on connect');
    eventSource.close();
    res.end();
    return;
  });

  req.on('continue', () => {
    console.log('req client connected on continue');
    eventSource.close();
    res.end();
    return;
  });

  req.on('finish', () => {
    console.log('req client connected on finish');
    eventSource.close();
    res.end();
    return;
  });

  req.on('information', () => {
    console.log('req client connected on information');
    eventSource.close();
    res.end();
    return;
  });

  req.on('response', () => {
    console.log('req client connected on response');
    eventSource.close();
    res.end();
    return;
  });

  req.on('socket', () => {
    console.log('req client connected on socket');
    eventSource.close();
    res.end();
    return;
  });

  req.on('timeout', () => {
    console.log('req client connected on timeout');
    eventSource.close();
    res.end();
    return;
  });

  req.on('upgrade', () => {
    console.log('req client connected on upgrade');
    eventSource.close();
    res.end();
    return;
  });

  req.on('checkContinue', () => {
    console.log('req client connected on upgrade');
    eventSource.close();
    res.end();
    return;
  });

  res.on('checkExpectation', () => {
    console.log('req client connected on checkExpectation');
    eventSource.close();
    res.end();
    return;
  });

  res.on('clientError', () => {
    console.log('req client connected on clientError');
    eventSource.close();
    res.end();
    return;
  });

  req.on('close', () => {
    console.log('req client connected on close');
    eventSource.close();
    res.end();
    return;
  });

  res.on('close', () => {
    console.log('req client connected on close');
    eventSource.close();
    res.end();
    return;
  });

  res.on('connect', () => {
    console.log('req client connected on connect');
    eventSource.close();
    res.end();
    return;
  });

  res.on('connection', () => {
    console.log('req client connected on connection');
    eventSource.close();
    res.end();
    return;
  });

  res.on('dropRequest', () => {
    console.log('req client connected on dropRequest');
    eventSource.close();
    res.end();
    return;
  });

  res.on('request', () => {
    console.log('req client connected on request');
    eventSource.close();

    res.end();
    return;
  });

  res.on('finish', () => {
    console.log('req client connected on finish');
    eventSource.close();
    res.end();
    return;
  });

  res.on('end', () => {
    console.log('req client connected on end');
    eventSource.close();
    res.end();
    return;
  });

  res.on('error', () => {
    console.log('req client connected on error');
    eventSource.close();
    res.end();
    return;
  });

  res.on('timeout', () => {
    console.log('req client connected on finish');
    eventSource.close();
    res.end();
    return;
  });

  eventSource.addEventListener('content', (event) => {
    console.log('content received');
    res.write(`event: content\ndata: ${event.data}\nretry: 1000\n\n`);
    console.log(res);
  });

  eventSource.addEventListener('full-content', (event) => {
    console.log('full-content received');
    res.write(`event: full-content\ndata: ${event.data}\nretry: 1000\n\n`);
    eventSource.close();
    res.end();
    return;
  });

  eventSource.addEventListener('error', (event) => {
    res.write(`event: error\ndata: ${event.data}\nretry: 1000\n\n`);
    eventSource.close();
    res.end();
    return;
  });
}
